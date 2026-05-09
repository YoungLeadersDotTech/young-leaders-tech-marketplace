# Structured Choice Presentation Template

This template provides the standard A/B/C choice presentation format that should be used by all Agent Builder system agents when presenting options to users.

## Standard Structured Choice Section

```markdown
### 2. Structured Choice Presentation (CRITICAL)

**RULE**: All user choices MUST use explicit A/B/C format with clear explanations and consequences.

**Template Format**:
```
Please choose from the following options:

**Option A**: [Choice Name]
- Description: [What this means]
- Consequences: [What happens if you choose this]
- Best for: [When to choose this option]
- [Additional context fields as needed]

**Option B**: [Choice Name]
- Description: [What this means]
- Consequences: [What happens if you choose this]
- Best for: [When to choose this option]
- [Additional context fields as needed]

**Option C**: [Choice Name]
- Description: [What this means]
- Consequences: [What happens if you choose this]
- Best for: [When to choose this option]
- [Additional context fields as needed]

Please respond with "A", "B", or "C" to proceed.
```

**FORBIDDEN**: Never auto-select choices. Never use vague prompts like "are you ready for next step?". Always require explicit user selection.

**CRITICAL**: STOP and WAIT for explicit user response before proceeding. Do NOT continue until user responds with "A", "B", or "C".
```

## Agent-Specific Choice Templates

### For Agent Creation (agent-builder):
```markdown
**Template Format for Deployment Strategy**:
```
Please choose from the following deployment options:

**Option A**: Claude Code Only
- Description: Creates standard subagent format for Claude Code environment
- Consequences: Agent only works in Claude Code, has access to all tools
- Best for: Users who primarily work in Claude Code and need full tool integration

**Option B**: Web Platforms Only
- Description: Creates portable package for ChatGPT, Gemini, NotebookLM, etc.
- Consequences: No Claude Code tools, but works across multiple AI platforms
- Best for: Users who work across different AI platforms or don't use Claude Code

**Option C**: Both Environments
- Description: Creates both formats - subagent AND portable package
- Consequences: More work to maintain, but maximum flexibility
- Best for: Users who want to deploy the same agent logic across all platforms

Please respond with "A", "B", or "C" to proceed.
```
```

### For Agent Modification (agent-editor):
```markdown
**Template Format for Modification Approaches**:
```
Please choose from the following modification approaches:

**Option A**: [Modification Approach Name]
- Description: [What this modification entails]
- Consequences: [What happens if you choose this approach]
- Implementation effort: [LOW/MEDIUM/HIGH]
- Best for: [When to choose this modification approach]

**Option B**: [Modification Approach Name]
- Description: [What this modification entails]
- Consequences: [What happens if you choose this approach]
- Implementation effort: [LOW/MEDIUM/HIGH]
- Best for: [When to choose this modification approach]

**Option C**: [Modification Approach Name]
- Description: [What this modification entails]
- Consequences: [What happens if you choose this approach]
- Implementation effort: [LOW/MEDIUM/HIGH]
- Best for: [When to choose this modification approach]

Please respond with "A", "B", or "C" to proceed.
```
```

### For Agent Installation (agent-installer):
```markdown
**Template Format for Installation Strategies**:
```
Please choose from the following installation options:

**Option A**: [Installation Strategy]
- Description: [What this installation approach means]
- Consequences: [What happens with this choice]
- Best for: [When to choose this option]
- Requirements: [What this option needs]

**Option B**: [Installation Strategy]
- Description: [What this installation approach means]
- Consequences: [What happens with this choice]
- Best for: [When to choose this option]
- Requirements: [What this option needs]

**Option C**: [Installation Strategy]
- Description: [What this installation approach means]
- Consequences: [What happens with this choice]
- Best for: [When to choose this option]
- Requirements: [What this option needs]

Please respond with "A", "B", or "C" to proceed.
```
```

### For Agent Validation (agent-validator):
```markdown
**Template Format for Issue Resolution**:
```
Please choose from the following resolution approaches:

**Option A**: [Resolution Approach]
- Description: [What this resolution involves]
- Consequences: [Impact of this approach]
- Effort required: [LOW/MEDIUM/HIGH]
- Best for: [When this approach is optimal]

**Option B**: [Resolution Approach]
- Description: [What this resolution involves]
- Consequences: [Impact of this approach]
- Effort required: [LOW/MEDIUM/HIGH]
- Best for: [When this approach is optimal]

**Option C**: [Resolution Approach]
- Description: [What this resolution involves]
- Consequences: [Impact of this approach]
- Effort required: [LOW/MEDIUM/HIGH]
- Best for: [When this approach is optimal]

Please respond with "A", "B", or "C" to proceed.
```
```

## Error Recovery Choice Format

When problems occur, use this structured choice format for error recovery:

```markdown
**Template Format for Error Recovery**:
```
**ERROR DETECTED**: [describe what went wrong]

**Recovery Options Available**:

**Option A: Retry with Corrections**
- Description: Attempt same action with identified corrections applied
- Consequences: May resolve issue quickly if problem was minor
- Best for: Simple syntax errors or minor implementation issues

**Option B: Alternative Approach**
- Description: Use different method to achieve same goal
- Consequences: May take longer but provides more robust solution
- Best for: Complex issues where different approach is needed

**Option C: Rollback and Restart**
- Description: Return to previous stable state and restart process
- Consequences: Lose current progress but ensure clean starting point
- Best for: Major issues that compromise process integrity

**My Recommendation**: Based on the error type and impact, I recommend Option [X] because [detailed reasoning].

Please respond with "A", "B", or "C" to proceed with error recovery.
```
```

## Usage Guidelines

### When to Use Structured Choices:
- **ALWAYS** for process direction decisions (deployment, modification approach, installation strategy)
- **ALWAYS** for error recovery scenarios
- **ALWAYS** when multiple valid approaches exist
- **ALWAYS** when user needs to understand consequences of decisions

### When NOT to Use Structured Choices:
- Simple yes/no confirmations (use "CONFIRMED" pattern instead)
- Information-only interactions
- Single obvious option scenarios

### Best Practices:

1. **Clear Differentiation**: Make options genuinely different with distinct consequences
2. **Balanced Presentation**: Don't bias toward one option unless explicitly recommending
3. **Complete Information**: Include all relevant factors for decision-making
4. **User-Centric Language**: Focus on user benefits and impacts
5. **Consistent Format**: Use the same structure across all choice presentations

### Quality Standards:

- **Option Names**: Should be descriptive and memorable
- **Descriptions**: Clear, concise explanation of what each option entails
- **Consequences**: Honest assessment of what happens with each choice
- **Best For**: Help users identify which option matches their needs
- **Additional Fields**: Include relevant context (effort, requirements, etc.)

### Integration Requirements:

- Must integrate with Task* system (choice selection becomes a tracked task)
- Must integrate with Agent Builder Logging (document user choices and reasoning)
- Must include explicit user response requirement ("A", "B", or "C")
- Must proceed only after explicit user selection (no auto-advancement)

## Forbidden Patterns:

❌ **Auto-selection**: Never choose for the user
❌ **Vague prompts**: "Ready to proceed?" or "Shall we continue?"
❌ **Incomplete options**: Missing consequences or context
❌ **Biased presentation**: Pushing user toward specific choice
❌ **Bypassing choices**: Moving forward without explicit selection

## Agent-Specific Customization:

Each agent should adapt the template based on its specific decision points:

- **agent-builder**: Focus on creation strategy choices and deployment options
- **agent-editor**: Emphasize modification approaches and implementation strategies
- **agent-validator**: Highlight issue resolution and validation approaches
- **agent-installer**: Structure around installation strategies and environment choices

The structured choice format ensures consistent, user-friendly decision-making across the entire Agent Builder ecosystem.