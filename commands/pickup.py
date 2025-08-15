#!/usr/bin/env python
import os
import sys
import json
import codecs
from datetime import datetime
from pathlib import Path

# Reconfigure stdout to use UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

class PickupCommand:
    """
    Reads the session handoff file and displays the context from the previous session.
    """

    def __init__(self, project_root=None):
        self.project_root = project_root or self._find_project_root()

    def _find_project_root(self) -> str:
        """
        Finds the project root by looking for marker files.
        """
        current_path = Path(__file__).resolve().parent
        project_markers = ['.git', 'pyproject.toml', 'README.md']
        
        for _ in range(10):  # Limit search depth
            if any((current_path / marker).exists() for marker in project_markers):
                return str(current_path)
            if current_path.parent == current_path:
                break
            current_path = current_path.parent
        
        return os.getcwd()  # Fallback

    def read_and_display_session_handoff(self):
        """Reads and displays the content of session_handoff.json."""
        handoff_path = os.path.join(self.project_root, 'session_handoff.json')
        try:
            with open(handoff_path, 'r', encoding='utf-8') as f:
                context = json.load(f)
        except FileNotFoundError:
            print("Session handoff file not found. Please run the handoff command at the end of your session.")
            return
        except json.JSONDecodeError:
            print("Error: Could not decode the session handoff file. It may be corrupted.")
            return
        except Exception as e:
            print(f"An error occurred while reading the session handoff file: {e}")
            return

        print("--- Session Handoff ---")
        print(f"Handoff Timestamp: {context.get('handoff_timestamp')}")
        print(f"Working Directory: {context.get('working_directory')}")
        print(f"Current Branch: {context.get('current_branch')}")
        print(f"Project Tracker Version: {context.get('project_tracker_version')}")
        
        print("\n--- Git Status ---")
        git_status = context.get('git_status', '').strip()
        if git_status:
            print("Uncommitted changes detected:")
            print(git_status)
        else:
            print("Working tree clean")

        print("\n--- Active Files (last 24 hours) ---")
        for file_path in context.get('active_files', []):
            print(f"- {file_path}")

        print("\n--- Blocking Issues & Risks ---")
        for issue in context.get('blocking_issues', []):
            print(f"- {issue}")

        print("\n--- Recommended Next Steps ---")
        for step in context.get('recommended_next_steps', []):
            print(f"- {step}")
        print("--- End of Session Handoff ---")

    def run(self):
        """Executes the pickup command workflow."""
        print("Reading session handoff...")
        self.read_and_display_session_handoff()

def main():
    """Main entry point for pickup command."""
    pickup = PickupCommand()
    pickup.run()

if __name__ == "__main__":
    main()
