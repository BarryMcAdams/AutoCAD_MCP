# Claude AI Project Guidelines

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