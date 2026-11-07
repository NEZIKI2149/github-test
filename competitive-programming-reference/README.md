# C++ 競プロリファレンス

**ライブラリ名から操作を探し、必要な全体コードをコピーするための資料です。**

## ブラウザ用HTML

**[ブラウザ用リファレンスを開く](https://neziki2149.github.io/github-test/competitive-programming-reference/)**

GitHub Pages公開後に上のURLで閲覧できます。ローカルでは [index.html](index.html) をダウンロードし、ブラウザで開いても使えます。HTMLは1ファイルで完結し、閲覧・検索・コードの展開・コピーはブラウザ内で動作します。生成AIへの問い合わせや外部スクリプトの読み込みはありません。

- **標準ライブラリ**：容器と操作関数を分け、「日本語の機能 → 短いコード → 計算量」の順に掲載。
- **定番アルゴリズム**：名前と機能を1項目ずつ独立させ、読みの50音順に掲載。累積和・いもす法なども別項目。
- **全体コード**：アルゴリズムは「名前 → 目的 → 全体の時間・メモリ → 展開済みコード」の順に表示。標準ライブラリ・ACLは各操作の行をクリックして全体コードを開きます。`#include`・`main()`・必要な補助関数を含み、コピー・C++ファイルの保存に対応。
- **検索**：すべての分類から検索。`/` で検索欄に移動、`Esc` で検索解除。
- **項目の切り替え**：目次で選んだ1項目だけを本文に表示。選択中の目次はハイライトを保持し、別項目を選ぶと本文を切り替えます。検索結果も目次から1項目ずつ開きます。
- **表記**：添字は0始まり、区間は「l以上r未満」。数値の規模は `10²`・`2×10⁵` のように表記。

共通の前提はこのREADMEで確認できます。各項目の本文は選んだ内容から始まり、章タイトルや共通のバッジは繰り返し表示しません。和・積・距離などの計算結果は使用する型の範囲内に収め、到達できない地点を表す `INF` は、あり得る距離より大きい値を設定してください。

## GitHub上で読む

| 分類 | 内容 |
|---|---|
| **[標準ライブラリ](docs/standard-library.md)** | vector・string・set・mapなどの容器と、sort・reverse・二分探索などの操作関数。部分操作を含む主要操作 |
| **[AtCoder Library](docs/atcoder-library.md)** | DSU・Fenwick Tree・segtree・modintなど |
| **[定番アルゴリズム・実装](docs/algorithms.md)** | 累積和・全探索・座標圧縮・BFS・Dijkstra・DPなど。機能と全体コードが中心 |
| **[計算量・メモリの目安](docs/complexity-memory.md)** | Nと計算量の対応、型別・二次元配列の容量、メモリ上限との比較 |

## コードの使用

使用言語は **C++23 (GCC 15.2.0)**、ローカルのコンパイル設定は **`-std=gnu++23`** を前提とします。[AtCoder公式の言語・コンパイル設定](https://img.atcoder.jp/file/language-update/2025-10/language-list.html)

`bits/stdc++.h` はGCC系環境向けです。**ACLの例にはAtCoder Libraryのヘッダが別途必要です。** [コンパイル方法](examples/README.md) / [ACL公式ドキュメント](https://atcoder.github.io/ac-library/production/document_ja/index.html)

この資料のコードは生成AIを用いて事前作成しています。ABC・ARC・AGCでコピーして使用する場合、コンテスト開始前のWeb公開と、提出コードへの参照URLの添付が必要です。HTMLの全体コードには出典コメントを含めています。公開コミットの時刻が参加するコンテストの開始前であることを確認してください。[AtCoder公式ルール](https://info.atcoder.jp/entry/llm-rules-ja)

参照内容を固定する場合は、GitHubで対象ファイルを開き `y` キーでコミット固定URLを取得できます。

## 更新と検証

内容は `build_reference.py`、画面は `page-template.html` で管理します。生成物を直接変更するのではなく、次のコマンドでHTML・Markdown・検証データをまとめて生成します。

```sh
python build_reference.py
```

全コードの検証（WSL/Linux、Python3・g++・インターネット接続が必要）：

```sh
python3 validate.py
```

検証スクリプトは公式ACLを一時フォルダへ取得します。203件の全体コードを、それぞれの本文を別の名前空間に置いてC++23 (GCC 15.2.0)で一括コンパイルし、入出力設定だけの1件を除く202件を実行します。単独cppファイル7本のコンパイルと、355ケースの境界値・ランダム入力の出力照合も行います。すべての入力や手法を網羅する検証ではありません。

GitHub Pagesの初回設定は、[Settings → Pages](https://github.com/NEZIKI2149/github-test/settings/pages)で **Deploy from a branch → master → /(root) → Save**。リポジトリ直下の入口から、この資料へ移動する構成です。
