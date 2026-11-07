"""WSL/Linuxで python3 validate.py。公式ACLを一時フォルダへ取得して検証する。"""
import json
import pathlib
import random
import re
import subprocess
import tempfile
import urllib.request
from collections import deque

ROOT = pathlib.Path(__file__).resolve().parent
RNG = random.Random(20261108)


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "cpp-reference-validation"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


with tempfile.TemporaryDirectory(prefix="cpp-reference-") as directory:
    work = pathlib.Path(directory)
    commit = json.loads(fetch("https://api.github.com/repos/atcoder/ac-library/commits/master"))["sha"]
    headers = work / "atcoder"
    headers.mkdir()
    pending = ["dsu", "fenwicktree", "segtree", "modint", "math", "string"]
    downloaded = set()
    while pending:
        name = pending.pop()
        if name in downloaded:
            continue
        data = fetch(f"https://raw.githubusercontent.com/atcoder/ac-library/{commit}/atcoder/{name}")
        (headers / name).write_bytes(data)
        downloaded.add(name)
        pending.extend(re.findall(r'#include [<"]atcoder/([^>"]+)[>"]', data.decode()))

    programs = {}
    for source in sorted((ROOT / "examples").glob("*.cpp")):
        binary = work / source.stem
        subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra",
                        "-I", str(work), str(source), "-o", str(binary)], check=True)
        programs[source.stem] = binary

    count = 0

    def check(name, input_text, expected):
        global count
        result = subprocess.run([str(programs[name])], input=input_text, text=True,
                                capture_output=True, check=True, timeout=5)
        assert result.stdout.split() == list(map(str, expected)), (name, input_text, result.stdout, expected)
        count += 1

    import math
    for k in list(range(1, 101)) + [10**18, 10**18-1, 999999999**2, 999999999**2+1]:
        root = math.isqrt(k)
        check("binary_search", f"{k}\n", [root + (root*root != k)])

    for _ in range(30):
        n = RNG.randint(1, 12)
        edges = [(RNG.randrange(n), RNG.randrange(n), RNG.randrange(10)) for _ in range(RNG.randrange(35))]
        g = [[] for _ in range(n)]
        inf = 10**30
        dist = [[inf]*n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for a, b, cost in edges:
            g[a].append(b)
            g[b].append(a)
            dist[a][b] = min(dist[a][b], cost)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
        text = f"{n} {len(edges)}\n" + "".join(f"{a+1} {b+1} {c}\n" for a, b, c in edges)
        check("dijkstra", text, [-1 if d == inf else d for d in dist[0]])
        bfs = [-1]*n
        bfs[0] = 0
        q = deque([0])
        while q:
            v = q.popleft()
            for to in g[v]:
                if bfs[to] == -1:
                    bfs[to] = bfs[v]+1
                    q.append(to)
        text = f"{n} {len(edges)}\n" + "".join(f"{a+1} {b+1}\n" for a, b, c in edges)
        check("bfs", text, bfs)

        labels = list(range(n))
        queries, expected = [], []
        for i in range(100):
            t, a, b = RNG.randrange(2), RNG.randrange(n), RNG.randrange(n)
            queries.append(f"{t} {a} {b}\n")
            if t == 0:
                old, new = labels[b], labels[a]
                labels = [new if x == old else x for x in labels]
            else:
                expected.append(int(labels[a] == labels[b]))
        check("acl_dsu", f"{n} 100\n"+"".join(queries), expected)

        initial = [RNG.randint(-20, 20) for _ in range(n)]
        for kind in ["acl_fenwick", "acl_segtree"]:
            a = initial[:]
            queries, expected = [], []
            for i in range(100):
                if RNG.randrange(2) == 0:
                    p, x = RNG.randrange(n), RNG.randint(-20, 20)
                    queries.append(f"0 {p} {x}\n")
                    if kind == "acl_fenwick":
                        a[p] += x
                    else:
                        a[p] = x
                else:
                    l = RNG.randrange(n+1)
                    r = RNG.randint(l, n)
                    queries.append(f"1 {l} {r}\n")
                    expected.append(sum(a[l:r]) if kind == "acl_fenwick" else min(a[l:r], default=2**63-1))
            check(kind, f"{n} 100\n"+" ".join(map(str, initial))+"\n"+"".join(queries), expected)

    a, b = 1, 1
    for n in range(101):
        check("acl_modint", f"{n}\n", [a])
        a, b = b, (a+b) % 998244353

    data = json.loads((ROOT / "reference-data.json").read_text(encoding="utf-8"))
    items = [i for g in data["groups"] for i in g["items"]]
    # 全コードを別々の名前空間に置き、mainのみrunに改名して一括検証。
    # includeは外に出すが、本文・補助関数・型定義はそのままコンパイルする。
    includes = set()
    namespaces, runs = [], []
    for index, item in enumerate(items):
        full = item["full"]
        assert "int main()" in full and "#include" in full, item["id"]
        includes.update(re.findall(r"^#include[^\n]+", full, re.M))
        full = re.sub(r"^#include[^\n]+\n", "", full, flags=re.M)
        full = full.replace("int main()", "int run()", 1)
        # C++でmain末尾のreturn省略は許可される。改名したrunには明記する。
        last = full.rfind("}")
        full = full[:last]+"\nreturn 0;\n"+full[last:]
        namespaces.append(f"namespace example{index} {{\n{full}\n}}\n")
        if "sync_with_stdio" in full:
            continue  # 入出力バッファ設定の例は構文のみ検証
        inp = json.dumps(item.get("input", ""))
        expected = item.get("expected")
        compare = "" if expected is None else f"if(output.str() != {json.dumps(expected)}){{ cerr << \"Output mismatch: {item['id']}\\n\"; return 1; }}"
        runs.append(f"""{{
            istringstream input({inp}); ostringstream output;
            auto inbuf = cin.rdbuf(input.rdbuf()); auto outbuf = cout.rdbuf(output.rdbuf());
            cin.clear(); cout.clear();
            example{index}::run();
            cin.rdbuf(inbuf); cout.rdbuf(outbuf); cin.clear(); cout.clear();
            {compare}
        }}""")
    bundle = work / "all-examples.cpp"
    bundle.write_text("\n".join(sorted(includes))+"\nusing namespace std;\n"+"\n".join(namespaces)+
                      "\nint main(){\n"+"\n".join(runs)+"\nreturn 0;\n}\n", encoding="utf-8")
    binary = work / "all-examples"
    result = subprocess.run(["g++", "-std=c++17", "-O1", "-Werror=return-type", "-I", str(work),
                             str(bundle), "-o", str(binary)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    subprocess.run([str(binary)], check=True, timeout=20)
    print(f"PASS: {len(programs)} standalone files compiled; {count} randomized/boundary output checks; {len(items)} reference examples compiled; {len(runs)} examples executed")
    print(f"ACL revision: {commit}")
