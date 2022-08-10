from wallaby.compiler import compile_file


document = compile_file("README.md")
document.execute()

