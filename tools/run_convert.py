from pathlib import Path

base = Path(__file__).resolve().parent
ns = globals()
for name in ["convert_wp.py", "convert_wp_part2_fixed.py", "convert_wp_part3_fixed.py"]:
    path = base / name
    code = path.read_text(encoding="utf-8")
    ns["__file__"] = str(path)
    exec(compile(code, str(path), "exec"), ns)

