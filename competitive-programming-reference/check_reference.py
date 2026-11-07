"""生成物の整合性とHTML内JavaScriptの構文を確認。Python3とNode.jsが必要。"""
import hashlib
import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
data = json.loads((ROOT / "reference-data.json").read_text(encoding="utf-8"))
page = (ROOT / "index.html").read_text(encoding="utf-8")
embedded = re.search(r'<script id="reference-data" type="application/json">(.*?)</script>', page, re.S).group(1)
assert json.loads(embedded) == data
keys = [g["key"] for g in data["groups"]] + [s["key"] for s in data["limits"]]
assert len(keys) == len(set(keys))
assert not (set(keys) & {"search", "main", "source", "sidebar", "theme", "clear", "toast", "reference-data"})
items = [i for g in data["groups"] for i in g["items"]]
assert len({i["id"] for i in items}) == len(items)
assert all("#include" in i["full"] and "int main()" in i["full"] and "// Reference:" in i["full"] for i in items)
assert all("万" not in s["content"] and "億" not in s["content"] for s in data["limits"])
assert any("reverse(A.begin()+l, A.begin()+r);" == i["code"] for i in items)
scripts = re.findall(r'<script>(.*?)</script>', page, re.S)
assert len(scripts) == 1
with tempfile.TemporaryDirectory() as tmp:
    script = pathlib.Path(tmp) / "page.js"
    script.write_text(scripts[0], encoding="utf-8")
    subprocess.run(["node", "--check", str(script)], check=True)
tracked = [ROOT / "index.html", ROOT / "reference-data.json"] + sorted((ROOT / "docs").glob("*.md"))
before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
subprocess.run(["python", str(ROOT / "build_reference.py")], check=True)
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in before.items())
print(f"PASS: {len(items)} complete examples; unique IDs; embedded data; reproducible HTML/Markdown; JavaScript syntax")
