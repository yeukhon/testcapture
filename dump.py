import ast
import inspect
import unittest
import pretty

import new

code = inspect.getsource(new)
nodes = ast.parse(code)

#pretty.parseprint(nodes)

def createNode(node):
    if isinstance(node, ast.Assign):
        if isinstance(node.targets[0], ast.Name):
            new_node = add(node.targets[0])
            return new_node

def add(node):
    id_name = None
    id_name = node.id
    new_node = ast.Print(dest=None,
        values=[
            ast.Call(func=ast.Attribute(
                value=ast.Str(s='reading {} value: {}'),
                attr='format', ctx=ast.Load()),
                args=[
                    ast.Str(s=id_name),
                    node
                ],
            keywords=[], starargs=None, kwargs=None),
        ], nl=True)
    ast.copy_location(new_node, node)
    ast.increment_lineno(node)
    ast.fix_missing_locations(new_node)
    ast.fix_missing_locations(node)
    return new_node

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

            body = node.body

            new_stmts = []
            for node in node.body:
                new_stmts.append(createNode(node))
            new_node_body = []
            for i in xrange(0, len(new_stmts)):
                if new_stmts[i]:
                    new_node_body.append(new_stmts[i])
                new_node_body.append(body[i])
            node.body = new_node_body
            return node
        ast.fix_missing_locations(node)
        return node

    """
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
                                    ast.Str(s='a'),
                                    node.targets[0],
                  ], keywords=[], starargs=None, kwargs=None),
              ], nl=True)
            #ast.copy_location(new_node, node)
            ast.increment_lineno(node)
            ast.fix_missing_locations(new_node)
            ast.fix_missing_locations(node)
            return node
        else:
            return node
    """
a = Tracker()
new_code = a.visit(nodes)

code = compile(new_code, 'new.py','exec')
pretty.parseprint(new_code)
import unparser
import sys
unparser.Unparser(new_code, sys.stdout)
print "\n"
#exec(code)
