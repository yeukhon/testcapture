import ast
import inspect
import unittest
import pretty
import itertools

import new

Monitor = {}
code = inspect.getsource(new)
nodes = ast.parse(code)

def monitor_on(fname, lineno, var_name, var_obj):
    var_dict = {}
    for name, value in pairwise(variables):
        var_dict[name] = value
    if not Monitor.get(fname):
        Monitor[fname] = {}
    if not Monitor[fname].get(lineno):
        Monitor[fname][lineno] = {}
    Monitor[fname][lineno][var_name] = var_obj

def monitor_node(fname, lineno, var_name, var_obj):
    code = """\
try:
    monitor_on({}, {}, {}, {})
except (IndexError, KeyError, AttributeError, UnboundLocalError):
    monitor_on({}, {}, {}, "__undefined__")
    """

    nodes = ast.parse(code)
    pretty.parseprint(nodes)
    first_args = [ make_str(x) for x in
        [fname, lineno, var_name]]
    first_args += [var_obj]

    second_args = [ make_str(x) for x in
        [fname, lineno, var_name, "__unefined__"] ]
    nodes.body[0].body[0].value.args = first_args
    nodes.body[0].handlers[0].body[0].value.args = second_args
    return nodes.body[0]

def createNode(fname, node):
    if isinstance(node, ast.Assign):
        if isinstance(node.targets[0], ast.Name):
            new_node = add_for_name(fname, node.targets[0])
            return new_node
        elif isinstance(node.targets[0], ast.Attribute):
            new_node = add_for_attribute(fname, node.targets[0])
            return new_node
        elif isinstance(node.targets[0], ast.Subscript):
            new_node = add_for_subscript(fname, node.targets[0])
            return new_node
    elif isinstance(node, ast.Expr):
        if isinstance(node.value, ast.Call):
            new_node = add_for_call(fname, node.value)
            return new_node
    else:
        return node

def z_merge(L1, L2):
    for i in range(len(L1)):
        yield L1[i], L2[i]

def get_arg_name(arg):
    if isinstance(arg, ast.Attribute):
        return arg.value.id + "." + arg.attr
    elif isinstance(arg, ast.Subscript):
        return arg.value.id + "[" + arg.slice.value.s + "]"
    elif isinstance(arg, ast.Str):
        return arg.s
    else:
        return arg.id

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

def add_for_call(fname, node):
    id_name = None
    args = node.args
    if isinstance(node.func, ast.Attribute):
        id_name = node.func.value.id + "." + node.func.attr
    else:
        id_name = node.func.id

    new_nodes = [
        monitor_node(fname, get_arg_name(arg),
            arg.lineno, arg) for arg in node.args
    ]

    return new_nodes

def add_for_name(fname, node):
    id_name = None
    id_name = node.id
    new_node = monitor_node(fname, node.lineno, id_name, node)
    return new_node

def add_for_attribute(fname, node):
    id_name = None
    id_name = node.value.id + '.' + node.attr
    new_node = monitor_node(fname, node.lineno, id_name, node)
    return new_node

def add_for_subscript(fname, node):
    id_name = None
    id_name = node.value.id
    new_node = monitor_node(fname, node.lineno, id_name, node)
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
                new_stmts.append(createNode(node.name, _node))
            new_node_body = []
            for i in xrange(0, len(new_stmts)):
                new_node = new_stmts[i]
                old_node = body[i]
                if isinstance(new_node, list):
                    for _new_node in new_node:
                        ast.copy_location(_new_node, old_node)
                        new_node_body.append(_new_node)
                    new_node_body.append(old_node)
                elif isinstance(new_node, ast.TryExcept):
                    ast.copy_location(new_node, old_node)
                    new_node_body.append(new_node)
                    new_node_body.append(old_node)
                else:
                    new_node_body.append(new_node)
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
#pretty.parseprint(new_code)
import unparser
import sys
unparser.Unparser(new_code, sys.stdout)
print "\n"
