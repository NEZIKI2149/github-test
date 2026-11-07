# 入出力まで揃ったコード例

**各cppファイルは単独でコンパイルして実行できます。** 入力形式はそれぞれのファイルの冒頭にも書いてあります。問題ごとの入力形式・有向/無向・添字の始まりに合わせて変更してください。

| ファイル | 処理 | 入力の要点 |
|---|---|---|
| [binary_search.cpp](binary_search.cpp) | x² ≥ K の最小整数x | Kのみ。1 ≤ K ≤ 10¹⁸ |
| [bfs.cpp](bfs.cpp) | 無向グラフの最短距離 | N M、M本の辺。頂点1始まり |
| [dijkstra.cpp](dijkstra.cpp) | 非負重みの有向グラフの最短距離 | N M、M本の a b cost。頂点1始まり |
| [acl_dsu.cpp](acl_dsu.cpp) | グループ結合・連結判定 | N Q、Q個の t a b。頂点0始まり |
| [acl_fenwick.cpp](acl_fenwick.cpp) | 1点加算・区間和 | N Q、配列、Q個の操作。添字0始まり |
| [acl_segtree.cpp](acl_segtree.cpp) | 1点代入・区間最小値 | N Q、配列、Q個の操作。添字0始まり |
| [acl_modint.cpp](acl_modint.cpp) | 階段DPを998244353で割った余り | Nのみ |

### コンパイル例（WSL / Linux、examplesフォルダで実行）

```sh
g++ -std=gnu++23 -O2 -Wall -Wextra bfs.cpp -o bfs
./bfs
```

ACLの例では、別途ACLのヘッダが必要です。たとえば `~/ac-library/atcoder/dsu` がある場合：

```sh
g++ -std=gnu++23 -O2 -Wall -Wextra -I "$HOME/ac-library" acl_dsu.cpp -o acl_dsu
./acl_dsu
```

`-I` には **atcoderフォルダ自身ではなく、その親フォルダ** を指定します。

### 全例の再検証

Python3・g++・インターネット接続があるWSL/Linux環境で、親フォルダにある `validate.py` を実行します。

```sh
python3 ../validate.py
```

公式GitHubからACLを一時フォルダに取得し、7本のコンパイルと境界値・ランダム入力の出力照合を行います。HTML・Markdownに掲載中の全体コードも一括コンパイルし、実行可能な例を動かします。ヘッダと実行ファイルは検証終了時に削除します。すべての入力を網羅するテストではありません。
