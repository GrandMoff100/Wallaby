from wallaby import compile_text

with open("README.md", "r", encoding="utf-8") as fh:
    compile_text(fh.read())
