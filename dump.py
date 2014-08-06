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
        elif isinstance(node.targets[0], ast.Attribute):
            new_node = add_for_attribute(node.targets[0])
            return new_node
        elif isinstance(node.targets[0], ast.Subscript):
            new_node = add_for_subscript(node.targets[0])
            return new_node
    elif isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Call):
            new_node = add_for_call(node.value)
            return new_node

def z_merge(L1, L2):
    for i in range(len(L1)):
        yield L1[i], L2[i]

def get_args_names(args):
    names = []
    name = None
    for arg in args:
        if isinstance(arg, ast.Attribute):
            name = arg.value.id + "." + arg.attr
        else:
            name = arg.id
        names.append(name)
    return names

def make_str(s):
    return ast.Str(s=s)

def add_for_call(node):
    id_name = None
    args = node.args
    if isinstance(node.func, ast.Attribute):
        id_name = node.func.value.id + "." + node.func.attr
    else:
        id_name = node.func.id

    arg_names = get_args_names(args)
    print arg_names
    
    r_str_list = ["reading {} values:"] + ["{}: {}" for x in arg_names]
    r_str = "\n".join(r_str_list)
    r_args = [make_str(id_name)]
    for (x,y) in z_merge(arg_names, args):
        r_args.append(make_str(x))
        r_args.append(y)

    new_node = ast.Print(dest=None,
        values=[
            ast.Call(func=ast.Attribute(
                value=ast.Str(s=r_str),
                attr='format', ctx=ast.Load()),
                args=r_args,
            keywords=[], starargs=None, kwargs=None),
        ], nl=True)
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

def add_for_attribute(node):
    id_name = None
    id_name = node.value.id + '.' + node.attr
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
#pretty.parseprint(new_code)

class T(ast.NodeTransformer):
    def visit_FuncDef(self, node):
        for n in node.body:
            ast.fix_missing_locations(n)
        return node
c  = T().visit(new_code)
code = compile(new_code, 'new.py','exec')
pretty.parseprint(new_code)
import unparser
import sys
unparser.Unparser(new_code, sys.stdout)
print "\n"
