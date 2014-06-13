Example of mapping over an AST
=======

The file `foo.py` contains a couple of dummy Python classes. Run

    import map_ast
    print map_ast.test_codegen()
    
to generate a modified version of `foo.py`.

Run

    map_ast.test_bytecode()
    
to generate a file `output.pyc` with the bytecode of the modified `foo.py` (which does not require `codegen`).
