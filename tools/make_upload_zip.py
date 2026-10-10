"""Build qollab_upload.zip from five_tests_priced/ for Qollab's "Upload / Browse -> Files..." (choose Unpack).

Qollab keeps folder paths when it unpacks an archive (a plain folder upload from the browser can drop
subfolders). The archive has no single wrapping folder, so paths land exactly as in five_tests_priced/.

    .venv/Scripts/python.exe tools/make_upload_zip.py
"""
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "five_tests_priced"
OUT = ROOT / "qollab_upload.zip"

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SRC.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts:
            z.write(f, f.relative_to(SRC).as_posix())
            print("  +", f.relative_to(SRC).as_posix())
print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.1f} KB)")
