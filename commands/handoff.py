import os
import json
from datetime import datetime

class HandoffCommand:
    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.timestamp = datetime.now().isoformat()

    def update_session_handoff(self):
        """Update session_handoff.md with current context."""
        handoff_path = os.path.join(self.project_root, 'session_handoff.md')
        
        # Capture current context
        context = {
            'timestamp': self.timestamp,
            'current_directory': os.getcwd(),
            'active_files': self._get_active_files(),
            'todo_status': self._get_todo_status(),
            'project_tracker_version': self._get_project_tracker_version()
        }

        # Write context to session_handoff.md
        with open(handoff_path, 'w') as f:
            f.write("# Session Handoff\n\n")
            f.write(f"## Handoff Timestamp: {self.timestamp}\n\n")
            f.write("### Current Project Context\n\n")
            f.write(f"- **Working Directory**: `{context['current_directory']}`\n")
            f.write("- **Active Files**:\n")
            for file in context['active_files']:
                f.write(f"  - `{file}`\n")
            f.write("\n### Todo Status\n")
            f.write(json.dumps(context['todo_status'], indent=2))
            f.write(f"\n\n### Project Tracker Version: {context['project_tracker_version']}")

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
            with open(tracker_path, 'r') as f:
                for line in f:
                    if line.startswith('*Project Tracking Version*:'):
                        return line.split(':')[-1].strip()
        except FileNotFoundError:
            return "Unknown"
        return "Unknown"

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