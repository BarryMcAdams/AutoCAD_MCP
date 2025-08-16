#!/usr/bin/env python
import codecs
import json
import logging
import os
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Reconfigure stdout to use UTF-8 encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")


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
        project_markers = [".git", "pyproject.toml", "README.md"]

        for _ in range(10):  # Limit search depth
            if any((current_path / marker).exists() for marker in project_markers):
                return str(current_path)
            if current_path.parent == current_path:
                break
            current_path = current_path.parent

        return os.getcwd()  # Fallback

    def read_and_display_session_handoff(self):
        """Reads and displays the content of session_handoff.json."""
        handoff_path = os.path.join(self.project_root, "session_handoff.json")
        try:
            with open(handoff_path, encoding="utf-8") as f:
                context = json.load(f)
        except FileNotFoundError:
            logger.error(
                "Session handoff file not found. "
                "Please run the handoff command at the end of your session."
            )
            return
        except json.JSONDecodeError:
            logger.error("Error: Could not decode the session handoff file. It may be corrupted.")
            return
        except Exception as e:
            logger.error(f"An error occurred while reading the session handoff file: {e}")
            return

        logger.info("--- Session Handoff ---")
        logger.info(f"Handoff Timestamp: {context.get('handoff_timestamp')}")
        logger.info(f"Working Directory: {context.get('working_directory')}")
        logger.info(f"Current Branch: {context.get('current_branch')}")
        logger.info(f"Project Tracker Version: {context.get('project_tracker_version')}")

        logger.info("\n--- Git Status ---")
        git_status = context.get("git_status", "").strip()
        if git_status:
            logger.info("Uncommitted changes detected:")
            logger.info(git_status)
        else:
            logger.info("Working tree clean")

        logger.info("\n--- Active Files (last 24 hours) ---")
        for file_path in context.get("active_files", []):
            logger.info(f"- {file_path}")

        logger.info("\n--- Blocking Issues & Risks ---")
        for issue in context.get("blocking_issues", []):
            logger.info(f"- {issue}")

        logger.info("\n--- Recommended Next Steps ---")
        for step in context.get("recommended_next_steps", []):
            logger.info(f"- {step}")
        logger.info("--- End of Session Handoff ---")

    def run(self):
        """Executes the pickup command workflow."""
        logger.info("Reading session handoff...")
        self.read_and_display_session_handoff()


def main():
    """Main entry point for pickup command."""
    pickup = PickupCommand()
    pickup.run()


if __name__ == "__main__":
    main()
