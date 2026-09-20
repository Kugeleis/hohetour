from pathlib import Path
base = Path("/workspace/tools")
for name in ["convert_wp.py", "convert_wp_part2_fixed.py", "convert_wp_part3_fixed.py"]:
    code = (base / name).read_text(encoding="utf-8")
    exec(compile(code, name, "exec"), globals())
