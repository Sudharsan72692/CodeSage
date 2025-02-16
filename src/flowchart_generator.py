import ast
import graphviz

class FlowchartGenerator:
    def __init__(self):
        self.dot = graphviz.Digraph()
        self.node_count = 0

    def generate_flowchart(self, code_snippet):
        try:
            self.dot.clear()
            self.node_count = 0
            
            tree = ast.parse(code_snippet)
            self._process_node(tree)

            return self.dot
        except Exception as e:
            self.dot.node('error', f'Error generating flowchart: {str(e)}')
            return self.dot

    def _process_node(self, node):
        if isinstance(node, ast.FunctionDef):
            self._add_function_node(node)
        elif isinstance(node, ast.If):
            self._add_if_node(node)
        elif isinstance(node, ast.For):
            self._add_for_node(node)
        elif isinstance(node, ast.While):
            self._add_while_node(node)

        for child in ast.iter_child_nodes(node):
            self._process_node(child)

    def _add_function_node(self, node):
        node_id = f"node_{self.node_count}"
        self.node_count += 1
        self.dot.node(node_id, f"Function: {node.name}")
        return node_id

    def _add_if_node(self, node):
        node_id = f"node_{self.node_count}"
        self.node_count += 1
        self.dot.node(node_id, "If condition")
        return node_id

    def _add_for_node(self, node):
        node_id = f"node_{self.node_count}"
        self.node_count += 1
        self.dot.node(node_id, "For loop")
        return node_id

    def _add_while_node(self, node):
        node_id = f"node_{self.node_count}"
        self.node_count += 1
        self.dot.node(node_id, "While loop")
        return node_id
