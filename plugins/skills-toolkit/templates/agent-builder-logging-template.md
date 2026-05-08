# Agent Builder Logging Template

This template provides the standard Agent Builder Logging configuration that should be included in all Agent Builder system agents.

## Standard Agent Builder Logging Section

```markdown
## Agent Builder Logging

**AGENT_LOGGING: true** (set to false to disable)

When AGENT_LOGGING is enabled, automatically log task progress to help improve the Agent Builder system:

- **Log file**: `$(date +%Y-%m-%d)-agent-builder-log-{agent-name}.txt` in working directory root
- **Content**: Task completion status, operation results, and key decision points
- **Format**: Timestamped entries with agent name and task description

After completing each Task* task, append log entry:
```
================================================================================
[$(date)] Agent: {agent-name} | Task: {task-description} | Status: COMPLETED
================================================================================
{relevant task output, terminal results, or error messages}
================================================================================
```
```

## Usage Instructions

### For Agent Creation/Modification:
1. Replace `{agent-name}` with the actual agent name (e.g., `agent-builder`, `agent-editor`)
2. Include this section in the agent's system prompt after the core expertise sections
3. Ensure logging is automatically triggered after Task* task completion

### For Conversation/Process Logging:
For agents that manage complex multi-phase processes (like agent-builder), also include:

```markdown
### Automatic Process Logging Protocol (MANDATORY)

**RULE**: Must automatically maintain comprehensive process logs and decision documentation without user requests.

**Auto-Logging Requirements**:

1. **Phase Completion Logging** - After completing each phase, automatically append to log:
```bash
# Auto-execute after each phase completion:
echo "================================================================================" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
echo "[$(date)] PHASE COMPLETED | Agent: {agent-name} | Phase: [N] - [Phase Name]" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
echo "================================================================================" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
echo "User Decisions: [summarize key user choices and reasoning]" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
echo "Phase Outcomes: [summarize what was accomplished]" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt" 
echo "Next Steps: [what happens in next phase]" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
echo "================================================================================" >> "$(date +%Y-%m-%d)-agent-builder-conversation-log.txt"
```

2. **Decision Point Logging** - Immediately after user makes choices, automatically document:
   - What choice was presented (A/B/C options)
   - Which option user selected
   - User's reasoning (if provided)
   - Implications of the choice for the process

3. **Error Recovery Logging** - When problems occur, automatically document:
   - What went wrong
   - Recovery options presented to user
   - User's selected recovery approach
   - Resolution outcome
```

## Integration Notes

- This logging system helps improve the Agent Builder by tracking:
  - Task completion patterns and success rates
  - Common user decision points and preferences
  - Error patterns and effective recovery strategies
  - Phase progression timing and efficiency
  - Overall system performance and user satisfaction

- Agents should implement logging automatically without requiring user setup or requests
- Log files are created in the working directory root for easy access and analysis
- Timestamps enable correlation of agent activities across the ecosystem