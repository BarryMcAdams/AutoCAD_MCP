import os
import json
import ast
import re
from datetime import datetime
from typing import List, Dict, Any, Set, Tuple
from pathlib import Path

class PickupCommand:
    """
    Intelligent session startup command that gathers project context,
    analyzes current state, and generates prioritized todo lists for approval.
    """
    
    def __init__(self, project_root=None):
        self.project_root = project_root or self._find_project_root()
        self.timestamp = datetime.now().isoformat()
        self.context = {}
        self.todos = []
    
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
        
        # Deep codebase analysis
        self.context['codebase_analysis'] = self._analyze_codebase()
        
        # Project phase and maturity assessment
        self.context['project_phase'] = self._assess_project_phase()
        
        # Technical debt and quality assessment
        self.context['quality_assessment'] = self._assess_code_quality()
        
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
        """Parse roadmap for strategic priorities and current phase tracking."""
        roadmap_paths = [
            os.path.join(self.project_root, 'docs', 'development', 'roadmap.md'),
            os.path.join(self.project_root, 'ROADMAP.md')
        ]
        
        for path in roadmap_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract current phase and completion status
                    phase_info = self._extract_roadmap_phase(content)
                    completion_criteria = self._extract_completion_criteria(content)
                    
                    return {
                        'exists': True,
                        'content': content,
                        'path': path,
                        'last_modified': os.path.getmtime(path),
                        'current_phase': phase_info,
                        'completion_criteria': completion_criteria
                    }
            except FileNotFoundError:
                continue
        
        return {'exists': False, 'message': 'No roadmap found'}
    
    def _extract_roadmap_phase(self, content: str) -> Dict[str, Any]:
        """Extract current phase information from roadmap content."""
        lines = content.split('\n')
        current_phase = 'unknown'
        phase_status = 'unknown'
        
        for line in lines:
            if 'CURRENT PRIORITY' in line and 'Phase 0' in line:
                current_phase = 'Phase 0: Emergency Foundation Repairs'
                phase_status = 'critical'
            elif 'Current Phase' in line and 'Phase 1' in line:
                current_phase = 'Phase 1: Consolidation and Expansion'
                phase_status = 'active'
            elif 'Phase 2' in line:
                current_phase = 'Phase 2: Advanced AI Integration'
                phase_status = 'planned'
        
        return {
            'phase': current_phase,
            'status': phase_status
        }
    
    def _extract_completion_criteria(self, content: str) -> List[str]:
        """Extract completion criteria from roadmap."""
        criteria = []
        lines = content.split('\n')
        in_criteria_section = False
        
        for line in lines:
            if 'Phase 0 Completion Criteria' in line:
                in_criteria_section = True
                continue
            elif in_criteria_section and line.startswith('- ✅'):
                criteria.append(line.strip())
            elif in_criteria_section and line.startswith('##'):
                break
                
        return criteria
    
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
    
    def _analyze_codebase(self) -> Dict[str, Any]:
        """Perform comprehensive codebase analysis."""
        analysis = {
            'python_files': [],
            'incomplete_implementations': [],
            'todo_comments': [],
            'import_dependencies': {},
            'class_structures': {},
            'test_coverage': {},
            'recent_changes_impact': []
        }
        
        # Find all Python files
        src_dir = os.path.join(self.project_root, 'src')
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        analysis['python_files'].append(filepath)
                        
                        # Analyze each Python file
                        file_analysis = self._analyze_python_file(filepath)
                        analysis['incomplete_implementations'].extend(file_analysis['incomplete'])
                        analysis['todo_comments'].extend(file_analysis['todos'])
                        analysis['import_dependencies'][filepath] = file_analysis['imports']
                        analysis['class_structures'][filepath] = file_analysis['classes']
        
        # Analyze recent changes impact
        analysis['recent_changes_impact'] = self._analyze_recent_changes()
        
        # Check test coverage
        analysis['test_coverage'] = self._assess_test_coverage()
        
        return analysis
    
    def _analyze_python_file(self, filepath: str) -> Dict[str, Any]:
        """Deep analysis of individual Python file."""
        result = {
            'incomplete': [],
            'todos': [],
            'imports': [],
            'classes': [],
            'functions': [],
            'complexity_issues': []
        }
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST for structural analysis
            try:
                tree = ast.parse(content)
                
                # Analyze imports
                for node in ast.walk(tree):
                    if isinstance(node, (ast.Import, ast.ImportFrom)):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                result['imports'].append(alias.name)
                        else:
                            result['imports'].append(node.module)
                    
                    # Analyze classes and methods
                    elif isinstance(node, ast.ClassDef):
                        class_info = {
                            'name': node.name,
                            'methods': [],
                            'line': node.lineno
                        }
                        for item in node.body:
                            if isinstance(item, ast.FunctionDef):
                                class_info['methods'].append(item.name)
                        result['classes'].append(class_info)
                    
                    # Analyze standalone functions
                    elif isinstance(node, ast.FunctionDef) and not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                        result['functions'].append({
                            'name': node.name,
                            'line': node.lineno,
                            'args': len(node.args.args)
                        })
            
            except SyntaxError:
                result['complexity_issues'].append("Syntax error in file")
            
            # Find TODO comments and incomplete implementations
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line_lower = line.lower().strip()
                
                # TODO comments
                if 'todo' in line_lower or 'fixme' in line_lower:
                    result['todos'].append({
                        'file': filepath,
                        'line': i,
                        'content': line.strip()
                    })
                
                # Incomplete implementations
                if any(marker in line_lower for marker in ['pass', 'not implemented', 'placeholder', '# stub']):
                    result['incomplete'].append({
                        'file': filepath,
                        'line': i,
                        'content': line.strip(),
                        'type': 'incomplete_implementation'
                    })
        
        except Exception as e:
            result['complexity_issues'].append(f"Error analyzing file: {str(e)}")
        
        return result
    
    def _analyze_recent_changes(self) -> List[Dict[str, Any]]:
        """Analyze the impact of recent changes."""
        impacts = []
        
        try:
            import subprocess
            
            # Get recently changed files
            result = subprocess.run(['git', 'diff', '--name-only', 'HEAD~5..HEAD'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                changed_files = result.stdout.strip().split('\n')
                
                for file_path in changed_files:
                    if file_path and file_path.endswith('.py'):
                        full_path = os.path.join(self.project_root, file_path)
                        if os.path.exists(full_path):
                            # Analyze what changed
                            diff_result = subprocess.run(['git', 'diff', 'HEAD~5..HEAD', '--', file_path],
                                                       capture_output=True, text=True, cwd=self.project_root)
                            
                            if diff_result.returncode == 0:
                                diff_content = diff_result.stdout
                                
                                # Classify type of changes
                                change_type = self._classify_change_type(diff_content)
                                impacts.append({
                                    'file': file_path,
                                    'change_type': change_type,
                                    'requires_testing': change_type in ['new_feature', 'bug_fix', 'refactor'],
                                    'requires_documentation': change_type in ['new_feature', 'api_change']
                                })
        
        except Exception as e:
            impacts.append({'error': f"Could not analyze recent changes: {str(e)}"})
        
        return impacts
    
    def _classify_change_type(self, diff_content: str) -> str:
        """Classify the type of change based on diff content."""
        diff_lower = diff_content.lower()
        
        if 'def ' in diff_content and '+' in diff_content:
            return 'new_feature'
        elif 'class ' in diff_content and '+' in diff_content:
            return 'new_class'
        elif 'test' in diff_lower and '+' in diff_content:
            return 'test_addition'
        elif 'fix' in diff_lower or 'bug' in diff_lower:
            return 'bug_fix'
        elif 'refactor' in diff_lower or ('def ' in diff_content and '-' in diff_content):
            return 'refactor'
        elif 'import' in diff_content:
            return 'dependency_change'
        else:
            return 'general_modification'
    
    def _assess_test_coverage(self) -> Dict[str, Any]:
        """Assess current test coverage and gaps."""
        coverage = {
            'test_files': [],
            'untested_modules': [],
            'test_quality': 'unknown'
        }
        
        # Find test files
        for root, _, files in os.walk(self.project_root):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    coverage['test_files'].append(os.path.join(root, file))
        
        # Find source files without corresponding tests
        src_dir = os.path.join(self.project_root, 'src')
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        module_name = file[:-3]  # Remove .py
                        test_file_name = f"test_{module_name}.py"
                        
                        # Check if corresponding test exists
                        test_exists = any(test_file_name in test_path for test_path in coverage['test_files'])
                        if not test_exists:
                            coverage['untested_modules'].append(file)
        
        # Assess test quality
        if len(coverage['test_files']) == 0:
            coverage['test_quality'] = 'none'
        elif len(coverage['untested_modules']) > len(coverage['test_files']):
            coverage['test_quality'] = 'poor'
        elif len(coverage['untested_modules']) > 0:
            coverage['test_quality'] = 'partial'
        else:
            coverage['test_quality'] = 'good'
        
        return coverage
    
    def _assess_project_phase(self) -> Dict[str, Any]:
        """Determine current project phase and maturity."""
        phase_info = {
            'phase': 'unknown',
            'maturity': 'unknown',
            'next_logical_steps': [],
            'blockers': []
        }
        
        # Analyze project structure to determine phase
        has_src = os.path.exists(os.path.join(self.project_root, 'src'))
        try:
            has_tests = any('test' in f for f in os.listdir(self.project_root) if os.path.isfile(os.path.join(self.project_root, f)))
        except (OSError, FileNotFoundError):
            has_tests = False
            
        has_docs = os.path.exists(os.path.join(self.project_root, 'docs'))
        
        has_server = False
        src_path = os.path.join(self.project_root, 'src')
        if os.path.exists(src_path):
            try:
                has_server = any('server.py' in f for f in os.listdir(src_path))
            except (OSError, FileNotFoundError):
                has_server = False
        
        # Determine phase
        if not has_src:
            phase_info['phase'] = 'initialization'
            phase_info['maturity'] = 'early'
        elif has_src and not has_tests:
            phase_info['phase'] = 'development'
            phase_info['maturity'] = 'early'
        elif has_src and has_tests and not has_docs:
            phase_info['phase'] = 'development'
            phase_info['maturity'] = 'mid'
        elif has_src and has_tests and has_docs:
            phase_info['phase'] = 'mature_development'
            phase_info['maturity'] = 'high'
        
        # Parse session handoff for phase indicators
        if self.context.get('handoff', {}).get('exists', False):
            handoff_content = self.context['handoff']['content'].lower()
            if 'testing expansion' in handoff_content:
                phase_info['phase'] = 'testing_expansion'
            elif 'enterprise' in handoff_content:
                phase_info['phase'] = 'enterprise_scaling'
            elif 'algorithm' in handoff_content:
                phase_info['phase'] = 'algorithm_development'
        
        return phase_info
    
    def _assess_code_quality(self) -> Dict[str, Any]:
        """Comprehensive code quality and technical debt assessment."""
        quality = {
            'technical_debt': [],
            'security_issues': [],
            'maintainability_score': 'unknown',
            'architecture_issues': [],
            'best_practice_violations': []
        }
        
        # Check for common technical debt indicators
        src_dir = os.path.join(self.project_root, 'src')
        if os.path.exists(src_dir):
            for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()
                                
                            # Check for technical debt patterns
                            if 'hack' in content.lower() or 'quick fix' in content.lower():
                                quality['technical_debt'].append(f"Hack/quick fix detected in {file}")
                            
                            if 'hardcoded' in content.lower():
                                quality['technical_debt'].append(f"Hardcoded values in {file}")
                            
                            # Check for security issues
                            if 'eval(' in content or 'exec(' in content:
                                quality['security_issues'].append(f"Dangerous eval/exec in {file}")
                            
                            if 'password' in content.lower() and '=' in content:
                                quality['security_issues'].append(f"Potential hardcoded password in {file}")
                            
                            # Check for long functions (>50 lines)
                            lines = content.split('\n')
                            in_function = False
                            function_line_count = 0
                            current_function = ""
                            
                            for line in lines:
                                if line.strip().startswith('def '):
                                    if in_function and function_line_count > 50:
                                        quality['maintainability_score'] = 'needs_improvement'
                                        quality['architecture_issues'].append(f"Long function {current_function} in {file}")
                                    
                                    in_function = True
                                    function_line_count = 0
                                    current_function = line.strip()
                                elif in_function:
                                    if line.strip() and not line.startswith(' '):
                                        in_function = False
                                    else:
                                        function_line_count += 1
                        
                        except Exception:
                            continue
        
        # Set overall maintainability score
        total_issues = len(quality['technical_debt']) + len(quality['security_issues']) + len(quality['architecture_issues'])
        if total_issues == 0:
            quality['maintainability_score'] = 'excellent'
        elif total_issues < 3:
            quality['maintainability_score'] = 'good'
        elif total_issues < 7:
            quality['maintainability_score'] = 'fair'
        else:
            quality['maintainability_score'] = 'needs_improvement'
        
        return quality
    
    def analyze_and_prioritize(self) -> List[Dict[str, Any]]:
        """Masterful analysis and ultra-detailed todo generation using TRUTH and wisdom."""
        print("Performing comprehensive analysis and generating masterful todos...")
        
        todos = []
        
        # Get analysis data
        codebase = self.context.get('codebase_analysis', {})
        quality = self.context.get('quality_assessment', {})
        phase = self.context.get('project_phase', {})
        
        # PRINCIPLE 1: "FINISH WHAT YOU STARTED" - Incomplete work first
        incomplete_items = codebase.get('incomplete_implementations', [])
        if incomplete_items:
            for item in incomplete_items[:3]:  # Top 3 incomplete items
                todos.append({
                    'priority': 'CRITICAL',
                    'task': f"Complete implementation in {os.path.basename(item['file'])}:{item['line']}",
                    'rationale': f"Incomplete implementation: '{item['content']}'. TRUTH: Unfinished code is technical debt that compounds daily.",
                    'category': 'Implementation',
                    'estimated_time': '20-45 minutes',
                    'wisdom': 'Finish what you started before beginning new work',
                    'file_location': f"{item['file']}:{item['line']}"
                })
        
        # PRINCIPLE 2: "ADDRESS CRITICAL FLAWS IMMEDIATELY" - Quality issues
        security_issues = quality.get('security_issues', [])
        if security_issues:
            for issue in security_issues:
                todos.append({
                    'priority': 'CRITICAL',
                    'task': f"Fix security vulnerability: {issue}",
                    'rationale': "TRUTH: Security vulnerabilities are project-killing risks that must be eliminated immediately.",
                    'category': 'Security',
                    'estimated_time': '30-60 minutes',
                    'wisdom': 'Security is not negotiable in professional development'
                })
        
        # PRINCIPLE 3: "VALIDATE RECENT CHANGES" - Test what was changed
        recent_changes = codebase.get('recent_changes_impact', [])
        changes_needing_tests = [c for c in recent_changes if c.get('requires_testing', False)]
        if changes_needing_tests:
            todos.append({
                'priority': 'HIGH',
                'task': f"Create comprehensive tests for recently modified components",
                'rationale': f"TRUTH: {len(changes_needing_tests)} recent changes require validation. Untested changes are landmines.",
                'category': 'Testing',
                'estimated_time': '45-90 minutes',
                'wisdom': 'Test immediately after implementation while context is fresh',
                'details': [f"- Test {c['file']} ({c['change_type']})" for c in changes_needing_tests[:5]]
            })
        
        # PRINCIPLE 4: "TODO COMMENTS ARE COMMITMENTS" - Honor your promises
        todo_comments = codebase.get('todo_comments', [])
        if todo_comments:
            high_priority_todos = [t for t in todo_comments if any(word in t['content'].lower() 
                                                                 for word in ['urgent', 'critical', 'fix', 'bug'])]
            if high_priority_todos:
                for todo in high_priority_todos[:2]:  # Top 2 urgent TODOs
                    todos.append({
                        'priority': 'HIGH',
                        'task': f"Resolve urgent TODO in {os.path.basename(todo['file'])}:{todo['line']}",
                        'rationale': f"TODO comment: '{todo['content']}'. TRUTH: TODO comments are technical debt disguised as good intentions.",
                        'category': 'Technical Debt',
                        'estimated_time': '15-30 minutes',
                        'wisdom': 'TODO comments should have expiration dates',
                        'file_location': f"{todo['file']}:{todo['line']}"
                    })
        
        # PRINCIPLE 5: "TESTING IS INSURANCE" - Address coverage gaps
        test_coverage = codebase.get('test_coverage', {})
        untested_modules = test_coverage.get('untested_modules', [])
        if len(untested_modules) > 0:
            critical_modules = [m for m in untested_modules if 'server' in m or 'main' in m or 'core' in m]
            if critical_modules:
                todos.append({
                    'priority': 'HIGH',
                    'task': f"Create test suite for critical untested modules: {', '.join(critical_modules[:3])}",
                    'rationale': f"TRUTH: {len(untested_modules)} modules lack tests. Critical modules without tests are organizational risk.",
                    'category': 'Testing',
                    'estimated_time': '60-120 minutes',
                    'wisdom': 'Test critical paths first - they break the most and cost the most'
                })
        
        # PRINCIPLE 6: "PARSE HANDOFF INTELLIGENCE" - Honor previous session insights
        if self.context['handoff']['exists']:
            handoff_content = self.context['handoff']['content']
            
            # Look for specific next steps
            if 'NumPy deprecation warning' in handoff_content:
                todos.append({
                    'priority': 'MEDIUM',
                    'task': 'Resolve NumPy deprecation warning in LSCM algorithm',
                    'rationale': 'Previous session identified compatibility risk. TRUTH: Deprecation warnings become breaking changes.',
                    'category': 'Maintenance',
                    'estimated_time': '20-30 minutes',
                    'wisdom': 'Address deprecation warnings before they become forced upgrades'
                })
            
            if 'Comprehensive Testing Expansion' in handoff_content:
                todos.append({
                    'priority': 'HIGH',
                    'task': 'Execute comprehensive testing expansion plan per previous session',
                    'rationale': 'Previous session identified this as the next major milestone. TRUTH: Testing expansion is project maturity.',
                    'category': 'Testing',
                    'estimated_time': '90-150 minutes',
                    'wisdom': 'Testing expansion should happen in phases, not all at once'
                })
        
        # ROADMAP ALIGNMENT CHECK - Ensure todos align with current roadmap phase
        roadmap = self.context.get('roadmap', {})
        if roadmap.get('exists', False):
            current_phase = roadmap.get('current_phase', {})
            if current_phase.get('status') == 'critical':
                # Prioritize Phase 0 critical blockers
                todos.append({
                    'priority': 'CRITICAL',
                    'task': 'Complete Phase 0 roadmap requirements before proceeding',
                    'rationale': f"ROADMAP ALIGNMENT: {current_phase.get('phase', 'Unknown')} is active. TRUTH: Phase completion prevents scope creep.",
                    'category': 'Roadmap Compliance',
                    'estimated_time': '30-60 minutes',
                    'wisdom': 'Complete current phase fully before advancing to next phase'
                })
        
        # PRINCIPLE 7: "ARCHITECTURE BEFORE FEATURES" - Fix structural issues
        architecture_issues = quality.get('architecture_issues', [])
        if architecture_issues:
            todos.append({
                'priority': 'MEDIUM',
                'task': 'Refactor architectural issues to improve maintainability',
                'rationale': f"TRUTH: {len(architecture_issues)} structural issues compound complexity. Fix architecture before adding features.",
                'category': 'Refactoring',
                'estimated_time': '45-90 minutes',
                'wisdom': 'Clean architecture is the foundation of sustainable development',
                'details': architecture_issues[:3]
            })
        
        # PRINCIPLE 8: "DOCUMENT DECISIONS" - Capture architectural wisdom
        recent_feature_changes = [c for c in recent_changes if c.get('change_type') == 'new_feature']
        if recent_feature_changes and not any(c.get('requires_documentation', False) for c in recent_changes):
            todos.append({
                'priority': 'MEDIUM',
                'task': 'Document new features and architectural decisions',
                'rationale': f"TRUTH: {len(recent_feature_changes)} new features lack documentation. Undocumented code is unmaintainable code.",
                'category': 'Documentation',
                'estimated_time': '30-45 minutes',
                'wisdom': 'Document the WHY, not just the WHAT'
            })
        
        # PRINCIPLE 9: "VALIDATE INTEGRATION" - Ensure components work together
        if phase.get('phase') in ['mature_development', 'enterprise_scaling']:
            todos.append({
                'priority': 'HIGH',
                'task': 'Run comprehensive integration tests to validate system cohesion',
                'rationale': f"Project phase: {phase.get('phase')}. TRUTH: Mature projects require integration validation.",
                'category': 'Integration Testing',
                'estimated_time': '30-60 minutes',
                'wisdom': 'Integration bugs are exponentially more expensive than unit bugs'
            })
        
        # PRINCIPLE 10: "HONOR THE PHASE" - Phase-appropriate tasks
        current_phase = phase.get('phase', 'unknown')
        if current_phase == 'testing_expansion':
            todos.append({
                'priority': 'HIGH',
                'task': 'Implement enterprise-grade testing framework expansion',
                'rationale': 'Project is in testing expansion phase. TRUTH: Testing phases require focus and completion.',
                'category': 'Testing Framework',
                'estimated_time': '120-180 minutes',
                'wisdom': 'Complete each development phase fully before moving to the next'
            })
        elif current_phase == 'algorithm_development':
            todos.append({
                'priority': 'HIGH',
                'task': 'Validate and optimize algorithmic implementations',
                'rationale': 'Project is in algorithm development phase. TRUTH: Algorithms require mathematical validation.',
                'category': 'Algorithm Validation',
                'estimated_time': '60-120 minutes',
                'wisdom': 'Algorithmic correctness is more important than algorithmic optimization'
            })
        
        # Always end with project tracking (PRINCIPLE 11: "MEASURE WHAT MATTERS")
        todos.append({
            'priority': 'LOW',
            'task': 'Update PROJECT_TRACKER.md with detailed session progress and insights',
            'rationale': 'TRUTH: What gets measured gets managed. Session handoff requires comprehensive tracking.',
            'category': 'Project Management',
            'estimated_time': '10-15 minutes',
            'wisdom': 'Tracking is the foundation of continuous improvement'
        })
        
        # WISDOM-BASED SORTING: Critical flaws first, then incomplete work, then testing, then features
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        category_order = {
            'Security': 0, 'Implementation': 1, 'Testing': 2, 'Technical Debt': 3,
            'Integration Testing': 4, 'Bug Fix': 5, 'Refactoring': 6, 'Testing Framework': 7,
            'Algorithm Validation': 8, 'Maintenance': 9, 'Documentation': 10, 'Project Management': 11
        }
        
        todos.sort(key=lambda x: (priority_order.get(x['priority'], 4), 
                                 category_order.get(x['category'], 12)))
        
        return todos
    
    def present_for_approval(self, todos: List[Dict[str, Any]]) -> str:
        """Format masterful analysis and todos for user approval."""
        output = []
        output.append("**MASTERFUL SESSION PICKUP - COMPREHENSIVE PROJECT ANALYSIS**")
        output.append("=" * 75)
        output.append("")
        
        # Executive Intelligence Summary
        output.append("## Executive Intelligence Summary")
        output.append(f"- **Analysis Timestamp**: {self.timestamp}")
        output.append(f"- **Current Branch**: {self.context['git_status'].get('current_branch', 'unknown')}")
        output.append(f"- **Project Phase**: {self.context.get('project_phase', {}).get('phase', 'unknown')}")
        output.append(f"- **Code Quality Score**: {self.context.get('quality_assessment', {}).get('maintainability_score', 'unknown')}")
        output.append(f"- **Total Strategic Actions**: {len(todos)}")
        output.append("")
        
        # Deep Context Analysis
        output.append("## Deep Context Analysis")
        
        # Handoff Intelligence
        if self.context['handoff']['exists']:
            output.append("+ Previous session handoff analyzed")
        else:
            output.append("- No previous session context available")
        
        # Codebase Health
        codebase = self.context.get('codebase_analysis', {})
        incomplete_count = len(codebase.get('incomplete_implementations', []))
        todo_count = len(codebase.get('todo_comments', []))
        
        if incomplete_count > 0:
            output.append(f"- {incomplete_count} incomplete implementations detected")
        else:
            output.append("+ No incomplete implementations found")
            
        if todo_count > 0:
            output.append(f"- {todo_count} TODO comments require attention")
        else:
            output.append("+ No outstanding TODO comments")
        
        # Test Coverage Assessment
        test_coverage = codebase.get('test_coverage', {})
        test_quality = test_coverage.get('test_quality', 'unknown')
        untested_count = len(test_coverage.get('untested_modules', []))
        
        output.append(f"+ Test coverage quality: {test_quality}")
        if untested_count > 0:
            output.append(f"- {untested_count} modules lack test coverage")
        
        # Quality Assessment
        quality = self.context.get('quality_assessment', {})
        security_issues = len(quality.get('security_issues', []))
        tech_debt = len(quality.get('technical_debt', []))
        
        if security_issues > 0:
            output.append(f"- {security_issues} CRITICAL security issues detected")
        else:
            output.append("+ No security vulnerabilities detected")
            
        if tech_debt > 0:
            output.append(f"- {tech_debt} technical debt items identified")
        
        output.append("")
        
        # Strategic Action Plan with Wisdom
        output.append("## Strategic Action Plan (Wisdom-Driven Prioritization)")
        output.append("")
        
        for i, todo in enumerate(todos, 1):
            priority_symbol = {
                'CRITICAL': '[!]',
                'HIGH': '[H]', 
                'MEDIUM': '[M]',
                'LOW': '[L]'
            }.get(todo['priority'], '[?]')
            
            output.append(f"### {i}. {priority_symbol} {todo['task']}")
            output.append(f"   - **Priority**: {todo['priority']} | **Category**: {todo['category']}")
            output.append(f"   - **Time Investment**: {todo['estimated_time']}")
            output.append(f"   - **Strategic Rationale**: {todo['rationale']}")
            
            if 'wisdom' in todo:
                output.append(f"   - **Development Wisdom**: {todo['wisdom']}")
            
            if 'file_location' in todo:
                output.append(f"   - **Location**: {todo['file_location']}")
            
            if 'details' in todo:
                output.append("   - **Implementation Details**:")
                for detail in todo['details'][:3]:  # Limit to 3 details
                    output.append(f"     {detail}")
            
            output.append("")
        
        # Wisdom Principles Applied
        output.append("## Development Wisdom Principles Applied")
        output.append("- PRINCIPLE 1: 'Finish What You Started' - Incomplete work prioritized")
        output.append("- PRINCIPLE 2: 'Address Critical Flaws Immediately' - Security first")
        output.append("- PRINCIPLE 3: 'Validate Recent Changes' - Test modifications")
        output.append("- PRINCIPLE 4: 'TODO Comments Are Commitments' - Honor promises")
        output.append("- PRINCIPLE 5: 'Testing Is Insurance' - Address coverage gaps")
        output.append("- PRINCIPLE 6: 'Parse Handoff Intelligence' - Honor previous insights")
        output.append("- PRINCIPLE 7: 'Architecture Before Features' - Structure first")
        output.append("- PRINCIPLE 8: 'Document Decisions' - Capture architectural wisdom")
        output.append("- PRINCIPLE 9: 'Validate Integration' - System cohesion")
        output.append("- PRINCIPLE 10: 'Honor The Phase' - Phase-appropriate development")
        output.append("- PRINCIPLE 11: 'Measure What Matters' - Comprehensive tracking")
        output.append("")
        
        # Project Health Assessment
        output.append("## Project Health Assessment")
        phase = self.context.get('project_phase', {})
        current_phase = phase.get('phase', 'unknown')
        maturity = phase.get('maturity', 'unknown')
        
        output.append(f"- **Development Phase**: {current_phase}")
        output.append(f"- **Project Maturity**: {maturity}")
        output.append(f"- **Maintainability**: {quality.get('maintainability_score', 'unknown')}")
        
        recent_changes = codebase.get('recent_changes_impact', [])
        if recent_changes:
            output.append(f"- **Recent Activity**: {len(recent_changes)} files modified in last 5 commits")
        else:
            output.append("- **Recent Activity**: Minimal changes detected")
        
        output.append("")
        output.append("**TRUTH-BASED ANALYSIS COMPLETE**")
        output.append("**Please review this masterful action plan and approve to proceed.**")
        
        return "\n".join(output)
    
    def update_roadmap(self):
        """Update ROADMAP.md with current analysis findings."""
        roadmap_path = os.path.join(self.project_root, 'ROADMAP.md')
        
        if os.path.exists(roadmap_path):
            try:
                with open(roadmap_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update the "Last Updated" line
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "- **Last Updated**:" in line:
                        lines[i] = f"- **Last Updated**: {datetime.now().strftime('%Y-%m-%d')} (Session Pickup)"
                        break
                
                # Update current development focus based on analysis
                quality = self.context.get('quality_assessment', {})
                codebase = self.context.get('codebase_analysis', {})
                
                # Update footer timestamp
                for i, line in enumerate(lines):
                    if line.startswith("*Roadmap maintained by handoff.py/pickup.py scripts"):
                        lines[i] = f"*Roadmap maintained by handoff.py/pickup.py scripts - Updated: {datetime.now().strftime('%Y-%m-%d')}*"
                        break
                
                with open(roadmap_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
            except Exception as e:
                print(f"Warning: Could not update ROADMAP.md: {e}")

    def save_session_todo(self, presentation: str, todos: List[Dict[str, Any]]) -> None:
        """Save the wisdom-driven analysis to session_todo.md."""
        session_todo_path = os.path.join(self.project_root, 'session_todo.md')
        
        # Create markdown content for the session todo file
        content = []
        content.append("# Session TODO - Masterful Action Plan")
        content.append("")
        content.append(f"**Generated**: {self.timestamp}")
        content.append("**Analysis Type**: MASTERFUL SESSION PICKUP - COMPREHENSIVE PROJECT ANALYSIS")
        content.append("")
        
        # Executive Summary
        content.append("## Executive Intelligence Summary")
        content.append(f"- **Analysis Timestamp**: {self.timestamp}")
        content.append(f"- **Current Branch**: {self.context['git_status'].get('current_branch', 'unknown')}")
        content.append(f"- **Project Phase**: {self.context.get('project_phase', {}).get('phase', 'unknown')}")
        content.append(f"- **Code Quality Score**: {self.context.get('quality_assessment', {}).get('maintainability_score', 'unknown')}")
        content.append(f"- **Total Strategic Actions**: {len(todos)}")
        content.append("")
        
        # Context Analysis Summary
        content.append("## Deep Context Analysis")
        codebase = self.context.get('codebase_analysis', {})
        quality = self.context.get('quality_assessment', {})
        
        if self.context['handoff']['exists']:
            content.append("+ Previous session handoff analyzed")
        else:
            content.append("- No previous session context available")
        
        incomplete_count = len(codebase.get('incomplete_implementations', []))
        if incomplete_count > 0:
            content.append(f"- {incomplete_count} incomplete implementations detected")
        else:
            content.append("+ No incomplete implementations found")
        
        todo_count = len(codebase.get('todo_comments', []))
        if todo_count > 0:
            content.append(f"- {todo_count} TODO comments require attention")
        else:
            content.append("+ No outstanding TODO comments")
        
        test_coverage = codebase.get('test_coverage', {})
        content.append(f"+ Test coverage quality: {test_coverage.get('test_quality', 'unknown')}")
        
        security_issues = len(quality.get('security_issues', []))
        if security_issues > 0:
            content.append(f"- {security_issues} CRITICAL security issues detected")
        else:
            content.append("+ No security vulnerabilities detected")
        
        content.append("")
        
        # Strategic Action Plan
        content.append("## Strategic Action Plan (Wisdom-Driven Prioritization)")
        content.append("")
        
        for i, todo in enumerate(todos, 1):
            priority_symbol = {
                'CRITICAL': '[!]',
                'HIGH': '[H]', 
                'MEDIUM': '[M]',
                'LOW': '[L]'
            }.get(todo['priority'], '[?]')
            
            content.append(f"### {i}. {priority_symbol} {todo['task']}")
            content.append(f"   - **Priority**: {todo['priority']} | **Category**: {todo['category']}")
            content.append(f"   - **Time Investment**: {todo['estimated_time']}")
            content.append(f"   - **Strategic Rationale**: {todo['rationale']}")
            
            if 'wisdom' in todo:
                content.append(f"   - **Development Wisdom**: {todo['wisdom']}")
            
            if 'file_location' in todo:
                content.append(f"   - **Location**: {todo['file_location']}")
            
            if 'details' in todo:
                content.append("   - **Implementation Details**:")
                for detail in todo['details'][:3]:
                    content.append(f"     {detail}")
            
            content.append("")
        
        # Wisdom Principles
        content.append("## Development Wisdom Principles Applied")
        content.append("- PRINCIPLE 1: 'Finish What You Started' - Incomplete work prioritized")
        content.append("- PRINCIPLE 2: 'Address Critical Flaws Immediately' - Security first")
        content.append("- PRINCIPLE 3: 'Validate Recent Changes' - Test modifications")
        content.append("- PRINCIPLE 4: 'TODO Comments Are Commitments' - Honor promises")
        content.append("- PRINCIPLE 5: 'Testing Is Insurance' - Address coverage gaps")
        content.append("- PRINCIPLE 6: 'Parse Handoff Intelligence' - Honor previous insights")
        content.append("- PRINCIPLE 7: 'Architecture Before Features' - Structure first")
        content.append("- PRINCIPLE 8: 'Document Decisions' - Capture architectural wisdom")
        content.append("- PRINCIPLE 9: 'Validate Integration' - System cohesion")
        content.append("- PRINCIPLE 10: 'Honor The Phase' - Phase-appropriate development")
        content.append("- PRINCIPLE 11: 'Measure What Matters' - Comprehensive tracking")
        content.append("")
        
        # Project Health
        content.append("## Project Health Assessment")
        phase = self.context.get('project_phase', {})
        content.append(f"- **Development Phase**: {phase.get('phase', 'unknown')}")
        content.append(f"- **Project Maturity**: {phase.get('maturity', 'unknown')}")
        content.append(f"- **Maintainability**: {quality.get('maintainability_score', 'unknown')}")
        
        recent_changes = codebase.get('recent_changes_impact', [])
        if recent_changes:
            content.append(f"- **Recent Activity**: {len(recent_changes)} files modified in last 5 commits")
        else:
            content.append("- **Recent Activity**: Minimal changes detected")
        
        content.append("")
        content.append("**TRUTH-BASED ANALYSIS COMPLETE**")
        content.append("**Action plan ready for execution.**")
        
        # Write to file
        try:
            with open(session_todo_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
            print(f"Session TODO saved to: {session_todo_path}")
        except Exception as e:
            print(f"Warning: Could not save session_todo.md: {str(e)}")
    
    def run(self) -> str:
        """Execute the pickup command workflow."""
        try:
            # Gather all context
            self.gather_context()
            
            # Generate intelligent todos
            todos = self.analyze_and_prioritize()
            
            # Present for approval
            presentation = self.present_for_approval(todos)
            
            # Save session TODO to file
            self.save_session_todo(presentation, todos)
            
            # Update roadmap with current analysis
            self.update_roadmap()
            
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