#!/usr/bin/env python3
"""ingest_source.py - onboard a marketplace, plugin, or repo into OpenCode.

Part of the opencode-sync skill. Given one source (a local path or a git URL),
this resolves it to a local checkout, detects whether it is a Claude Code
marketplace, a single plugin, or a plain repo, discovers every assessable tool
(skills, agents, commands, MCP servers), and emits the OpenCode config that makes
them work: skills.paths for discovery, a permission.skill deny-list for the
reference-only skills, MCP blocks, and a resolution note for AGENTS.md. Agent
generation is delegated to sync_agents.py.

The script is non-interactive on purpose so it runs identically on Claude Code and
OpenCode. The SKILL.md Mode E flow drives the questions (config target, clone
location) and re-invokes with the chosen flags.

Config routing:
  --config-target global|project|both   default target for unlisted plugins
  --global-plugins NAME...               route these plugins to the global config
  --project-plugins NAME...              route these plugins to the project config
  --no-deny                              enable all skills (skip the deny-list)
  --respect-claude-settings              mirror ~/.claude enablement: expose only enabled
                                         plugins, deny disabled ones, emit user-scope MCP (global)
  --wire-memory                          add an `instructions` array so OpenCode auto-loads memory
  --opencode-json PATH                   explicit single config file

Exit: 0 ok | 2 bad args / nothing found | 3 url not found locally (caller should ask)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Reuse the validated discovery + classification from validate_dual.py.
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from validate_dual import discover, split_frontmatter, fm_get
except Exception as e:  # pragma: no cover - import guard
    print(f"ERROR: cannot import validate_dual helpers: {e}", file=sys.stderr)
    sys.exit(2)

URL_RE = re.compile(r"^(https?://|git@|ssh://|git://)")


def repo_name_from_url(url):
    name = url.rstrip("/").split("/")[-1]
    return name[:-4] if name.endswith(".git") else name


def git(args, cwd):
    try:
        out = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=60)
        return out.returncode, out.stdout.strip(), out.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def find_local_clone(name, search_roots):
    for root in search_roots:
        cand = Path(root).expanduser() / name
        if (cand / ".git").exists():
            return cand
    return None


def currency_report(repo, do_fetch):
    """Report dirty / ahead / behind so the caller can confirm the clone is current."""
    notes = []
    rc, dirty, _ = git(["status", "--porcelain"], repo)
    if dirty:
        notes.append(f"{len(dirty.splitlines())} uncommitted change(s)")
    if do_fetch:
        git(["fetch", "--quiet"], repo)
    rc, ahead, _ = git(["rev-list", "--count", "@{u}..HEAD"], repo)
    rc2, behind, _ = git(["rev-list", "--count", "HEAD..@{u}"], repo)
    if rc == 0 and ahead.isdigit() and int(ahead) > 0:
        notes.append(f"{ahead} commit(s) ahead of upstream")
    if rc2 == 0 and behind.isdigit() and int(behind) > 0:
        notes.append(f"{behind} commit(s) behind upstream (run git pull)" if not do_fetch
                     else f"{behind} behind after fetch (run git pull)")
    return notes or ["clean and current" if do_fetch else "clean (no fetch; pass --fetch to compare upstream)"]


def resolve_source(args):
    """Return (local_path, note) or exits with a status the caller can act on."""
    if args.local_path:
        p = Path(args.local_path).expanduser()
        if not p.is_dir():
            print(f"ERROR: --local-path {p} is not a directory", file=sys.stderr)
            sys.exit(2)
        return p, "using provided local path"

    src = args.source
    if not URL_RE.match(src):
        p = Path(src).expanduser()
        if p.is_dir():
            return p, "using local directory"
        print(f"ERROR: {src} is neither a URL nor an existing directory", file=sys.stderr)
        sys.exit(2)

    name = repo_name_from_url(src)
    if args.clone_into:
        dest = Path(args.clone_into).expanduser() / name
        if dest.exists():
            return dest, f"clone target {dest} already exists - reusing"
        dest.parent.mkdir(parents=True, exist_ok=True)
        print(f"cloning {src} -> {dest} (shallow)")
        rc, _, err = git(["clone", "--depth", "1", src, str(dest)], dest.parent)
        if rc != 0:
            print(f"ERROR: clone failed: {err}", file=sys.stderr)
            sys.exit(2)
        return dest, "freshly cloned"

    found = find_local_clone(name, args.search_roots)
    if found:
        notes = currency_report(found, args.fetch)
        return found, "found local clone: " + "; ".join(notes)

    print(f"URL_NOT_FOUND_LOCALLY name={name}", file=sys.stderr)
    print(f"No local clone of '{name}' under {', '.join(args.search_roots)}.", file=sys.stderr)
    print("Re-run with --local-path <dir> if you have it elsewhere, "
          "or --clone-into <dir> to clone it.", file=sys.stderr)
    sys.exit(3)


def detect_type(root):
    if (root / ".claude-plugin" / "marketplace.json").exists():
        return "marketplace"
    if (root / ".claude-plugin" / "plugin.json").exists():
        return "plugin"
    return "repo"


def marketplace_plugin_dirs(root):
    """Return plugin dirs listed in marketplace.json (local sources only)."""
    mp = json.loads((root / ".claude-plugin" / "marketplace.json").read_text())
    dirs = []
    for p in mp.get("plugins", []):
        src = p.get("source", "")
        if isinstance(src, str) and src.startswith("./"):
            d = root / src[2:]
            if d.is_dir():
                dirs.append(d)
    return dirs


def classify_skill(skill_path):
    """invocable vs hide, using disable-model-invocation + user-invocable."""
    fm, _body, _ = split_frontmatter(Path(skill_path).read_text(encoding="utf-8", errors="replace"))
    if fm is None:
        return "invocable"  # malformed; expose so it is visible and gets validated
    dmi = bool(re.search(r"^disable-model-invocation:\s*true", fm, re.MULTILINE))
    uinv = fm_get(fm, "user-invocable")
    user_off = (uinv is not None and str(uinv).lower() == "false")
    return "hide" if (dmi and user_off) else "invocable"


def find_mcp_servers(root, scan_dirs=None):
    """Collect mcpServers from any .mcp.json in the source or selected subdirs."""
    servers = {}
    files = []
    if scan_dirs:
        for d in scan_dirs:
            files.extend(list(Path(d).rglob(".mcp.json")))
            files.extend(list(Path(d).glob(".mcp.json")))
    else:
        files = list(root.rglob(".mcp.json")) + list(root.glob(".mcp.json"))
    for f in files:
        try:
            data = json.loads(f.read_text())
            if isinstance(data.get("mcpServers"), dict):
                servers.update(data["mcpServers"])
            elif isinstance(data, dict):
                # Official Claude plugin cache entries often use the simpler
                # {"name": {command/url...}} shape directly in .mcp.json.
                servers.update({k: v for k, v in data.items() if isinstance(v, dict)})
        except Exception:
            continue
    return servers


def discover_source(root, kind):
    skills, agents, commands = [], [], []
    if kind == "marketplace":
        scan_dirs = marketplace_plugin_dirs(root) or [root]
    else:
        scan_dirs = [root]
    for d in scan_dirs:
        for path, k in discover(str(d), "deep"):
            if k == "skill":
                skills.append(path)
            elif k == "agent":
                agents.append(path)
            elif k == "command":
                commands.append(path)
    skills = sorted(set(skills))
    hide = [s for s in skills if classify_skill(s) == "hide"]
    return {
        "skills": skills,
        "hide": hide,
        "agents": sorted(set(agents)),
        "commands": sorted(set(commands)),
        "mcp": find_mcp_servers(root),
    }


def filter_discovery_to_units(root, kind, disc, allowed_units):
    if kind != "marketplace":
        return disc
    allowed_dirs = []
    for _name, sk in allowed_units:
        base = sk.parent if sk.name == "skills" else sk
        allowed_dirs.append(base.resolve())

    def under_allowed(path):
        rp = Path(path).resolve()
        return any(base == rp or base in rp.parents for base in allowed_dirs)

    return {
        "skills": [p for p in disc["skills"] if under_allowed(p)],
        "hide": [p for p in disc["hide"] if under_allowed(p)],
        "agents": [p for p in disc["agents"] if under_allowed(p)],
        "commands": [p for p in disc["commands"] if under_allowed(p)],
        "mcp": find_mcp_servers(root, scan_dirs=allowed_dirs),
    }


def to_opencode_mcp(servers):
    out = {}
    for name, cfg in servers.items():
        if cfg.get("url"):
            out[name] = {"type": "remote", "url": cfg["url"], "enabled": True}
        else:
            cmd = [cfg["command"]] + cfg.get("args", []) if cfg.get("command") else cfg.get("command", [])
            out[name] = {"type": "local", "command": cmd, "enabled": True}
    return out


def skill_name(skill_path):
    return Path(skill_path).parent.name


AGENTS_RESOLUTION_BLOCK = """
## OpenCode cross-runtime resolution (added by opencode-sync)

When you encounter these Claude Code tokens, resolve them yourself - OpenCode does
not expand them automatically:

- `${CLAUDE_PLUGIN_ROOT}` means `plugins/<that-plugin>/` from the repo root.
- A `plugin:skill` reference (for example in a `Skill(\"plugin:skill\")` call) resolves
  to `plugins/<plugin>/skills/<skill>/SKILL.md`. Load it with the Read tool on a
  need-to-know basis, or invoke the discovered skill by its bare name via the skill tool.
- Reference-only skills (denied in permission.skill) are not in the skill list; load
  them by reading their SKILL.md path directly when a body references them.
"""


def rules_file_state(root):
    """Return (Path of the rules file OpenCode reads, block_present) or (None, False)."""
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = root / name
        if p.exists():
            present = "OpenCode cross-runtime resolution" in p.read_text(encoding="utf-8", errors="replace")
            return p, present
    return None, False


def ensure_resolution_block(root, apply):
    """Place the resolution block without shadowing an existing CLAUDE.md.

    AGENTS.md exists -> append to it. Only CLAUDE.md exists -> append to it (creating a
    new AGENTS.md would make OpenCode ignore CLAUDE.md). Neither -> create AGENTS.md.
    """
    target, present = rules_file_state(root)
    if target and present:
        return f"resolution block already in {target.name}"
    if target is None:
        target = root / "AGENTS.md"
        body = (f"# {root.name} - Instructions\n\n"
                f"Rules file, read by Claude Code and OpenCode.\n{AGENTS_RESOLUTION_BLOCK}")
        action = f"create {target.name} with the resolution block"
    else:
        body = target.read_text(encoding="utf-8").rstrip() + "\n" + AGENTS_RESOLUTION_BLOCK
        action = f"append the resolution block to {target.name}"
    if apply:
        target.write_text(body, encoding="utf-8")
    return ("" if apply else "would ") + action


def plugin_units(root, kind):
    """Return [(plugin_name, skills_dir)] for routing. Marketplace -> each plugin's
    skills dir; plugin/repo -> the source root as a single unit."""
    units = []
    if kind == "marketplace":
        for d in (marketplace_plugin_dirs(root) or [root]):
            sk = d / "skills"
            units.append((d.name, sk if sk.is_dir() else d))
    else:
        units.append((root.name, root))
    return units


def route(plugin_name, args):
    """Which config targets a plugin goes to: a subset of {global, project}."""
    if args.global_plugins and plugin_name in args.global_plugins:
        return {"global"}
    if args.project_plugins and plugin_name in args.project_plugins:
        return {"project"}
    if args.config_target == "both":
        return {"global", "project"}
    return {args.config_target}


def merge_opencode(existing, cfg):
    """Merge a config fragment into an opencode.json dict: union skills.paths,
    merge permission.skill (deny wins), add new mcp entries."""
    existing.setdefault("$schema", "https://opencode.ai/config.json")
    if "skills" in cfg:
        sk = existing.setdefault("skills", {})
        sk["paths"] = list(dict.fromkeys([*(sk.get("paths") or []), *cfg["skills"]["paths"]]))
    if "instructions" in cfg:
        existing["instructions"] = list(dict.fromkeys([*(existing.get("instructions") or []), *cfg["instructions"]]))
    if "permission" in cfg:
        existing.setdefault("permission", {}).setdefault("skill", {}).update(cfg["permission"]["skill"])
    if "mcp" in cfg:
        mcp = existing.setdefault("mcp", {})
        for k, v in cfg["mcp"].items():
            mcp.setdefault(k, v)
    return existing


def _norm(p):
    return os.path.normpath(str(p))


def prune_source_entries(existing, target_kind, target_path, source_root, all_units, source_skill_names):
    """Remove stale entries for this source before merging fresh config.

    `merge_opencode()` is additive by design, which is fine for combining marketplaces,
    but wrong for re-running ingest on the same source with a stricter Claude enablement
    filter. In that case, paths for previously enabled plugins would linger forever.
    """
    skills = existing.get("skills") or {}
    old_paths = list(skills.get("paths") or [])
    if old_paths:
        managed = {_norm(sk) for _name, sk in all_units}
        kept = []
        for raw in old_paths:
            resolved = Path(raw)
            if not resolved.is_absolute():
                resolved = (target_path.parent / resolved).resolve()
            if _norm(resolved) in managed:
                continue
            kept.append(raw)
        skills["paths"] = kept

    perm = ((existing.get("permission") or {}).get("skill") or {})
    for name in source_skill_names:
        if name != "*":
            perm.pop(name, None)


def _load_json(path):
    try:
        return json.loads(Path(path).expanduser().read_text())
    except Exception:
        return {}


def marketplace_name(root):
    mp = root / ".claude-plugin" / "marketplace.json"
    if mp.exists():
        try:
            return json.loads(mp.read_text()).get("name") or root.name
        except Exception:
            pass
    return root.name


def claude_enablement(root):
    """Read Claude settings (user + project + local) -> (enabled set, disabled set, user_mcp dict).

    enabledPlugins keys are 'plugin@marketplace'; only entries for this source's marketplace count.
    user_mcp is the user-scope mcpServers from ~/.claude/settings.json - a per-user concern that
    belongs in the global OpenCode config, never duplicated per project.
    """
    mkt = marketplace_name(root)
    user = _load_json(Path.home() / ".claude" / "settings.json")
    proj = _load_json(root / ".claude" / "settings.json")
    local = _load_json(root / ".claude" / "settings.local.json")
    enabled, disabled = set(), set()
    for src in (user, proj, local):
        for key, on in (src.get("enabledPlugins") or {}).items():
            name, _, m = key.partition("@")
            if m and m != mkt:
                continue
            (enabled if on else disabled).add(name)
    return enabled, disabled, (user.get("mcpServers") or {})


def filter_units_by_enablement(units, enabled, disabled):
    if enabled:
        return [(n, sk) for (n, sk) in units if n in enabled and n not in disabled]
    if disabled:
        return [(n, sk) for (n, sk) in units if n not in disabled]
    return list(units)


def default_agent_out_dir(target_keys, explicit_out_dir):
    if explicit_out_dir:
        return explicit_out_dir
    if "global" in target_keys:
        return str(Path.home() / ".config" / "opencode" / "agent")
    return ".opencode/agent"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help="local path or git URL of the marketplace/plugin/repo")
    ap.add_argument("--local-path", help="use this existing checkout (I already have it)")
    ap.add_argument("--search-roots", nargs="+", default=[str(Path.home() / "Projects")],
                    help="dirs to search for an existing clone (default: ~/Projects)")
    ap.add_argument("--clone-into", help="clone the URL into this dir and use it")
    ap.add_argument("--fetch", action="store_true", help="git fetch before the currency check")
    ap.add_argument("--config-target", choices=["global", "project", "both"], default="project",
                    help="where unlisted plugins go; 'both' routes every plugin to global AND project")
    ap.add_argument("--global-plugins", nargs="*", default=[], help="plugin names to route to the global config")
    ap.add_argument("--project-plugins", nargs="*", default=[], help="plugin names to route to the project config")
    ap.add_argument("--no-deny", action="store_true", help="enable all skills (skip the reference-only deny-list)")
    ap.add_argument("--respect-claude-settings", action="store_true",
                    help="mirror Claude's enabledPlugins + mcpServers from ~/.claude/settings.json and the "
                         "repo's .claude/settings(.local).json: expose only enabled plugins, deny disabled ones, "
                         "and emit user-scope MCP servers to the global config")
    ap.add_argument("--wire-memory", action="store_true",
                    help="add an `instructions` array so OpenCode auto-loads memory at session start "
                         "(AGENTS.md + ~/.claude/memory/memory.md), replacing the Claude SessionStart hook")
    ap.add_argument("--opencode-json", help="explicit single config file (use with --config-target global or project)")
    ap.add_argument("--opencode-agent-dir",
                    help="output directory for generated agents (default: ~/.config/opencode/agent when any global target is used, otherwise .opencode/agent)")
    ap.add_argument("--apply", action="store_true", help="write the config and generate agents")
    ap.add_argument("--add-resolution-block", action="store_true",
                    help="add the ${CLAUDE_PLUGIN_ROOT}/plugin:skill resolution block to the rules file "
                         "(AGENTS.md, or CLAUDE.md, or a new AGENTS.md if neither exists)")
    ap.add_argument("--dry-run", action="store_true", help="preview only (default)")
    args = ap.parse_args()
    if not args.source and not args.local_path:
        ap.error("provide a source path/URL or --local-path")

    root, note = resolve_source(args)
    kind = detect_type(root)
    disc = discover_source(root, kind)

    # Resolve the two possible target files.
    explicit = Path(args.opencode_json).expanduser() if args.opencode_json else None
    target_paths = {
        "global": (explicit if (explicit and args.config_target == "global")
                   else Path.home() / ".config" / "opencode" / "opencode.json"),
        "project": (explicit if (explicit and args.config_target == "project")
                    else root / "opencode.json"),
    }

    # Route each plugin to global / project, building skills.paths per target.
    all_units = plugin_units(root, kind)
    units = list(all_units)
    user_mcp = {}
    if args.respect_claude_settings:
        enabled, disabled, user_mcp = claude_enablement(root)
        if enabled or disabled:
            units = filter_units_by_enablement(units, enabled, disabled)
            print(f"respect-claude-settings: {len(disabled)} disabled plugin(s) excluded "
                  f"({', '.join(sorted(disabled)) or 'none'})")
            if enabled:
                print(f"respect-claude-settings: {len(enabled)} enabled plugin(s) included "
                      f"({', '.join(sorted(enabled))})")
    disc = filter_discovery_to_units(root, kind, disc, units)
    routed = {}
    target_keys = set()
    for pname, sk in units:
        for tk in route(pname, args):
            target_keys.add(tk)
            if not disc["skills"]:
                continue
            if tk == "project":
                try:
                    p = os.path.relpath(sk, target_paths["project"].parent)
                except ValueError:
                    p = str(sk)
            else:
                p = str(sk)
            routed.setdefault(tk, []).append(p)

    deny = [] if args.no_deny else sorted({skill_name(s) for s in disc["hide"]})
    source_skill_names = sorted({skill_name(s) for s in disc["skills"]})
    fragments = {}
    for tk in sorted(target_keys):
        cfg = {}
        paths = list(dict.fromkeys(routed.get(tk, [])))
        if paths:
            cfg["skills"] = {"paths": paths}
        if args.wire_memory:
            cfg["instructions"] = ["AGENTS.md", "~/.claude/memory/memory.md"]
        if deny:
            cfg["permission"] = {"skill": {"*": "allow", **{d: "deny" for d in deny}}}
        if disc["mcp"]:
            cfg["mcp"] = to_opencode_mcp(disc["mcp"])
        if cfg:
            fragments[tk] = cfg

    # User-scope MCP (from ~/.claude/settings.json) is a per-user concern, not a
    # per-project one: it belongs in the user's global OpenCode config and must not
    # be duplicated into every repo's opencode.json. Route it to the global target
    # only, creating a global fragment if this run is otherwise project-scoped.
    if user_mcp:
        gfrag = fragments.setdefault("global", {})
        gmcp = gfrag.setdefault("mcp", {})
        for mname, mcfg in to_opencode_mcp(user_mcp).items():
            gmcp.setdefault(mname, mcfg)
        print(f"respect-claude-settings: {len(user_mcp)} user-scope MCP server(s) -> global only "
              f"({', '.join(sorted(user_mcp))})")

    agent_out_dir = default_agent_out_dir(target_keys or {args.config_target}, args.opencode_agent_dir)

    print(f"source: {root}  ({kind})")
    print(f"resolve: {note}")
    print(f"discovered: {len(disc['skills'])} skills ({len(disc['hide'])} reference-only), "
          f"{len(disc['agents'])} agents, {len(disc['commands'])} commands, {len(disc['mcp'])} MCP server(s)")
    routing = f"config-target={args.config_target}"
    if args.global_plugins:
        routing += f", global={args.global_plugins}"
    if args.project_plugins:
        routing += f", project={args.project_plugins}"
    print(f"plugins: {len(units)}  routing: {routing}")
    if deny:
        print("  deny (reference-only): " + ", ".join(deny))
    elif args.no_deny and disc["hide"]:
        print(f"  --no-deny: all {len(disc['hide'])} reference-only skills left enabled")
    rf, rf_present = rules_file_state(root)
    print("rules file: " + (f"{rf.name} ({'has block' if rf_present else 'no block'})" if rf
                            else "none - would create AGENTS.md"))
    if args.add_resolution_block:
        print("  resolution block: " + ensure_resolution_block(root, False))
    elif not (rf and rf_present):
        print("  resolution block: ABSENT - pass --add-resolution-block to add it")
    for tk, cfg in fragments.items():
        print(f"\n--- {tk} config -> {target_paths[tk]} ---")
        print(json.dumps(cfg, indent=2))

    if not args.apply:
        print("\n[dry-run] nothing written. Re-run with --apply to write the config(s) and generate agents.")
        return 0

    for tk, cfg in fragments.items():
        target = target_paths[tk]
        existing = {}
        if target.exists():
            try:
                existing = json.loads(target.read_text())
            except json.JSONDecodeError:
                print(f"WARN: {target} is not valid JSON - writing a fresh file", file=sys.stderr)
        prune_source_entries(existing, tk, target, root, all_units, source_skill_names)
        merge_opencode(existing, cfg)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")
            print(f"wrote {tk} config: {target}")
        except OSError as e:
            print(f"WARN: could not write {target} ({e}). The {tk} fragment is printed above - apply it manually.",
                  file=sys.stderr)

    if args.add_resolution_block:
        print(ensure_resolution_block(root, True))

    if disc["agents"]:
        agent_dirs = sorted({str(Path(a).parent) for a in disc["agents"]})
        cmd = [sys.executable, str(Path(__file__).resolve().parent / "sync_agents.py"),
               *agent_dirs, "--out-dir", agent_out_dir]
        print("generating agents: " + " ".join(cmd))
        subprocess.run(cmd)

    print("\nNext: open OpenCode and run /skills to verify exposure.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
