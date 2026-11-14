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
from security_policy import with_security_policy
from license_bundle import with_bundled_licenses
assert page == with_security_policy(with_bundled_licenses(page))
editor = (ROOT / "mobile-editor.html").read_text(encoding="utf-8")
assert editor == with_security_policy(with_bundled_licenses(editor), wasm=True)
embedded = re.search(r'<script id="reference-data" type="application/json">(.*?)</script>', page, re.S).group(1)
assert json.loads(embedded) == data
assert "C++23 (GCC 15.2.0)" in page and "C++17" not in page
keys = [g["key"] for g in data["groups"]] + [s["key"] for s in data["limits"]]
assert len(keys) == len(set(keys))
assert not (set(keys) & {"search", "main", "source", "sidebar", "theme", "clear", "toast", "reference-data"})
items = [i for g in data["groups"] for i in g["items"]]
from html.parser import HTMLParser

class CodeText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text = []

    def handle_data(self, value):
        self.text.append(value)

    def handle_starttag(self, tag, attrs):
        assert tag == "span" and all(key == "style" for key, _ in attrs)

highlighting = json.loads((ROOT / "syntax-highlighting.json").read_text(encoding="utf-8"))
for item in items:
    for field in ("code", "full"):
        parser = CodeText()
        parser.feed(item[field+"Html"])
        assert "".join(parser.text) == item[field], (item["id"], field)
        cached = highlighting["items"][item["id"]][field]
        assert cached["sha256"] == hashlib.sha256(item[field].encode("utf-8")).hexdigest()
        assert item[field+"Html"] == cached["html"]
algorithms = [g for g in data["groups"] if g["page"] == "algo"]
assert len(algorithms) == 29
assert all(len(g["items"]) == 1 and g.get("reading") for g in algorithms)
assert len({g["title"] for g in algorithms}) == len(algorithms)
import unicodedata
def gojuon(reading):
    plain = "".join(c for c in unicodedata.normalize("NFD", reading) if not unicodedata.combining(c))
    return plain.translate(str.maketrans("ぁぃぅぇぉっゃゅょゎ", "あいうえおつやゆよわ")), reading
assert [g["reading"] for g in algorithms] == sorted([g["reading"] for g in algorithms], key=gojuon)
assert algorithms[0]["title"] == "いもす法" and algorithms[-1]["title"] == "ワーシャルフロイド法"
assert len({i["id"] for i in items}) == len(items)
assert all("#include" in i["full"] and "int main()" in i["full"] and "// Reference:" in i["full"] for i in items)
assert all("万" not in s["content"] and "億" not in s["content"] for s in data["limits"])
assert any("reverse(A.begin()+l, A.begin()+r);" == i["code"] for i in items)
scripts = re.findall(r'<script>(.*?)</script>', page, re.S)
assert len(scripts) == 1
with tempfile.TemporaryDirectory() as tmp:
    script = pathlib.Path(tmp) / "page.js"
    script.write_text("\n".join(scripts), encoding="utf-8")
    subprocess.run(["node", "--check", str(script)], check=True)
tracked = [ROOT / "index.html", ROOT / "mobile-editor.html", ROOT / "reference-data.json"] + sorted((ROOT / "docs").glob("*.md"))
before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
subprocess.run(["python", str(ROOT / "build_reference.py")], check=True)
assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in before.items())
print(f"PASS: {len(items)} complete examples; unique IDs; embedded data; reproducible HTML/Markdown; JavaScript syntax")
