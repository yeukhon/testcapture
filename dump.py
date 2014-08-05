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
            new_node = add_for_name(node.targets[0])
            return new_node
        elif isinstance(node.targets[0], ast.Subscript):
            new_node = add_for_subscript(node.targets[0])
            return new_node

def add_for_name(node):
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
    return new_node

def add_for_subscript(node):
    id_name = None
    id_name = node.value.id
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
            for _node in node.body:
                new_stmts.append(createNode(_node))
            new_node_body = []
            for i in xrange(0, len(new_stmts)):
                new_node = new_stmts[i]
                old_node = body[i]
                if new_node:
                    new_node_body.append(new_node)
                    ast.copy_location(new_node, old_node)
                    ast.increment_lineno(old_node)
                    ast.fix_missing_locations(new_node)
                    ast.fix_missing_locations(old_node)
                new_node_body.append(old_node)
            node.body = new_node_body
            ast.fix_missing_locations(node)
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
