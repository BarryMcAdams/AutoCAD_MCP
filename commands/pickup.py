import os
import json
from datetime import datetime
from typing import List, Dict, Any

class PickupCommand:
    """
    Intelligent session startup command that gathers project context,
    analyzes current state, and generates prioritized todo lists for approval.
    """
    
    def __init__(self, project_root=None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.timestamp = datetime.now().isoformat()
        self.context = {}
        self.todos = []
        
    def gather_context(self):
        """Aggregate information from all key project documents."""
        print("Gathering project context...")
        
        # Read session handoff
        self.context['handoff'] = self._read_session_handoff()
        
        # Read project tracker
        self.context['tracker'] = self._read_project_tracker()
        
        # Read roadmap
        self.context['roadmap'] = self._read_roadmap()
        
        # Read improvement documents
        self.context['improvements'] = self._read_improvements()
        
        # Get git status and recent commits
        self.context['git_status'] = self._get_git_status()
        
        return self.context
    
    def _read_session_handoff(self) -> Dict[str, Any]:
        """Parse session_handoff.md for previous session context."""
        handoff_path = os.path.join(self.project_root, 'session_handoff.md')
        try:
            with open(handoff_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return {
                    'exists': True,
                    'content': content,
                    'last_modified': os.path.getmtime(handoff_path)
                }
        except FileNotFoundError:
            return {'exists': False, 'message': 'No previous session handoff found'}
    
    def _read_project_tracker(self) -> Dict[str, Any]:
        """Parse PROJECT_TRACKER.md for current objectives and status."""
        tracker_path = os.path.join(self.project_root, 'PROJECT_TRACKER.md')
        try:
            with open(tracker_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract version
                version = "Unknown"
                for line in content.split('\n'):
                    if '*Project Tracking Version*:' in line:
                        version = line.split(':')[-1].strip()
                        break
                
                return {
                    'exists': True,
                    'content': content,
                    'version': version,
                    'last_modified': os.path.getmtime(tracker_path)
                }
        except FileNotFoundError:
            return {'exists': False, 'message': 'No project tracker found'}
    
    def _read_roadmap(self) -> Dict[str, Any]:
        """Parse roadmap for strategic priorities."""
        roadmap_paths = [
            os.path.join(self.project_root, 'docs', 'development', 'roadmap.md'),
            os.path.join(self.project_root, 'ROADMAP.md')
        ]
        
        for path in roadmap_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return {
                        'exists': True,
                        'content': content,
                        'path': path,
                        'last_modified': os.path.getmtime(path)
                    }
            except FileNotFoundError:
                continue
        
        return {'exists': False, 'message': 'No roadmap found'}
    
    def _read_improvements(self) -> Dict[str, Any]:
        """Parse improvement documents for project vision."""
        improvements_dir = os.path.join(self.project_root, 'Improvements')
        docs = {}
        
        if not os.path.exists(improvements_dir):
            return {'exists': False, 'message': 'No Improvements directory found'}
        
        for filename in ['Improvements_Overview.md', 'Research_Planning.md']:
            filepath = os.path.join(improvements_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    docs[filename] = f.read()
            except FileNotFoundError:
                docs[filename] = None
        
        return {'exists': True, 'documents': docs}
    
    def _get_git_status(self) -> Dict[str, Any]:
        """Get current git status and recent commits."""
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
            
            # Get recent commits
            log_result = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                      capture_output=True, text=True, cwd=self.project_root)
            recent_commits = log_result.stdout if log_result.returncode == 0 else 'unknown'
            
            return {
                'current_branch': current_branch,
                'status': git_status,
                'recent_commits': recent_commits
            }
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_and_prioritize(self) -> List[Dict[str, Any]]:
        """Analyze context and generate prioritized todo list."""
        print("Analyzing project state and generating todos...")
        
        todos = []
        
        # Critical operational tasks first
        if not self.context['handoff']['exists']:
            todos.append({
                'priority': 'CRITICAL',
                'task': 'Create initial session_handoff.md',
                'rationale': 'No handoff document exists - critical for session continuity',
                'category': 'Infrastructure',
                'estimated_time': '5 minutes'
            })
        
        if not self.context['tracker']['exists']:
            todos.append({
                'priority': 'CRITICAL', 
                'task': 'Create PROJECT_TRACKER.md',
                'rationale': 'Project tracking is mandatory per CLAUDE.md guidelines',
                'category': 'Infrastructure',
                'estimated_time': '10 minutes'
            })
        
        # Parse handoff for pending tasks
        if self.context['handoff']['exists']:
            handoff_content = self.context['handoff']['content']
            if 'NumPy deprecation warning' in handoff_content:
                todos.append({
                    'priority': 'HIGH',
                    'task': 'Address NumPy deprecation warning in LSCM algorithm',
                    'rationale': 'Identified in previous session as compatibility risk',
                    'category': 'Bug Fix',
                    'estimated_time': '15 minutes'
                })
            
            if 'Comprehensive Testing Expansion' in handoff_content:
                todos.append({
                    'priority': 'HIGH',
                    'task': 'Execute comprehensive testing expansion plan',
                    'rationale': 'Next major milestone identified in handoff',
                    'category': 'Testing',
                    'estimated_time': '30-60 minutes'
                })
        
        # Check git status for uncommitted changes
        if self.context['git_status'].get('status', '').strip():
            todos.append({
                'priority': 'MEDIUM',
                'task': 'Review and commit pending changes',
                'rationale': 'Uncommitted changes detected - should be resolved',
                'category': 'Version Control',
                'estimated_time': '10 minutes'
            })
        
        # Add validation/testing checkpoints
        if any(t['category'] in ['Bug Fix', 'Implementation'] for t in todos):
            todos.append({
                'priority': 'HIGH',
                'task': 'Run test suite to validate changes',
                'rationale': 'Testing required after code modifications',
                'category': 'Validation',
                'estimated_time': '5-10 minutes'
            })
        
        # Add project tracking update (always last)
        todos.append({
            'priority': 'LOW',
            'task': 'Update PROJECT_TRACKER.md with session progress',
            'rationale': 'Mandatory tracking per project guidelines',
            'category': 'Documentation',
            'estimated_time': '5 minutes'
        })
        
        # Sort by priority
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        todos.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return todos
    
    def present_for_approval(self, todos: List[Dict[str, Any]]) -> str:
        """Format todos for user approval."""
        output = []
        output.append("**INTELLIGENT SESSION PICKUP - TODO ANALYSIS**")
        output.append("=" * 60)
        output.append("")
        
        # Executive Summary
        output.append("## Executive Summary")
        output.append(f"- **Session Timestamp**: {self.timestamp}")
        output.append(f"- **Current Branch**: {self.context['git_status'].get('current_branch', 'unknown')}")
        output.append(f"- **Project Tracker Version**: {self.context['tracker'].get('version', 'Unknown')}")
        output.append(f"- **Total Proposed Tasks**: {len(todos)}")
        output.append("")
        
        # Context Summary
        output.append("## Context Analysis")
        if self.context['handoff']['exists']:
            output.append("+ Previous session handoff found")
        else:
            output.append("- No previous session handoff")
            
        if self.context['tracker']['exists']:
            output.append("+ Project tracker available")
        else:
            output.append("- Project tracker missing")
            
        git_clean = not self.context['git_status'].get('status', '').strip()
        if git_clean:
            output.append("+ Git working tree clean")
        else:
            output.append("- Uncommitted changes detected")
        output.append("")
        
        # Prioritized Todo List
        output.append("## Proposed Action Plan")
        output.append("")
        
        for i, todo in enumerate(todos, 1):
            priority_symbol = {
                'CRITICAL': '[!]',
                'HIGH': '[H]', 
                'MEDIUM': '[M]',
                'LOW': '[L]'
            }.get(todo['priority'], '[?]')
            
            output.append(f"### {i}. {priority_symbol} {todo['task']}")
            output.append(f"   - **Priority**: {todo['priority']}")
            output.append(f"   - **Category**: {todo['category']}")
            output.append(f"   - **Estimated Time**: {todo['estimated_time']}")
            output.append(f"   - **Rationale**: {todo['rationale']}")
            output.append("")
        
        # Best Practices Summary
        output.append("## Best Practices Applied")
        output.append("- Critical infrastructure tasks prioritized first")
        output.append("- Testing checkpoints included after code changes")
        output.append("- Documentation updates scheduled appropriately")
        output.append("- Git workflow considerations factored in")
        output.append("- Time estimates provided for planning")
        output.append("")
        
        output.append("**Please review and approve this action plan to proceed.**")
        
        return "\n".join(output)
    
    def run(self) -> str:
        """Execute the pickup command workflow."""
        try:
            # Gather all context
            self.gather_context()
            
            # Generate intelligent todos
            todos = self.analyze_and_prioritize()
            
            # Present for approval
            presentation = self.present_for_approval(todos)
            
            # Store todos for later execution
            self.todos = todos
            
            return presentation
            
        except Exception as e:
            return f"Error during pickup: {str(e)}"
    
    def get_approved_todos(self) -> List[Dict[str, Any]]:
        """Return the generated todos for execution after approval."""
        return self.todos

def main():
    """Main entry point for pickup command."""
    pickup = PickupCommand()
    result = pickup.run()
    
    # Handle Unicode encoding for Windows console
    try:
        print(result.encode('utf-8').decode('cp1252', errors='replace'))
    except (UnicodeDecodeError, UnicodeEncodeError):
        # Fallback: remove Unicode characters
        import re
        clean_result = re.sub(r'[^\x00-\x7F]+', '?', result)
        print(clean_result)
    
    # In a real implementation, this would wait for user approval
    # and then execute the approved todos
    
    return pickup.get_approved_todos()

if __name__ == "__main__":
    main()