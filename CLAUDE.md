# Claude AI Project Guidelines

## 🚀 Startup Procedures

### Mandatory Session Initialization

**IMPORTANT**: Before beginning any work in this project:

1. **Review Session Context** - Always read `session_handoff.md` to understand previous session status, completed work, and pending tasks
2. **Review Project Documentation** - Examine the latest documentation in the project folder for a general overview of the codebase and current state
3. **NEVER ADD AUTHORSHIP CREDITS** - Do NOT add any authorship credits anywhere. Remove them when you see them. Credits will be assigned upon production release.

## 🔍 Project Tracking

### Mandatory Project Tracking Procedure

**IMPORTANT**: For ALL work in this project:

1. ALWAYS update the `PROJECT_TRACKER.md` file after completing any task
2. Follow the comprehensive tracking guidelines in the file
3. Use status emojis: 🔴 (PENDING), 🟡 (IN_PROGRESS), 🟢 (COMPLETED)
4. Include:
   - Brief work description
   - Lines of code added/modified
   - Any new dependencies

### Reference Documents
- [PROJECT_TRACKER.md](/PROJECT_TRACKER.md): Comprehensive project tracking document
- [Improvements/Research_Planning.md](/Improvements/Research_Planning.md): Research strategy
- [Improvements/Improvements_Overview.md](/Improvements/Improvements_Overview.md): Project vision

## 🚨 Critical Tracking Rules
- Never delete existing project tracker content
- Always append updates
- Include timestamp with significant changes
- Update version number incrementally

## 🔄 Session Handoff Command

### /handoff Slash Command Specification

#### Purpose
Prepare a comprehensive session handoff for the next AI model, ensuring smooth knowledge transfer and context preservation.

#### Handoff Procedure
When `/handoff` is invoked, the AI MUST:

1. **Prepare Session Documentation**
   - Update `session_handoff.md` with:
     * Current task status
     * Completed work
     * Pending items
     * Context and insights
     * Recommended next steps

2. **Update Tracking Documents**
   - Modify `PROJECT_TRACKER.md`
     * Add detailed entry in Update History
     * Ensure all objectives are current
     * Flag any blocking issues

3. **Roadmap and Planning**
   - Update `ROADMAP.md`
     * Reflect current progress
     * Adjust priorities if needed
     * Note any strategic shifts

4. **Current Context Capture**
   - Create a comprehensive summary of:
     * Current working directory
     * Active files
     * Recent changes
     * Unresolved questions

5. **Clean-up and Preparation**
   - Clear any temporary state
   - Ensure all work is saved
   - Prepare a clean handoff state

#### Handoff Validation Checklist
- [ ] `session_handoff.md` is updated
- [ ] `PROJECT_TRACKER.md` reflects current state
- [ ] `ROADMAP.md` is current
- [ ] All critical information is documented
- [ ] No unsaved work remains

#### Error Handling
If any step fails during handoff:
- Log the error
- Prevent incomplete handoff
- Notify user of specific failure point

**CRITICAL**: The handoff must be atomic - either complete fully or not at all.

## 🔄 Session Pickup Command

### /pickup Slash Command Specification

#### Purpose
Intelligent session startup that gathers project context, analyzes current state, and generates prioritized todo lists for user approval before execution.

#### Pickup Procedure
When `/pickup` is invoked, the AI MUST:

1. **Context Aggregation**
   - Read `session_handoff.md` for previous session context
   - Parse `PROJECT_TRACKER.md` for current objectives and status
   - Review roadmap documents for strategic priorities
   - Analyze improvement plans and research documents
   - Get current git status and recent commits

2. **Intelligent Analysis**
   - Assess project health and current state
   - Identify critical vs. non-critical tasks
   - Determine proper execution order based on dependencies
   - Factor in testing requirements and best practices
   - Apply enterprise development standards

3. **Smart Todo Generation**
   - Create prioritized, actionable todo list with rationale
   - Include testing steps at appropriate intervals
   - Order tasks by criticality and dependencies
   - Add validation checkpoints and time estimates
   - Apply best practices for software development workflow

4. **Approval Workflow**
   - Present generated todo list with detailed rationale
   - Include executive summary and context analysis
   - Wait for explicit user approval before proceeding
   - Allow modifications to the proposed plan

#### Pickup Output Format
- Executive summary of project status
- Context analysis with health indicators
- Prioritized todo list with rationale and time estimates
- Best practices summary
- Clear approval request

#### Integration with Development Workflow
- Critical infrastructure tasks prioritized first
- Testing checkpoints included after code changes  
- Documentation updates scheduled appropriately
- Git workflow considerations factored in
- Enterprise standards and security practices applied

**CRITICAL**: The pickup command generates actionable intelligence but NEVER executes tasks without explicit user approval.

## 📁 File Management Policy

### Non-Destructive Development Rule

**NEVER DELETE ANYTHING** - If something needs to be removed or cleaned up, ALWAYS move it to the DELETED/ folder instead of deleting it.

- Do not delete the DELETED/ folder itself
- If the DELETED/ folder does not exist, create it and ensure it's included in the .gitignore file
- The DELETED/ folder is in .gitignore so GitHub stays clean and organized
- This preserves all historical content while maintaining a tidy repository structure
- Move unnecessary files/folders to DELETED/ to maintain project history