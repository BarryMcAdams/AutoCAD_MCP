"""
Security Manager for Code Execution
==================================

Provides security validation and sandboxing for interactive Python code
execution in AutoCAD context. Ensures safe execution while preventing
dangerous operations.
"""

import logging
import ast
import re
from typing import Dict, Any, List, Set, Optional

logger = logging.getLogger(__name__)


class SecurityManager:
    """
    Manages security for interactive code execution.
    """

    def __init__(self):
        """Initialize security manager."""
        # Dangerous modules and functions to block
        self.blocked_imports = {
            "os",
            "sys",
            "subprocess",
            "shutil",
            "glob",
            "pathlib",
            "urllib",
            "requests",
            "socket",
            "ftplib",
            "smtplib",
            "pickle",
            "marshal",
            "shelve",
            "dbm",
            "ctypes",
            "faulthandler",
            "gc",
            "importlib",
            "multiprocessing",
            "threading",
            "concurrent",
            "tempfile",
            "atexit",
            "signal",
            "resource",
        }

        # Dangerous built-in functions to block
        self.blocked_builtins = {
            "eval",
            "exec",
            "compile",
            "__import__",
            "open",
            "input",
            "raw_input",
            "exit",
            "quit",
            "help",
            "vars",
            "locals",
            "globals",
            "dir",
            "getattr",
            "setattr",
            "delattr",
            "hasattr",
            "isinstance",
            "issubclass",
            "callable",
        }

        # Dangerous attribute patterns
        self.blocked_attributes = {
            "__class__",
            "__bases__",
            "__subclasses__",
            "__import__",
            "__builtin__",
            "__builtins__",
            "__file__",
            "__name__",
            "__package__",
            "func_globals",
            "f_globals",
            "gi_frame",
        }

        # Allowed safe built-ins for execution environment
        self.safe_builtins = {
            "abs",
            "bool",
            "chr",
            "complex",
            "dict",
            "divmod",
            "enumerate",
            "filter",
            "float",
            "format",
            "frozenset",
            "hex",
            "int",
            "len",
            "list",
            "map",
            "max",
            "memoryview",
            "min",
            "oct",
            "ord",
            "pow",
            "range",
            "repr",
            "reversed",
            "round",
            "set",
            "slice",
            "sorted",
            "str",
            "sum",
            "tuple",
            "type",
            "zip",
            "print",
        }

        logger.info("Security Manager initialized")

    def validate_python_code(self, code: str) -> bool:
        """
        Validate Python code for security risks.

        Args:
            code: Python code to validate

        Returns:
            True if code is safe to execute
        """
        try:
            # Parse code into AST
            tree = ast.parse(code)

            # Check for dangerous constructs
            validator = CodeValidator(self)
            validator.visit(tree)

            if validator.violations:
                logger.warning(f"Security violations found in code: {validator.violations}")
                return False

            # Additional string-based checks
            if not self._validate_code_strings(code):
                return False

            logger.debug("Code validation passed")
            return True

        except SyntaxError as e:
            logger.warning(f"Syntax error in code: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error validating code: {str(e)}")
            return False

    def _validate_code_strings(self, code: str) -> bool:
        """
        Additional string-based validation for dangerous patterns.

        Args:
            code: Code to validate

        Returns:
            True if code passes string validation
        """
        code_lower = code.lower()

        # Check for dangerous patterns
        dangerous_patterns = [
            r"__import__\s*\(",
            r"exec\s*\(",
            r"eval\s*\(",
            r"open\s*\(",
            r"file\s*\(",
            r"input\s*\(",
            r"raw_input\s*\(",
            r"import\s+os",
            r"import\s+sys",
            r"import\s+subprocess",
            r"from\s+os\s+import",
            r"from\s+sys\s+import",
            r"\.system\s*\(",
            r"\.popen\s*\(",
            r"\.call\s*\(",
            r"\.run\s*\(",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, code_lower):
                logger.warning(f"Dangerous pattern found: {pattern}")
                return False

        return True

    def get_safe_builtins(self) -> Dict[str, Any]:
        """
        Get dictionary of safe built-in functions for execution.

        Returns:
            Dictionary of safe built-ins
        """
        import builtins

        safe_dict = {}

        for name in self.safe_builtins:
            if hasattr(builtins, name):
                safe_dict[name] = getattr(builtins, name)

        return safe_dict

    def create_safe_globals(self, autocad_wrapper=None) -> Dict[str, Any]:
        """
        Create safe global namespace for code execution.

        Args:
            autocad_wrapper: AutoCAD wrapper instance

        Returns:
            Safe globals dictionary
        """
        safe_globals = {
            "__builtins__": self.get_safe_builtins(),
            "__name__": "__main__",
            "__doc__": None,
        }

        # Add AutoCAD objects if provided
        if autocad_wrapper:
            safe_globals.update(
                {
                    "acad": autocad_wrapper,
                    "app": autocad_wrapper.app,
                    "doc": autocad_wrapper.doc,
                    "model": autocad_wrapper.model,
                }
            )

        # Add safe math functions
        import math

        safe_math_functions = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "atan2",
            "sinh",
            "cosh",
            "tanh",
            "asinh",
            "acosh",
            "atanh",
            "sqrt",
            "pow",
            "exp",
            "log",
            "log10",
            "log2",
            "ceil",
            "floor",
            "trunc",
            "fabs",
            "fmod",
            "pi",
            "e",
            "tau",
            "inf",
            "nan",
            "degrees",
            "radians",
            "isnan",
            "isinf",
            "isfinite",
        ]

        safe_globals["math"] = type(
            "SafeMath",
            (),
            {name: getattr(math, name) for name in safe_math_functions if hasattr(math, name)},
        )()

        return safe_globals

    def get_security_report(self) -> Dict[str, Any]:
        """
        Get security configuration report.

        Returns:
            Dictionary containing security settings
        """
        return {
            "blocked_imports_count": len(self.blocked_imports),
            "blocked_builtins_count": len(self.blocked_builtins),
            "blocked_attributes_count": len(self.blocked_attributes),
            "safe_builtins_count": len(self.safe_builtins),
            "validation_enabled": True,
            "sandboxing_enabled": True,
        }


class CodeValidator(ast.NodeVisitor):
    """AST visitor to validate code for security risks."""

    def __init__(self, security_manager: SecurityManager):
        """Initialize validator."""
        self.security_manager = security_manager
        self.violations = []

    def visit_Import(self, node):
        """Check import statements."""
        for alias in node.names:
            if alias.name in self.security_manager.blocked_imports:
                self.violations.append(f"Blocked import: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Check from-import statements."""
        if node.module in self.security_manager.blocked_imports:
            self.violations.append(f"Blocked import from: {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node):
        """Check function calls."""
        # Check for blocked built-in functions
        if isinstance(node.func, ast.Name):
            if node.func.id in self.security_manager.blocked_builtins:
                self.violations.append(f"Blocked function call: {node.func.id}")

        # Check for attribute calls that might be dangerous
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ["system", "popen", "call", "run"]:
                self.violations.append(f"Blocked method call: {node.func.attr}")

        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Check attribute access."""
        if node.attr in self.security_manager.blocked_attributes:
            self.violations.append(f"Blocked attribute access: {node.attr}")
        self.generic_visit(node)

    def visit_Name(self, node):
        """Check name references."""
        if node.id in self.security_manager.blocked_builtins:
            if isinstance(node.ctx, ast.Load):  # Only flag when loading/reading
                self.violations.append(f"Blocked name reference: {node.id}")
        self.generic_visit(node)
