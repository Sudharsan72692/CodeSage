# src/utils.py
def format_explanation(explanation):
    """Format the explanation text for better readability"""
    return explanation.strip().replace('\n\n', '\n')

def sanitize_code(code_snippet):
    """Clean and sanitize input code"""
    return code_snippet.strip()