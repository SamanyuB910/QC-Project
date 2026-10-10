"""Static checks that every file we upload to Qollab respects the in-browser runtime's rules.

Rules (Qollab docs, runtime environment / Python projects):
  * data files load only when their path is a plain string literal (no os.path.join / f-strings / __file__)
  * main() must be one line, at column 1, with only int/float/str/bool annotations; the runtime calls it itself
  * nobody else may call main() (it would run twice) and there is no __main__ block
  * heavy optional packages are imported lazily so a default Run does not pay for them
  * job.get_counts( raises on the built-in simulator; always go through job.result()
  * every file under 2 MB
"""
import ast
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
UPLOAD_DIRS = [ROOT / "five_tests_priced", ROOT / "tools" / "qollab_smoke"]
LAZY_ONLY = {"sklearn", "pandas", "matplotlib", "qiskit_aer", "scipy", "joblib"}
LITERAL_CALLS = {"open", "loadtxt", "genfromtxt", "load", "read_csv"}
ALLOWED_ANN = {"int", "float", "str", "bool"}


def _py_files():
    out = []
    for d in UPLOAD_DIRS:
        if d.exists():
            out += sorted(d.rglob("*.py"))
    return out


PY_FILES = _py_files()


def _ids(paths):
    return [str(p.relative_to(ROOT)) for p in paths]


@pytest.mark.parametrize("path", PY_FILES, ids=_ids(PY_FILES))
def test_no_path_building(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "__file__":
            pytest.fail(f"{path.name}:{node.lineno} uses __file__")
        if isinstance(node, ast.Attribute) and node.attr == "path" and isinstance(node.value, ast.Name) \
                and node.value.id == "os":
            pytest.fail(f"{path.name}:{node.lineno} uses os.path")


@pytest.mark.parametrize("path", PY_FILES, ids=_ids(PY_FILES))
def test_data_paths_are_literals(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else fn.attr if isinstance(fn, ast.Attribute) else None
            if name in LITERAL_CALLS and node.args:
                a0 = node.args[0]
                if name == "load" and not (isinstance(a0, ast.Constant) and isinstance(a0.value, str)):
                    continue  # json.load(fh) takes a file handle, not a path
                assert isinstance(a0, ast.Constant) and isinstance(a0.value, str), \
                    f"{path.name}:{node.lineno} {name}() path must be a string literal"


@pytest.mark.parametrize("path", PY_FILES, ids=_ids(PY_FILES))
def test_heavy_imports_are_lazy(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:  # module top level only
        mods = []
        if isinstance(node, ast.Import):
            mods = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods = [node.module.split(".")[0]]
        bad = set(mods) & LAZY_ONLY
        assert not bad, f"{path.name}:{node.lineno} top-level import of {bad} (import inside the function that needs it)"


@pytest.mark.parametrize("path", PY_FILES, ids=_ids(PY_FILES))
def test_no_job_get_counts_shortcut(path):
    src = path.read_text(encoding="utf-8")
    assert not re.search(r"\bjob\.get_(?:counts|probabilities)\s*\(", src), \
        f"{path.name}: use job.result().get_counts(...), not job.get_counts(...)"


@pytest.mark.parametrize("path", [p for p in PY_FILES if p.name == "main.py"],
                         ids=_ids([p for p in PY_FILES if p.name == "main.py"]))
def test_main_signature_and_no_self_call(path):
    src = path.read_text(encoding="utf-8")
    lines = [ln for ln in src.splitlines() if ln.startswith("def main(")]
    assert len(lines) == 1, "exactly one 'def main(' at column 1"
    assert lines[0].rstrip().endswith(":"), "main() signature must fit on one line"
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    for a in fn.args.args:
        assert isinstance(a.annotation, ast.Name) and a.annotation.id in ALLOWED_ANN, \
            f"main() parameter {a.arg} must be annotated int/float/str/bool"
    assert len(fn.args.defaults) == len(fn.args.args), "every main() parameter needs a default"
    for node in tree.body:
        if isinstance(node, ast.If) and "__name__" in ast.dump(node.test):
            pytest.fail("no __main__ block: Qollab calls main() itself")
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) \
                and isinstance(node.value.func, ast.Name) and node.value.func.id == "main":
            pytest.fail("main() must not be called at module level")


@pytest.mark.parametrize("d", [d for d in UPLOAD_DIRS if d.exists()], ids=lambda d: d.name)
def test_upload_files_small(d):
    for f in d.rglob("*"):
        if f.is_file() and "__pycache__" not in f.parts:
            assert f.stat().st_size < 2_000_000, f"{f} is over 2 MB"
