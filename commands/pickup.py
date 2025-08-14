#!/usr/bin/env python3
"""
Simple session pickup script.

Loads the previous session's handoff information into context.
"""

import os
import json
from pathlib import Path
from datetime import datetime


def find_project_root() -> str:
    """Find project root by looking for project markers."""
    current_path = Path(__file__).resolve().parent
    
    project_markers = [
        '.git',
        'CLAUDE.md', 
        'PROJECT_TRACKER.md',
        'pyproject.toml',
        'src'
    ]
    
    max_levels = 10
    for _ in range(max_levels):
        for marker in project_markers:
            marker_path = current_path / marker
            if marker_path.exists():
                return str(current_path)
        
        parent = current_path.parent
        if parent == current_path:
            break
        current_path = parent
    
    return os.getcwd()


def load_session_handoff(project_root: str) -> dict:
    """
    Load previous session handoff information.
    """
    handoff_path = os.path.join(project_root, 'session_handoff.md')
    
    if not os.path.exists(handoff_path):
        return {
            'exists': False,
            'message': 'No previous session handoff found',
            'timestamp': datetime.now().isoformat()
        }
    
    try:
        with open(handoff_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        handoff_info = {
            'exists': True,
            'content': content,
            'path': handoff_path,
            'last_modified': os.path.getmtime(handoff_path),
            'size': os.path.getsize(handoff_path)
        }
        
        # Extract basic metadata
        lines = content.split('\n')
        for line in lines:
            if line.startswith('**Handoff Timestamp**:'):
                handoff_info['session_timestamp'] = line.split(':')[-1].strip()
            elif line.startswith('**Current Branch**:'):
                handoff_info['branch'] = line.split(':')[-1].strip()
        
        return handoff_info
        
    except Exception as e:
        return {
            'exists': False,
            'error': f'Could not read handoff file: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }


def main():
    """
    Main entry point - loads previous session context.
    """
    project_root = find_project_root()
    print(f"Loading session context from: {project_root}")
    
    handoff = load_session_handoff(project_root)
    
    if handoff['exists']:
        print(f"Previous session handoff loaded")
        print(f"  Path: {handoff['path']}")
        print(f"  Size: {handoff['size']} bytes")
        if 'session_timestamp' in handoff:
            print(f"  Session timestamp: {handoff['session_timestamp']}")
        if 'branch' in handoff:
            print(f"  Branch: {handoff['branch']}")
    else:
        print("No previous session handoff found")
        if 'error' in handoff:
            print(f"  Error: {handoff['error']}")
    
    print(f"\nSession context loading complete at {datetime.now().isoformat()}")
    return 0


if __name__ == "__main__":
    exit(main())