"""Simple example of mapping over an AST.

It uses a dummy file named 'foo.py'.

Use as::

    import map_ast
    print(map_ast.test_codegen())  # should print 'foo' rewritten
    map_ast.test_bytecode()        # should generate a file 'output.pyc' with the
                                   # bytecode of the modified 'foo'. Import it with
                                   # 'import output'
"""

import ast
import marshal
import py_compile
import time

import codegen


CLASSES_TO_CONVERT = {
    # classname: convert it?
    'Foo': True,
    'Bar': False
}


class RewriteInit(ast.NodeTransformer):

    def visit_ClassDef(self, node):
        self.CONVERT = CLASSES_TO_CONVERT[node.name]
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        self.IN_INIT = False
        if self.CONVERT and node.name == '__init__':
            new_args = (node.args.args[:2] +
                        [ast.Name(id='new1', ctx=ast.Param()),
                         ast.Name(id='new2', ctx=ast.Param())])
            node.args.args = new_args
            self.IN_INIT = True
        self.generic_visit(node)
        return node

    def visit_Assign(self, node):
        if self.IN_INIT:
            target = node.targets[0]
            if isinstance(target, ast.Attribute) and \
               target.value.id == 'self' and \
               target.attr == 'u':
                node.value = ast.parse('{"key1": new1, "key2": new2}', '<string>', mode='eval').body
        return node


def rewrite_tree():
    code = open('foo.py').read()
    tree = ast.parse(code, '<string>', 'exec')
    RewriteInit().visit(tree)
    return tree


def test_codegen():
    """This function will rewrite the init in class Foo, substituting
    the last parameter for two other parameters and constructing a
    dictionary with them.

    """
    return codegen.to_source(rewrite_tree())


def test_bytecode():
    """This function does the same as test_codegen, but it generates a
    .pyc, avoiding the use of codegen.

    """
    code = compile(ast.fix_missing_locations(rewrite_tree()), '<string>', 'exec')
    with open('output.pyc', 'wb') as fc:
        fc.write('\0\0\0\0')
        py_compile.wr_long(fc, long(time.time()))
        marshal.dump(code, fc)
        fc.flush()
        fc.seek(0, 0)
        fc.write(py_compile.MAGIC)