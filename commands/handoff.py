import os
import json
from datetime import datetime
from pathlib import Path

class HandoffCommand:
    def __init__(self, project_root=None):
        self.project_root = project_root or self._find_project_root()
        self.timestamp = datetime.now().isoformat()
    
    def _find_project_root(self) -> str:
        """
        Portable project root detection that works across different machines and paths.
        Walks up the directory tree looking for project markers.
        """
        # Start from the current script location
        current_path = Path(__file__).resolve().parent
        
        # Project marker files that indicate we've found the root
        project_markers = [
            '.git',           # Git repository
            'CLAUDE.md',      # Project guidelines
            'PROJECT_TRACKER.md',  # Project tracker
            'pyproject.toml', # Python project file
            'package.json',   # Node.js project
            'requirements.txt', # Python requirements
            'src'             # Source directory
        ]
        
        # Walk up the directory tree
        max_levels = 10  # Prevent infinite loops
        for _ in range(max_levels):
            # Check if any project markers exist in current directory
            for marker in project_markers:
                marker_path = current_path / marker
                if marker_path.exists():
                    return str(current_path)
            
            # Move up one level
            parent = current_path.parent
            if parent == current_path:  # Reached filesystem root
                break
            current_path = parent
        
        # Fallback: use current working directory
        return os.getcwd()

    def update_session_handoff(self):
        """Update session_handoff.md with comprehensive context."""
        handoff_path = os.path.join(self.project_root, 'session_handoff.md')
        
        # Capture comprehensive context
        context = {
            'timestamp': self.timestamp,
            'current_directory': os.getcwd(),
            'active_files': self._get_active_files(),
            'todo_status': self._get_todo_status(),
            'project_tracker_version': self._get_project_tracker_version(),
            'git_status': self._get_git_status(),
            'roadmap_status': self._get_roadmap_status(),
            'strategic_insights': self._generate_strategic_insights(),
            'blocking_issues': self._identify_blocking_issues()
        }

        # Write comprehensive context to session_handoff.md
        with open(handoff_path, 'w', encoding='utf-8') as f:
            f.write(f"# Session Handoff: {datetime.now().strftime('%B %d, %Y')}\n\n")
            
            # Executive Summary
            f.write("## 📋 Executive Summary\n\n")
            f.write(f"**Handoff Timestamp**: {self.timestamp}\n")
            f.write(f"**Working Directory**: `{context['current_directory']}`\n")
            f.write(f"**Current Branch**: {context['git_status'].get('current_branch', 'unknown')}\n")
            f.write(f"**Project Tracker Version**: {context['project_tracker_version']}\n\n")
            
            # Accomplishments
            f.write("## ✅ Session Accomplishments\n\n")
            f.write("### Completed Tasks\n")
            completed_tasks = context['todo_status'].get('completed_tasks', [])
            if completed_tasks:
                for task in completed_tasks:
                    f.write(f"- {task}\n")
            else:
                f.write("- No completed tasks recorded\n")
            f.write("\n")
            
            # Current State
            f.write("## 📊 Current State\n\n")
            f.write("### Active Files\n")
            for file_path in context['active_files']:
                f.write(f"- `{file_path}`\n")
            f.write("\n")
            
            f.write("### Git Status\n")
            if context['git_status'].get('status', '').strip():
                f.write("⚠️ Uncommitted changes detected:\n")
                f.write(f"```\n{context['git_status']['status']}\n```\n")
            else:
                f.write("✅ Working tree clean\n")
            f.write("\n")
            
            # Pending Work
            f.write("## 🔄 Pending Work\n\n")
            pending_tasks = context['todo_status'].get('pending_tasks', [])
            if pending_tasks:
                for task in pending_tasks:
                    f.write(f"- [ ] {task}\n")
            else:
                f.write("- No pending tasks recorded\n")
            f.write("\n")
            
            # Strategic Insights
            f.write("## 🧠 Strategic Insights\n\n")
            for insight in context['strategic_insights']:
                f.write(f"- {insight}\n")
            f.write("\n")
            
            # Blocking Issues
            f.write("## 🚨 Blocking Issues & Risks\n\n")
            if context['blocking_issues']:
                for issue in context['blocking_issues']:
                    f.write(f"- ⚠️ {issue}\n")
            else:
                f.write("- No blocking issues identified\n")
            f.write("\n")
            
            # Next Session Recommendations
            f.write("## 🎯 Recommended Next Steps\n\n")
            recommendations = self._generate_next_steps(context)
            for rec in recommendations:
                f.write(f"1. {rec}\n")
            f.write("\n")
            
            # Roadmap Status
            f.write("## 🗺️ Roadmap Status\n\n")
            f.write(context['roadmap_status'])

    def _get_active_files(self):
        """Get a list of recently modified files."""
        active_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                filepath = os.path.join(root, file)
                # Only track files modified in last 24 hours
                if os.path.getmtime(filepath) > (datetime.now().timestamp() - 86400):
                    active_files.append(filepath)
        return active_files

    def _get_todo_status(self):
        """Retrieve current todo status."""
        # This is a placeholder. In a real implementation, 
        # you'd parse the actual todo tracking mechanism
        return {
            "pending_tasks": [],
            "completed_tasks": []
        }

    def _get_project_tracker_version(self):
        """Get the current project tracker version."""
        tracker_path = os.path.join(self.project_root, 'PROJECT_TRACKER.md')
        try:
            with open(tracker_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('*Project Tracking Version*:'):
                        return line.split(':')[-1].strip()
        except FileNotFoundError:
            return "Unknown"
        return "Unknown"
    
    def _get_git_status(self):
        """Get current git status and branch information."""
        try:
            import subprocess
            
            # Get current branch
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, cwd=self.project_root)
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
            # Get git status
            status_result = subprocess.run(['git', 'status', '--porcelain'], 
                                         capture_output=True, text=True, cwd=self.project_root)
            git_status = status_result.stdout if status_result.returncode == 0 else 'unknown'
            
            return {
                'current_branch': current_branch,
                'status': git_status
            }
        except Exception:
            return {'current_branch': 'unknown', 'status': 'unknown'}
    
    def _get_roadmap_status(self):
        """Get current roadmap status and milestones with phase tracking."""
        roadmap_paths = [
            os.path.join(self.project_root, 'docs', 'development', 'roadmap.md'),
            os.path.join(self.project_root, 'ROADMAP.md')
        ]
        
        for path in roadmap_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract current phase
                    current_phase = "Unknown Phase"
                    phase_status = "Unknown Status"
                    
                    lines = content.split('\n')
                    for line in lines:
                        if 'CURRENT PRIORITY' in line and 'Phase 0' in line:
                            current_phase = "Phase 0: Emergency Foundation Repairs"
                            phase_status = "🔴 CRITICAL - Active"
                        elif 'Current Phase' in line and 'Phase 1' in line:
                            current_phase = "Phase 1: Consolidation and Expansion"
                            phase_status = "🟡 Active"
                    
                    # Extract status markers and completion criteria
                    status_lines = [line for line in lines if '✅' in line or '🔄' in line or '❌' in line or '🔴' in line]
                    completion_criteria = []
                    
                    in_criteria_section = False
                    for line in lines:
                        if 'Phase 0 Completion Criteria' in line:
                            in_criteria_section = True
                            continue
                        elif in_criteria_section and line.startswith('- ✅'):
                            completion_criteria.append(line.strip())
                        elif in_criteria_section and line.startswith('##'):
                            break
                    
                    result = f"**Current Phase**: {current_phase}\n"
                    result += f"**Phase Status**: {phase_status}\n\n"
                    
                    if completion_criteria:
                        result += "**Phase 0 Completion Criteria**:\n"
                        for criterion in completion_criteria:
                            result += f"  {criterion}\n"
                        result += "\n"
                    
                    if status_lines:
                        result += "**Status Indicators**:\n"
                        for status in status_lines[:5]:  # First 5 status items
                            result += f"  {status}\n"
                    
                    return result
                    
            except FileNotFoundError:
                continue
        
        return "No roadmap document found"
    
    def _generate_strategic_insights(self):
        """Generate strategic insights based on project state."""
        insights = []
        
        # Analyze recent file changes
        active_files = self._get_active_files()
        if len(active_files) > 10:
            insights.append("High development activity - multiple files modified recently")
        elif len(active_files) == 0:
            insights.append("Low development activity - consider reviewing project priorities")
        
        # Check for test files
        test_files = [f for f in active_files if 'test' in f.lower()]
        if test_files:
            insights.append("Testing activity detected - good development practices observed")
        else:
            insights.append("No recent test file modifications - consider adding tests")
        
        # Check project structure
        if os.path.exists(os.path.join(self.project_root, 'src')):
            insights.append("Well-structured project with src/ directory organization")
        
        return insights
    
    def _identify_blocking_issues(self):
        """Identify potential blocking issues or risks."""
        issues = []
        
        # Check for uncommitted changes
        git_status = self._get_git_status()
        if git_status.get('status', '').strip():
            issues.append("Uncommitted changes present - may indicate unfinished work")
        
        # Check for missing critical files
        critical_files = ['PROJECT_TRACKER.md', 'CLAUDE.md']
        for file in critical_files:
            if not os.path.exists(os.path.join(self.project_root, file)):
                issues.append(f"Critical file missing: {file}")
        
        # Check for Python import issues (basic check)
        if os.path.exists(os.path.join(self.project_root, 'src')):
            python_files = []
            for root, _, files in os.walk(os.path.join(self.project_root, 'src')):
                python_files.extend([f for f in files if f.endswith('.py')])
            
            if not python_files:
                issues.append("No Python files found in src/ - potential structure issue")
        
        return issues
    
    def _generate_next_steps(self, context):
        """Generate recommended next steps based on context."""
        recommendations = []
        
        # Handle pending tasks
        pending = context['todo_status'].get('pending_tasks', [])
        if pending:
            recommendations.append(f"Complete {len(pending)} pending tasks from previous session")
        
        # Handle blocking issues
        if context['blocking_issues']:
            recommendations.append("Address identified blocking issues before proceeding")
        
        # Handle git status
        if context['git_status'].get('status', '').strip():
            recommendations.append("Review and commit pending changes")
        
        # General recommendations
        recommendations.append("Run /pickup command to generate intelligent action plan")
        recommendations.append("Review PROJECT_TRACKER.md for current objectives")
        
        return recommendations

    def update_project_tracker(self):
        """Update PROJECT_TRACKER.md with handoff details."""
        tracker_path = os.path.join(self.project_root, 'PROJECT_TRACKER.md')
        
        with open(tracker_path, 'a') as f:
            f.write(f"\n\n### Version Increment at {self.timestamp}\n")
            f.write("- **Handoff Performed**\n")
            f.write(f"- Timestamp: {self.timestamp}\n")

    def update_session_todo(self):
        """Update session_todo.md with current development tasks."""
        todo_path = os.path.join(self.project_root, 'session_todo.md')
        
        # Read existing session_todo.md to preserve task content
        existing_content = ""
        if os.path.exists(todo_path):
            try:
                with open(todo_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            except:
                existing_content = ""
        
        # Update the header with current timestamp
        with open(todo_path, 'w', encoding='utf-8') as f:
            if existing_content and "**Generated**:" in existing_content:
                # Update timestamp in existing content
                lines = existing_content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith("**Generated**:"):
                        lines[i] = f"**Generated**: {self.timestamp}"
                        break
                f.write('\n'.join(lines))
            else:
                # Create basic structure if file doesn't exist
                f.write("# Session TODO - Current Development Tasks\n\n")
                f.write(f"**Generated**: {self.timestamp}\n")
                f.write("**Project Phase**: Production Readiness\n")
                f.write(f"**Branch**: {self._get_git_status().get('current_branch', 'unknown')}\n")
                f.write("**Status**: Session Handoff Complete\n\n")
                f.write("## Current Development Tasks\n\n")
                f.write("Please use /pickup command to generate current task priorities.\n\n")
                f.write("---\n*This file maintained by handoff.py/pickup.py scripts for session continuity*")

    def update_roadmap(self):
        """Update ROADMAP.md timestamp and status."""
        roadmap_path = os.path.join(self.project_root, 'ROADMAP.md')
        
        if os.path.exists(roadmap_path):
            try:
                with open(roadmap_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update the "Last Updated" line
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "- **Last Updated**:" in line:
                        lines[i] = f"- **Last Updated**: {datetime.now().strftime('%Y-%m-%d')} (Session Handoff)"
                        break
                
                # Update the footer timestamp
                for i, line in enumerate(lines):
                    if line.startswith("*Roadmap maintained by handoff.py/pickup.py scripts"):
                        lines[i] = f"*Roadmap maintained by handoff.py/pickup.py scripts - Updated: {datetime.now().strftime('%Y-%m-%d')}*"
                        break
                
                with open(roadmap_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
            except Exception as e:
                print(f"Warning: Could not update ROADMAP.md: {e}")

    def run(self):
        """Execute full handoff procedure."""
        self.update_session_handoff()
        self.update_project_tracker()
        self.update_session_todo()
        self.update_roadmap()
        return True

def main():
    handoff = HandoffCommand()
    handoff.run()
    print("Session handoff completed successfully.")

if __name__ == "__main__":
    main()