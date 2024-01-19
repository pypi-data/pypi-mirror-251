# paths-parser

```
pip install paths_parser
```

```py
import paths_parser

with open("../Case1-path.txt", "r") as f:
    src = f.read()

print(len(paths_parser.parse(src)))
```