import ast
import inspect
import unittest
import pretty

import new

code = inspect.getsource(new)
nodes = ast.parse(code)

pretty.parseprint(nodes)

class Tracker(ast.NodeTransformer):
    def __init__(self, *args, **kwargs):
        super(Tracker, self).__init__(*args, **kwargs)
        self.tracking = {}
        self.statements = []
    def visit_FunctionDef(self, node):
        if node.name.startswith('test'):
            statements = [stmt for stmt in node.body
                        if isinstance(stmt, ast.Assign) or
                           isinstance(stmt, ast.Expr)
                         ]
            self.statements += statements
            self.tracking[node.name] = None
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if node in self.statements:
            old_node_name = None
            if isinstance(node.targets[0], ast.Subscript):
                old_node_name = node.targets[0].value.id + str(node.targets[0].slice.value.n)
            else:
                old_node_name = node.targets[0].id
            new_node = ast.Print(dest=None,
                values=[
                    ast.Call(func=ast.Attribute(
                        value=ast.Str(s='reading {} value: {}'),
                                attr='format', ctx=ast.Load()),
                                args=[
                                    ast.Num(n=1000),
                                    ast.Num(n=3000),
                  ], keywords=[], starargs=None, kwargs=None),
              ], nl=True)
            ast.copy_location(new_node, node)
            ast.increment_lineno(node)
            ast.fix_missing_locations(new_node)
            return new_node
        else:
            return node
a = Tracker()
new_code = a.visit(nodes)

code = compile(new_code, 'new.py','exec')
pretty.parseprint(new_code)
import unparser
import sys
unparser.Unparser(new_code, sys.stdout)
print "\n"
#exec(code)
