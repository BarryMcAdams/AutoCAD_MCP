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
        current_path = Path(__file__).resolve().parent
        project_markers = [
            '.git',           # Git repository
            'CLAUDE.md',      # Project guidelines
            'PROJECT_TRACKER.md',  # Project tracker
            'pyproject.toml', # Python project file
            'package.json',   # Node.js project
            'requirements.txt', # Python requirements
            'src'             # Source directory
        ]
        
        max_levels = 10
        for _ in range(max_levels):
            if any((current_path / marker).exists() for marker in project_markers):
                return str(current_path)
            
            parent = current_path.parent
            if parent == current_path:
                break
            current_path = parent
        
        return os.getcwd()

    def update_session_handoff(self):
        """Update session_handoff.json with comprehensive context."""
        handoff_path = os.path.join(self.project_root, 'session_handoff.json')
        
        context = {
            'handoff_timestamp': self.timestamp,
            'working_directory': os.getcwd(),
            'current_branch': self._get_git_status().get('current_branch', 'unknown'),
            'project_tracker_version': self._get_project_tracker_version(),
            'active_files': self._get_active_files(),
            'git_status': self._get_git_status()['status'],
            'strategic_insights': self._generate_strategic_insights(),
            'blocking_issues': self._identify_blocking_issues(),
            'roadmap_status': self._get_roadmap_status(),
        }

        with open(handoff_path, 'w', encoding='utf-8') as f:
            json.dump(context, f, indent=4)

    def _get_active_files(self):
        """Get a list of recently modified files."""
        active_files = []
        for root, _, files in os.walk(self.project_root):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    if os.path.getmtime(filepath) > (datetime.now().timestamp() - 86400):
                        active_files.append(filepath)
                except FileNotFoundError:
                    continue
        return active_files

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
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, text=True, cwd=self.project_root)
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'unknown'
            
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
        """Get current roadmap status and milestones."""
        roadmap_paths = [
            os.path.join(self.project_root, 'docs', 'development', 'roadmap.md'),
            os.path.join(self.project_root, 'ROADMAP.md')
        ]
        
        for path in roadmap_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    status_lines = [line for line in lines if '✅' in line or '🔄' in line or '❌' in line]
                    if status_lines:
                        return '\n'.join(status_lines[:5])
                    else:
                        return "Roadmap exists but no status markers found"
            except FileNotFoundError:
                continue
        
        return "No roadmap document found"
    
    def _generate_strategic_insights(self):
        """Generate strategic insights based on project state."""
        insights = []
        active_files = self._get_active_files()
        if len(active_files) > 10:
            insights.append("High development activity - multiple files modified recently")
        elif len(active_files) == 0:
            insights.append("Low development activity - consider reviewing project priorities")
        
        test_files = [f for f in active_files if 'test' in f.lower()]
        if test_files:
            insights.append("Testing activity detected - good development practices observed")
        else:
            insights.append("No recent test file modifications - consider adding tests")
        
        if os.path.exists(os.path.join(self.project_root, 'src')):
            insights.append("Well-structured project with src/ directory organization")
        
        return insights
    
    def _identify_blocking_issues(self):
        """Identify potential blocking issues or risks."""
        issues = []
        git_status = self._get_git_status()
        if git_status.get('status', '').strip():
            issues.append("Uncommitted changes present - may indicate unfinished work")
        
        critical_files = ['PROJECT_TRACKER.md', 'CLAUDE.md']
        for file in critical_files:
            if not os.path.exists(os.path.join(self.project_root, file)):
                issues.append(f"Critical file missing: {file}")
        
        if os.path.exists(os.path.join(self.project_root, 'src')):
            python_files = []
            for root, _, files in os.walk(os.path.join(self.project_root, 'src')):
                python_files.extend([f for f in files if f.endswith('.py')])
            
            if not python_files:
                issues.append("No Python files found in src/ - potential structure issue")
        
        return issues

    def update_project_tracker(self):
        """Update PROJECT_TRACKER.md with handoff details."""
        tracker_path = os.path.join(self.project_root, 'PROJECT_TRACKER.md')
        
        with open(tracker_path, 'a') as f:
            f.write(f"\n\n### Version Increment at {self.timestamp}\n")
            f.write("- **Handoff Performed**\n")
            f.write(f"- Timestamp: {self.timestamp}\n")

    def run(self):
        """Execute full handoff procedure."""
        self.update_session_handoff()
        self.update_project_tracker()
        return True

def main():
    handoff = HandoffCommand()
    handoff.run()
    print("Session handoff completed successfully.")

if __name__ == "__main__":
    main()