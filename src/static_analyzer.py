# src/static_analyzer.py
import ast
import pylint.lint
from pylint.reporters import JSONReporter

class StaticAnalyzer:
    def analyze(self, code_snippet):
        issues = []
        
        # Basic AST analysis
        try:
            tree = ast.parse(code_snippet)
            issues.extend(self._check_complexity(tree))
            issues.extend(self._check_naming_conventions(tree))
        except Exception as e:
            issues.append(f"Parsing error: {str(e)}")
            
        # Pylint analysis
        pylint_issues = self._run_pylint(code_snippet)
        issues.extend(pylint_issues)
        
        return issues
    
    def _check_complexity(self, tree):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if len(list(ast.walk(node))) > 50:
                    issues.append(f"Function '{node.name}' might be too complex")
        return issues
    
    def _check_naming_conventions(self, tree):
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                if not node.id.islower():
                    issues.append(f"Variable '{node.id}' should use lowercase naming convention")
        return issues
    
    def _run_pylint(self, code_snippet):
        # Implementation for running pylint on the code snippet
        return []