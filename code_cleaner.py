import ast
import io
import tokenize
from typing import Set, Tuple
import os
from pathlib import Path

EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'env', 'build', 'dist'}

def process_file(filepath: Path) -> bool:
    try:
        src = filepath.read_text(encoding='utf-8')
    except Exception:
        return False

    try:
        mod = ast.parse(src)
    except Exception:
        return False

    def collect_docstring_positions(node, positions: Set[Tuple[int,int]]):
        if hasattr(node, 'body') and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                positions.add((first.lineno, first.col_offset))
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and getattr(child, 'body', None):
                first = child.body[0]
                if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                    positions.add((first.lineno, first.col_offset))
            if hasattr(child, 'body'):
                collect_docstring_positions(child, positions)

    positions = set()
    collect_docstring_positions(mod, positions)

    src_io = io.StringIO(src)
    out_tokens = []
    try:
        g = tokenize.generate_tokens(src_io.readline)
    except Exception:
        return False

    for tok in g:
        ttype, tstring, (srow, scol), (erow, ecol), line = tok
        if ttype == tokenize.COMMENT:
            continue
        if ttype == tokenize.STRING:
            if (srow, scol) in positions:
                continue
        out_tokens.append((ttype, tstring))

    try:
        new_src = tokenize.untokenize(out_tokens)
    except Exception:
        return False

    new_src = '\n'.join([ln.rstrip() for ln in new_src.splitlines()])
    import re
    new_src = re.sub(r"\n{3,}", "\n\n", new_src)

    try:
        filepath.write_text(new_src, encoding='utf-8')
    except Exception:
        return False

    return True

def main():
    repo_root = Path('.').resolve()
    processed = 0
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in files:
            if not fname.endswith('.py'):
                continue
            fpath = Path(root) / fname
            if fpath.resolve() == Path(__file__).resolve():
                continue
            ok = process_file(fpath)
            if ok:
                processed += 1

    print(f'Stripping complete. Files processed: {processed}')

if __name__ == '__main__':
    main()