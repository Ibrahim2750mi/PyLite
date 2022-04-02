import _ast
import ast


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"modules": [], "variables": [], "functions": []}

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.stats["modules"].append((alias.asname if alias.asname else alias.name))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.stats["modules"].append((alias.asname if alias.asname else alias.name))
        self.generic_visit(node)

    # legacy.
    # def visit_Assign(self, node: ast.Assign) -> None:
    #     for alias in node.targets:
    #         if type(alias) == _ast.Name:
    #             alias: _ast.Name
    #             self.stats["variables"].append(alias.id)
    #         elif type(alias) == _ast.Tuple:
    #             alias: _ast.Tuple
    #             for name in alias.elts:
    #                 name: _ast.Name
    #                 self.stats['variables'].append(name.id)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.stats["functions"].append(node.name)

    def report(self):
        return self.stats
