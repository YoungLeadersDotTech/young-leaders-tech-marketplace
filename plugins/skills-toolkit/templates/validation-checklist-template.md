# Validation Checklist Template

This template provides standard validation checklist patterns that should be used by all Agent Builder system agents to ensure quality and consistency at each phase or step.

## Standard Validation Protocol Section

```markdown
### 3. Phase/Step Validation Protocol (HIGH PRIORITY)

**RULE**: Cannot advance to next phase/step without completing validation checklist and receiving explicit user confirmation.

**Step Completion Template**:
```
=== [PHASE/STEP NAME] VALIDATION CHECKLIST ===

✓ [Requirement 1 completed]
✓ [Requirement 2 completed]
✓ [Requirement 3 completed]
✓ All [phase/step] objectives satisfied
✓ [Specific validation point for this phase/step]
✓ Next [phase/step] prerequisites confirmed

**User Confirmation Required**:
Please confirm that [Phase/Step N] is complete and satisfactory by responding "CONFIRMED" to proceed to [Phase/Step N+1].

If you need any changes, please specify them now before we advance.
```
```

## Agent-Specific Validation Checklists

### For Agent Creation (agent-builder):

#### Phase Validation Templates:

```markdown
**Phase 1 Validation Checklist**:
```
=== PHASE 1 VALIDATION CHECKLIST ===

✓ Agent role and expertise clearly defined
✓ 3-5 core tasks identified and documented
✓ Target audience specified
✓ Existing agent compatibility assessed
✓ All discovery objectives satisfied
✓ User input captured and validated
✓ Phase 2 prerequisites confirmed

**User Confirmation Required**:
Please confirm that Phase 1 is complete and satisfactory by responding "CONFIRMED" to proceed to Phase 2.

If you need any changes, please specify them now before we advance.
```

**Phase 2 Validation Checklist**:
```
=== PHASE 2 VALIDATION CHECKLIST ===

✓ Tool requirements identified and justified
✓ Template/document creation needs defined
✓ Validation requirements specified
✓ Knowledge/data requirements assessed
✓ All capability objectives satisfied
✓ User input captured and validated
✓ Phase 3 prerequisites confirmed

**User Confirmation Required**:
Please confirm that Phase 2 is complete and satisfactory by responding "CONFIRMED" to proceed to Phase 3.

If you need any changes, please specify them now before we advance.
```

**Phase 3 Validation Checklist**:
```
=== PHASE 3 VALIDATION CHECKLIST ===

✓ Communication style clearly defined
✓ Expertise level specified
✓ Guardrails and restrictions established
✓ Differentiation from other agents confirmed
✓ All personality objectives satisfied
✓ User input captured and validated
✓ Phase 4 prerequisites confirmed

**User Confirmation Required**:
Please confirm that Phase 3 is complete and satisfactory by responding "CONFIRMED" to proceed to Phase 4.

If you need any changes, please specify them now before we advance.
```

**Phase 4 Validation Checklist**:
```
=== PHASE 4 VALIDATION CHECKLIST ===

✓ Deployment option explicitly selected by user
✓ Platform research completed (if applicable)
✓ Output format requirements confirmed
✓ Installation location determined
✓ All deployment objectives satisfied
✓ User input captured and validated
✓ Phase 5 prerequisites confirmed

**User Confirmation Required**:
Please confirm that Phase 4 is complete and satisfactory by responding "CONFIRMED" to proceed to Phase 5.

If you need any changes, please specify them now before we advance.
```

**Phase 5 Validation Checklist**:
```
=== PHASE 5 VALIDATION CHECKLIST ===

✓ Agent draft generated in correct format(s)
✓ Draft clearly presented to user in response
✓ User approval obtained before installation
✓ Structure validation completed
✓ Conflict checking performed
✓ Installation location confirmed
✓ All integration objectives satisfied
✓ User input captured and validated
✓ Installation ready to proceed

**User Confirmation Required**:
Please confirm that Phase 5 is complete and satisfactory by responding "CONFIRMED" to proceed to installation.

If you need any changes, please specify them now before we advance.
```
```

### For Agent Modification (agent-editor):

#### Modification Phase Templates:

```markdown
**Pre-Modification Validation Checklist**:
```
=== PRE-MODIFICATION VALIDATION ===

✓ Target agent file read and analyzed
✓ Current agent purpose and scope documented
✓ Existing tool usage and system prompt structure assessed
✓ Agent Builder Logging section status verified
✓ Modification goals clearly defined
✓ Potential impact on agent ecosystem evaluated
✓ Backup plan and rollback strategy prepared

**User Confirmation Required**:
Please confirm that pre-modification analysis is complete by responding "ANALYSIS CONFIRMED" to proceed.
```

**Planning Phase Validation Checklist**:
```
=== PLANNING PHASE VALIDATION ===

✓ Multiple modification approaches identified and structured
✓ A/B/C options presented with clear consequences
✓ User explicitly selected preferred modification approach
✓ Tool additions/removals planned and justified
✓ System prompt improvements designed for clarity and effectiveness
✓ Agent Builder Logging integration planned (if missing)
✓ Impact on agent's core purpose assessed and approved
✓ Implementation timeline and effort estimated

**User Confirmation Required**:
Please confirm your modification approach selection by responding "PLANNING CONFIRMED" to proceed to implementation.
```

**Implementation Phase Validation Checklist**:
```
=== IMPLEMENTATION PHASE VALIDATION ===

✓ All approved modifications implemented precisely
✓ YAML frontmatter updated correctly (if applicable)
✓ Tool selections implemented and validated
✓ System prompt content refined for improved performance
✓ Agent Builder Logging section added (if was missing)
✓ Formatting and professional quality maintained
✓ Real-time validation performed during implementation
✓ Error recovery protocols available if needed

**User Confirmation Required**:
Please confirm that implementation phase is satisfactory by responding "IMPLEMENTATION CONFIRMED" to proceed to testing.
```

**Post-Modification Validation Checklist**:
```
=== POST-MODIFICATION VALIDATION ===

✓ All modifications maintain agent focus and purpose
✓ Tool selections are appropriate and functional
✓ Description accurately reflects updated capabilities
✓ YAML frontmatter syntax validated and complete
✓ Enhanced Agent Builder standards compliance verified
✓ Integration compatibility with ecosystem confirmed
✓ Modified agent meets autonomous operation requirements

**User Confirmation Required**:
Please confirm that post-modification validation is satisfactory by responding "VALIDATION CONFIRMED".
```
```

### For Agent Validation (agent-validator):

#### Validation Phase Templates:

```markdown
**Structure Validation Checklist**:
```
=== STRUCTURE VALIDATION CHECKLIST ===

✓ YAML frontmatter syntax validated
✓ Required fields present (name, description, tools)
✓ Tools list is valid and appropriate
✓ Agent Builder Logging section present
✓ System prompt structure and completeness verified
✓ File formatting consistency confirmed
✓ No syntax errors or malformed content detected

**Validation Status**: [PASS/FAIL with specific results]
```

**Conflict Detection Checklist**:
```
=== CONFLICT DETECTION CHECKLIST ===

✓ Agent name uniqueness verified across ecosystem
✓ Description differentiation from existing agents confirmed
✓ Functionality overlap assessment completed
✓ Tool compatibility verified
✓ Integration requirements satisfied
✓ No conflicts with existing agent ecosystem detected

**Conflict Status**: [PASS/FAIL with specific results]
```

**Quality Assessment Checklist**:
```
=== QUALITY ASSESSMENT CHECKLIST ===

✓ Single responsibility principle adherence verified
✓ Task* integration assessed (when needed)
✓ Structured choice patterns validated
✓ Phase validation protocols confirmed
✓ Professional system prompt quality verified
✓ Proactive behavior implementation assessed
✓ Automatic documentation capability confirmed
✓ Error recovery procedures validated

**Quality Score**: [X]/10 with detailed breakdown
```
```

### For Agent Installation (agent-installer):

#### Installation Step Templates:

```markdown
**Pre-Installation Validation Checklist**:
```
=== PRE-INSTALLATION VALIDATION ===

Agent File Structure:
✓ Valid YAML frontmatter with required fields
✓ Proper markdown structure and formatting
✓ System prompt completeness and clarity
✓ Tool selection appropriateness and necessity
✓ No syntax errors or malformed content

Compatibility Checks:
✓ Agent name uniqueness verified
✓ Description differentiation confirmed
✓ Tool compatibility with environment verified
✓ Integration requirements satisfied
✓ Quality standards alignment confirmed

Environment Validation:
✓ Target installation directory exists and is writable
✓ User permissions adequate for installation type
✓ No file system conflicts or space limitations
✓ Backup capabilities confirmed for rollback scenarios

**User Confirmation Required**:
Please confirm that pre-installation validation is complete by responding "VALIDATION CONFIRMED" to proceed to installation.
```

**Post-Installation Validation Checklist**:
```
=== POST-INSTALLATION VALIDATION ===

✓ Agent file properly installed at correct location
✓ YAML frontmatter syntax validated
✓ Agent description triggers appropriate auto-invocation
✓ Tool access permissions confirmed
✓ System prompt logic tested with sample inputs
✓ Conflict resolution with existing agents verified
✓ Documentation completeness confirmed

**Installation Status**: [PASS/FAIL with specific results]

**User Confirmation Required**:
Please confirm that installation is satisfactory by responding "INSTALLATION CONFIRMED".
```
```

## Integration Testing Checklist Template

For all agents that perform final integration testing:

```markdown
**Integration Testing Checklist**:
```
=== INTEGRATION TESTING CHECKLIST ===

✓ Agent functionality tested in target environment
✓ Tool access and permissions verified
✓ Automatic invocation triggers working correctly
✓ No conflicts with existing agents detected
✓ Performance within acceptable parameters
✓ Error handling procedures functioning properly
✓ Documentation accuracy verified
✓ User workflow integration confirmed

**Testing Status**: [PASS/FAIL with specific results]

**User Confirmation Required**:
Please confirm that integration testing is satisfactory by responding "TESTING CONFIRMED".

If any tests failed, specific remediation steps will be provided.
```
```

## Usage Guidelines

### When to Use Validation Checklists:
- **ALWAYS** before advancing to next phase/step in multi-step processes
- **ALWAYS** after completing major modifications or changes
- **ALWAYS** before final completion of complex operations
- **ALWAYS** when quality assurance is critical

### Customization Guidelines:

1. **Agent-Specific Items**: Adapt checklist items to match the agent's specific responsibilities
2. **Context-Appropriate Language**: Use terminology that matches the agent's domain
3. **Comprehensive Coverage**: Include all critical validation points for the operation
4. **User-Friendly Format**: Present checklists clearly with visual checkmarks
5. **Clear Next Steps**: Always specify what confirmation is needed to proceed

### Best Practices:

- **Visual Clarity**: Use ✓ checkmarks for completed items
- **Specific Items**: Make each checklist item specific and measurable
- **Logical Order**: Arrange items in order of importance or execution
- **Comprehensive Coverage**: Don't skip important validation points
- **User Engagement**: Require explicit confirmation before proceeding

### Integration Requirements:

- Must integrate with Task* system (validation becomes a tracked task)
- Must integrate with Agent Builder Logging (document validation results)
- Must require explicit user confirmation before proceeding
- Must provide clear guidance for handling validation failures

## Quality Standards:

Each validation checklist should:

- **Be Comprehensive**: Cover all aspects relevant to that phase/step
- **Be Specific**: Items should be clear and measurable
- **Be User-Focused**: Help user understand what has been accomplished
- **Be Actionable**: If items fail, provide clear next steps
- **Be Consistent**: Use same format across all validation points

This validation framework ensures quality and user confidence throughout all Agent Builder processes.