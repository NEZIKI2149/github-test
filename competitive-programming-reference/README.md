# 競プロ C++ 本番リファレンス

**やりたい操作を早見表で探し、該当するコードを使うための資料です。**

APG4bに近い書き方・C++17以降を基本にしています。`Ctrl+F` で「二分探索」「重複」「最小」「BFS」などを検索してください。

## 公開URLと本番での使用

公開先：[競プロ C++ 本番リファレンス](https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference)

**この資料のコードは生成AIを用いて作成しています。** ABC・ARC・AGCの本番でコードをコピーして使用する場合、現行ルールでは「コンテスト開始前のWeb公開」と「提出コードへの参照URLの添付」が必要です。公開コミットの時刻が参加するコンテストの開始前であることを確認してください。[AtCoder公式ルール（20261014版）](https://info.atcoder.jp/entry/llm-rules-ja#コンテスト開始前に生成AIで作成されたコードについて)

提出コードには、次のコメントを添付できます。参照内容を固定するには、GitHubで対象ファイルを開き `y` キーを押して取得できるコミット固定URLに置き換えます。

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
```

本番中の生成AIへの質問・コード修正依頼などは、この事前作成コードの許容とは別で、原則禁止です。ルールは変更されることがあるため、参加時点の規定を確認してください。

## 目次

- [やりたいことから探す](#やりたいことから探す)
- [基本テンプレート・計算量・数値](#基本テンプレート計算量数値)
- [vector：配列](#vector配列)
- [string：文字列](#string文字列)
- [sort・reverse・unique：並べ替えと重複削除](#sortreverseunique並べ替えと重複削除)
- [min・max・集計](#minmax集計)
- [lower_bound・upper_bound：二分探索](#lower_boundupper_bound二分探索)
- [set・multiset：順序つきの集合](#setmultiset順序つきの集合)
- [map：値ごとの情報](#map値ごとの情報)
- [queue・stack・deque：取り出す順番](#queuestackdeque取り出す順番)
- [priority_queue：最大・最小を繰り返し取る](#priority_queue最大最小を繰り返し取る)
- [pair・tuple・添字のソート](#pairtuple添字のソート)
- [数・文字・出力](#数文字出力)
- [順列・bit全探索](#順列bit全探索)
- [累積和・いもす法](#累積和いもす法)
- [座標圧縮](#座標圧縮)
- [答えに対する二分探索](#答えに対する二分探索)
- [しゃくとり法](#しゃくとり法)
- [グラフ：BFS・Dijkstra・トポロジカルソート](#グラフbfsdijkstraトポロジカルソート)
- [DP：状態・遷移・初期値](#dp状態遷移初期値)
- [AtCoder Library：DSU・Fenwick Tree・segtree・modint](#atcoder-library)
- [提出前チェック](#提出前チェック)

## やりたいことから探す

`N` は要素数、`M` は辺数、`Q` は質問数です。表の計算量は、特記がなければ1操作あたりです。

| やりたいこと | 選ぶもの・書き方 | 計算量・条件 |
|---|---|---|
| 添字で配列を読む・書く | `vector` / `A.at(i)` | O(1) |
| 末尾に追加 | `A.push_back(x)` | ならし O(1) |
| 昇順・降順に並べる | `sort` | O(N log N) |
| 配列を逆順にする | `reverse` | O(N) |
| 最大値・最小値を1回求める | `max_element` / `min_element` | O(N) |
| 値が何個あるか1回数える | `count` | O(N) |
| ソート済み配列で x 以上の最初の位置 | `lower_bound` | O(log N) |
| ソート済み配列で x より大きい最初の位置 | `upper_bound` | O(log N) |
| 重複なしで値を持つ | `set` | 追加・検索・削除 O(log N) |
| 重複ありで値を持ち、近い値を探す | `multiset` | 追加・検索・1個削除 O(log N) |
| 値ごとの出現回数 | 小さい非負整数なら `vector<int> cnt`、それ以外は `map` | O(1) / O(log N) |
| 追加順に取り出す | `queue` | O(1) |
| 最後に追加したものを取り出す | `stack` | O(1) |
| 両端から追加・削除 | `deque` | O(1) |
| 最大値・最小値を繰り返し取り出す | `priority_queue` | 追加・削除 O(log N)、参照 O(1) |
| 配列を変更せず区間和を何度も求める | 累積和 | 前処理 O(N)、質問 O(1) |
| 区間加算を全部行った後の値 | いもす法 | 更新 O(1)、最後に O(N) |
| 大きい値を大小関係を保って小さい番号にする | 座標圧縮 | 全体 O(N log N) |
| 単調な条件を満たす最小値 | 答えに対する二分探索 | O(判定の計算量 × log 探索幅) |
| 同じグループか判定・グループを結合 | ACL `dsu`（Union-Find） | ならし O(α(N))、ほぼ定数 |
| 1点に加算しながら区間和 | ACL `fenwick_tree` | O(log N) |
| 1点を変更しながら区間の最小・最大・和 | ACL `segtree` | O(log N) |
| 余りを取りながら計算 | ACL `modint` | 加減乗 O(1)、累乗 O(log 指数) |
| 重みなしグラフの最短距離 | BFS | 全体 O(N+M) |
| 重みがすべて非負のグラフの最短距離 | Dijkstra | この資料の実装は O((N+M) log(N+M)) |
| 前後関係を守った順番・有向閉路判定 | トポロジカルソート | 全体 O(N+M) |
| 全選択パターンを試す | bit全探索 | 典型的に O(N × 2^N) |
| 全並べ替えを試す | `next_permutation` | 典型的に O(N × N!) |

「ならし」は、多数回の操作をまとめて見たときの1回あたりの計算量です。

## 基本テンプレート・計算量・数値

### 最初に貼るコード

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<int> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }

    long long ans = 0;
    for(int i = 0;i < N;i++){
        ans += A.at(i);
    }
    cout << ans << endl;
}
```

以下の短いコードは、特記がなければ `main()` の中に置く部分コードです。実行できる全体例は [examples](examples) にあります。`#include <bits/stdc++.h>` はGCC系の競プロ環境向けです。

大量の入出力がある場合は、`main()` の先頭に次を置き、繰り返し出力には `endl` の代わりに `'\n'` を使います。`endl` は毎回出力を確定させるため、大量出力では遅くなります。対話問題では問題の指示どおり出力を確定させてください。

```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

### 制約から候補を絞る

**制限時間・処理内容・定数倍で変わるので、以下は目安です。**

| 規模 | 候補 |
|---|---|
| N ≤ 8〜10 程度 | 順列全探索 O(N × N!) |
| N ≤ 20 程度 | bit全探索 O(N × 2^N) |
| N ≤ 3000 程度 | O(N²) |
| N ≤ 2×10^5 程度 | O(N log N)、O(N) |
| 値が 10^9〜10^18 程度 | 値を1ずつ全探索せず、二分探索・数式などを検討 |

### int / long long / INF

```cpp
int N = 200000;
long long ans = 1LL * N * (N-1) / 2;
const long long INF = (1LL << 60);
```

- `int` は約 ±21億、`long long` は約 ±9×10^18 まで。
- **代入先が `long long` でも、`int * int` は先に `int` で計算されます。** `1LL * A * B` とします。
- `INF` は「あり得る答えより大きく、加算しても型からあふれない値」を選びます。上の値が常に十分とは限りません。
- `A.size()` は符号なし整数です。引き算や逆向きループでは `int N = A.size();` としてから使うと扱いやすくなります。
- 区間 `[l, r)` は **l を含み、r を含まない** 区間です。`[2, 5)` は添字2, 3, 4、長さは `r-l` です。

## vector：配列

```cpp
vector<int> A(5, 0);                 // 0が5個
vector<vector<int>> B(3, vector<int>(4, -1)); // 3行4列
A.at(2) = 10;
A.push_back(7);                      // 末尾追加
int x = A.back();                    // 最後の値
A.pop_back();                        // 最後を削除。値は返さない
int N = A.size();
bool empty = A.empty();
A.resize(8, -1);                     // 新しく増えた要素を-1にする
A.assign(5, 2);                      // 全体を「2が5個」に置き換える
fill(A.begin(), A.end(), 0);         // 要素数を変えず、全部0にする
```

**`reserve(N)` は容量の確保で、要素数を N にしません。** `A.at(i)` で書くなら `vector<int> A(N);` または `resize` が必要です。

| 操作 | 計算量・注意 |
|---|---|
| `A.at(i)` / `A.front()` / `A.back()` | O(1)。空の配列の front/back は使えない |
| `push_back` | ならし O(1) |
| `pop_back` | O(1)。空の配列には使えない |
| `A.erase(A.begin()+i)` | O(N)。後ろの要素が左にずれる |
| `A.insert(A.begin()+i, x)` | O(N) |
| `A = B` | O(B.size())。配列全体のコピー |

関数に配列を渡して読むだけなら `const vector<int>& A` とします。`&` はコピーせず元の配列を参照する指定、`const` は関数内で変更しない指定です。

## string：文字列

```cpp
string S = "abcabc";
char c = S.at(0);               // 'a'
string T = S.substr(1, 3);      // "bca"。開始位置1から3文字
S += 'x';                      // 末尾に1文字追加
S += "yz";                     // 末尾に文字列追加
S.pop_back();                  // 最後の1文字を削除。空なら使わない
size_t p = S.find("bc");        // 最初に出る位置。なければ string::npos
if(p != string::npos){
    cout << p << endl;
}
int digit = '7' - '0';          // 文字の数字 → 整数7
int index = 'c' - 'a';          // 英小文字 → 0始まりの番号2
long long x = stoll("12345678900");
string U = to_string(x);
```

- `substr(開始位置, 文字数)` です。第2引数は終点ではありません。作る文字数ぶんのコピー時間がかかります。
- `find` の結果は `string::npos` と比較します。見つからないときに `S.at(p)` を読まないでください。
- `stoi` は `int`、`stoll` は `long long` に変換します。範囲外・数字でない文字列では失敗します。
- 空白を含む1行は `getline(cin, S)`。直前に `cin >> N` がある場合、行末まで読み捨ててから使います。

```cpp
int N;
cin >> N;
cin.ignore(numeric_limits<streamsize>::max(), '\n');
string S;
getline(cin, S); // 次の行。空行や先頭の空白も残す
```

## sort・reverse・unique：並べ替えと重複削除

```cpp
vector<int> A = {3, 1, 3, 2};
sort(A.begin(), A.end());                  // 1, 2, 3, 3
sort(A.begin(), A.end(), greater<int>());  // 3, 3, 2, 1
reverse(A.begin(), A.end());               // 現在の並びを反転
```

**並べ替えで元の位置の情報が失われます。必要ならコピーか、値と元の添字の組を使います。**

重複を消すときは、先にソートして同じ値を隣同士にします。

```cpp
sort(A.begin(), A.end());
A.erase(unique(A.begin(), A.end()), A.end()); // 1, 2, 3
```

`unique` だけでは配列は短くなりません。重複を詰めた後の「新しい終端」を返すので、`erase` で不要な末尾を消します。全体 O(N log N) です。

部分区間だけ並べる場合も右端は含みません。

```cpp
// 0 <= l <= r <= A.size() が必要
sort(A.begin()+l, A.begin()+r); // 添字 l〜r-1 を並べる
```

## min・max・集計

```cpp
vector<int> A = {4, 1, 7};
int x = min(3, 5);
int y = max({3, 5, 2});
swap(x, y);
int mn = *min_element(A.begin(), A.end()); // 1
int mx = *max_element(A.begin(), A.end()); // 7
int pos = min_element(A.begin(), A.end()) - A.begin(); // 1
long long sum = accumulate(A.begin(), A.end(), 0LL);  // 12
int cnt = count(A.begin(), A.end(), 4);               // 1
auto it = find(A.begin(), A.end(), 7);
if(it != A.end()){
    cout << it - A.begin() << endl;
}
```

- `*it` は、その位置にある値を読む書き方です。`end()` は末尾の1つ先なので `*A.end()` は読めません。
- **空の配列で `*min_element(...)` / `*max_element(...)` を使わないでください。**
- `accumulate(..., 0)` は `int` で合計します。大きい和には `0LL`。
- `min` / `max` の2引数は型をそろえます。例：`max(0LL, x)`（x が long long の場合）。
- 最大・最小・合計・`count`・`find` は配列を1周するので O(N)。質問ごとに呼ぶと O(NQ) になります。

## lower_bound・upper_bound：二分探索

**昇順にソート済みの配列で、値を挿入できる境界の位置を探します。返るものは値そのものではなく「位置を指すもの」です。**

```cpp
vector<int> A = {1, 3, 3, 7};
int x = 3;
int l = lower_bound(A.begin(), A.end(), x) - A.begin(); // 1
int r = upper_bound(A.begin(), A.end(), x) - A.begin(); // 3
cout << r-l << endl; // xの個数 = 2
```

| 求めたいもの | 書き方 |
|---|---|
| x 以上の最初の位置 | `lower_bound(...) - A.begin()` |
| x より大きい最初の位置 | `upper_bound(...) - A.begin()` |
| x 未満の個数 | `lower_bound(...) - A.begin()` |
| x 以下の個数 | `upper_bound(...) - A.begin()` |
| x 以上の個数 | `N - (lower_bound(...) - A.begin())` |
| x より大きい個数 | `N - (upper_bound(...) - A.begin())` |
| x の個数 | `upper_bound(...) - lower_bound(...)` |
| x があるか | `binary_search(A.begin(), A.end(), x)` |

位置が `N` なら条件を満たす値はありません。値を読む前に確認します。

```cpp
int N = A.size();
int p = lower_bound(A.begin(), A.end(), x) - A.begin();
if(p < N){
    cout << A.at(p) << endl; // x以上で最小の値
}
if(p > 0){
    cout << A.at(p-1) << endl; // x未満で最大の値
}
```

`upper_bound` の位置から1つ戻れば「x 以下で最大」です。各探索は O(log N)、最初のソートは O(N log N) です。

## set・multiset：順序つきの集合

### set：同じ値を1個だけ持つ

```cpp
set<int> S;
S.insert(5);
S.insert(2);
S.insert(5);                  // 5は増えない
bool exists = S.count(5) > 0;
S.erase(5);                  // 5があれば削除
if(!S.empty()){
    cout << *S.begin() << endl;  // 最小値
    cout << *S.rbegin() << endl; // 最大値
}
for(auto it = S.begin();it != S.end();it++){
    cout << *it << endl;      // 小さい順
}
```

`set` は添字で読めません。`S.at(i)` や `S[i]` はありません。

### x 以上で最小 / x 未満で最大

```cpp
set<int> S = {2, 5, 9};
int x = 6;
auto it = S.lower_bound(x);
if(it != S.end()){
    cout << *it << endl;     // 9
}
if(it != S.begin()){
    it--;
    cout << *it << endl;     // 5
}
```

**set / multiset では `S.lower_bound(x)` を使います。** 一般の `lower_bound(S.begin(), S.end(), x)` は移動に O(N) かかります。`set` 内の「x未満の個数」を距離で数える処理も O(N) です。

### multiset：同じ値を複数持つ

```cpp
multiset<int> S = {2, 5, 5, 9};
auto it = S.find(5);
if(it != S.end()){
    S.erase(it);            // 5を1個だけ削除
}
S.erase(5);                 // 残っている5を全部削除
```

`erase(x)` は同じ値を全部消します。**1個だけ消すなら `find` → 存在確認 → `erase(it)`。** `count(x)` は O(log N + xの個数)、`erase(x)` は O(log N + 削除数) です。

## map：値ごとの情報

**`map<キーの型, 値の型>` は、キーごとに1つの値を持ちます。** 出現回数なら「数 → 回数」です。

```cpp
vector<int> A = {5, 2, 5};
map<int, long long> cnt;
for(int i = 0;i < (int)A.size();i++){
    cnt[A.at(i)]++;
}
cout << cnt[5] << endl;      // 2
bool exists = cnt.count(9) > 0; // 存在確認。要素を追加しない
for(auto it = cnt.begin();it != cnt.end();it++){
    int x = it->first;           // キー
    long long num = it->second;  // 値
    cout << x << " " << num << endl;
}
```

- **`cnt[x]` は、x がないと値0の要素を作ります。** 存在確認だけなら `count` / `find`。
- `cnt.size()` は現在あるキーの種類数です。`cnt[x]--` で値が0になってもキーは残ります。必要なら `cnt.erase(x)`。
- `map` はキーの小さい順。追加・参照・削除は O(log N)。文字列キーなら比較の文字数も考慮します。
- `map<string, int>` のように文字列もキーにできます。
- 値の範囲が `0〜200000` など小さいなら `vector<int> cnt(200001, 0);` のほうが簡単で高速です。
- `unordered_map` / `unordered_set` は順序なし、検索などは平均 O(1)、最悪 O(N)。`lower_bound` は使えません。通常は `map` / `set` を基準に選べます。

同じ値のペア数は、各出現回数 `num` に対して `num*(num-1)/2` を合計します。`num` は `long long` にします。

## queue・stack・deque：取り出す順番

```cpp
queue<int> Q;       // 先に入れたものが先
Q.push(3);
Q.push(7);
int x = Q.front();  // 3
Q.pop();           // 3を削除。値は返さない

stack<int> S;       // 後に入れたものが先
S.push(3);
S.push(7);
int y = S.top();    // 7
S.pop();

deque<int> D;
D.push_back(3);
D.push_front(7);    // 7, 3
int z = D.front();  // 7
D.pop_front();
D.pop_back();
```

**読む・削除する前に、空でないことを確認します。** `while(!Q.empty())` が基本形です。`queue` / `stack` に添字アクセスはありません。`deque` は `D.at(i)` も使えます。

## priority_queue：最大・最小を繰り返し取る

```cpp
priority_queue<int> Q; // 最大値が先
Q.push(3);
Q.push(7);
cout << Q.top() << endl; // 7
Q.pop();

priority_queue<int, vector<int>, greater<int>> R; // 最小値が先
R.push(3);
R.push(7);
cout << R.top() << endl; // 3
```

追加・削除は O(log N)、先頭の参照は O(1)。途中の値を自由に削除・変更する操作はありません。必要なら `multiset` を検討します。

「小さいものをK個だけ保持」なら、最大値を先に取り出す `priority_queue` に入れ、サイズがKを超えたら最大値を捨てます。最後の `top()` が保持しているK個の最大、つまり全体のK番目に小さい値です（要素数がK以上必要）。

## pair・tuple・添字のソート

```cpp
pair<int, int> P = {3, 7};
cout << P.first << " " << P.second << endl;
vector<pair<int, int>> A = {{2, 8}, {1, 9}, {2, 3}};
sort(A.begin(), A.end()); // (1,9), (2,3), (2,8)
```

`pair` は first の昇順、同じなら second の昇順です。`tuple` は3項目以上をまとめ、先頭から順に比較します。

```cpp
tuple<int, int, int> T = {2, 5, 8};
cout << get<0>(T) << endl; // 2
auto [a, b, c] = T;       // C++17。中身に名前をつける
```

### 元の添字を残して、値の降順・同値なら添字の昇順

```cpp
vector<int> A = {30, 10, 30};
int N = A.size();
vector<int> order(N);
iota(order.begin(), order.end(), 0); // 0,1,...,N-1
sort(order.begin(), order.end(), [&](int i, int j){
    if(A.at(i) != A.at(j)){
        return A.at(i) > A.at(j);
    }
    return i < j;
}); // order = {0, 2, 1}
```

`[&](int i, int j){...}` はその場で比較用の関数を作る書き方です。`[&]` により外の `A` を参照できます。`true` は「iをjより前に置く」を意味します。**比較に `<=` / `>=` を使って同じもの同士でも true にすると、sort の前提を破ります。**

## 数・文字・出力

```cpp
long long a = 12, b = 18;
long long g = gcd(a, b); // 6。C++17
long long l = lcm(a, b); // 36。結果が型に収まる必要がある
long long d = abs(a-b);
double x = sqrt(2.0);
cout << fixed << setprecision(10) << x << endl;
```

### 割り算・余り

```cpp
long long a = 17, b = 5; // a >= 0, b > 0
long long floor_value = a / b;               // 3
long long ceil_value = a / b + (a % b != 0); // 4。a+b-1のあふれを避ける
long long x = -3, MOD = 5;                  // MOD > 0
long long r = x % MOD;
if(r < 0){
    r += MOD;                               // 2。0以上MOD未満にそろえる
}
```

C++の整数除算は0に近い側に切り捨てます。負数を含む場合、上の切り上げ式や数学の床関数と同じとは限りません。`pow(a,b)` は浮動小数点計算なので、整数の累乗を厳密に求める用途には使わないのが基本です。

### 約数列挙：O(√N)（N ≥ 1）

```cpp
long long N = 36;
vector<long long> D;
for(long long x = 1;x <= N/x;x++){
    if(N % x == 0){
        D.push_back(x);
        if(x != N/x){
            D.push_back(N/x);
        }
    }
}
sort(D.begin(), D.end());
```

`x <= N/x` は `x*x <= N` と同じ判定を、積のあふれを避けて行います。

### 素数判定：O(√N)

次の関数は **main の外** に置きます。Nが10^18級なら試し割りは遅すぎる場合があります。

```cpp
bool is_prime(long long N){
    if(N < 2){
        return false;
    }
    for(long long x = 2;x <= N/x;x++){
        if(N % x == 0){
            return false;
        }
    }
    return true;
}
```

### 素因数分解：O(√N)（N ≥ 1）

```cpp
long long N = 360;
vector<pair<long long, int>> factors;
for(long long x = 2;x <= N/x;x++){
    int cnt = 0;
    while(N % x == 0){
        N /= x;
        cnt++;
    }
    if(cnt > 0){
        factors.push_back({x, cnt});
    }
}
if(N > 1){
    factors.push_back({N, 1});
}
// factors = {(2,3), (3,2), (5,1)}。N自体は途中で変更される
```

## 順列・bit全探索

### 全順列

```cpp
vector<int> A = {0, 1, 2};
sort(A.begin(), A.end());
do{
    // この順番の A を調べる
}while(next_permutation(A.begin(), A.end()));
```

**全パターンを出すには昇順から始め、最初の並びも処理するため do-while を使います。** 重複値がある場合、同じ値の並びは重複して出ません。

### bit全探索：各要素を選ぶ / 選ばない

```cpp
vector<int> A = {2, 3, 5};
int N = A.size();
long long K = 5;
long long ans = 0;
for(long long bit = 0;bit < (1LL << N);bit++){
    long long sum = 0;
    for(int i = 0;i < N;i++){
        if((bit >> i) & 1LL){ // i番目を選んでいる
            sum += A.at(i);
        }
    }
    if(sum == K){
        ans++;
    }
}
cout << ans << endl; // {2,3} と {5} の2通り
```

空集合も含みます。O(N × 2^N)。`1LL << N` はこの用途では `0 <= N <= 62` が型上の条件ですが、全探索が現実的なのは典型的にはNが20前後です。

## 累積和・いもす法

### 累積和：更新なしの区間和

```cpp
vector<int> A = {3, 1, 4, 2};
int N = A.size();
vector<long long> S(N+1, 0);
for(int i = 0;i < N;i++){
    S.at(i+1) = S.at(i) + A.at(i);
}
int l = 1, r = 3;
long long ans = S.at(r) - S.at(l); // A[1]+A[2] = 5
```

**`S[i]` は「先頭から i 個の和」です。`[l,r)` の和は `S[r]-S[l]`。** 前処理 O(N)、質問 O(1)、メモリ O(N)。配列を変更したら、この累積和はそのまま使えません。

問題の添字が1始まりで「L番目〜R番目を両端含む」なら、答えは `S.at(R)-S.at(L-1)` です。

### いもす法：区間に加算し、最後にまとめて復元

```cpp
int N = 5;
vector<long long> D(N+1, 0);
int l = 1, r = 4;
long long x = 3;
D.at(l) += x; // [l,r) にxを加算
D.at(r) -= x;
for(int i = 0;i < N;i++){
    if(i > 0){
        D.at(i) += D.at(i-1);
    }
    cout << D.at(i) << endl; // 0,3,3,3,0
}
```

更新のたびに途中の区間和を聞かれる場合には、この形では対応できません。

## 座標圧縮

**値の大小・一致だけが必要なとき、値を0始まりの順位に置き換えます。数値の差そのものは保ちません。**

```cpp
vector<long long> A = {100, 5, 100, 20};
vector<long long> B = A;
sort(B.begin(), B.end());
B.erase(unique(B.begin(), B.end()), B.end()); // 5,20,100
int N = A.size();
vector<int> C(N);
for(int i = 0;i < N;i++){
    C.at(i) = lower_bound(B.begin(), B.end(), A.at(i)) - B.begin();
}
// C = {2,0,2,1}。元の値は B.at(C.at(i))
```

O(N log N)。距離・区間の長さが必要な問題で、圧縮後の番号の差を元の距離として使わないでください。

## 答えに対する二分探索

**「x が条件を満たすなら、それより大きい値も満たす」という単調性があるとき、条件を満たす最小の整数を探せます。**

例：正の整数Kに対し、`x*x >= K` となる最小の非負整数x。積のあふれを避けて割り算で判定します。

```cpp
long long K = 20; // 1 <= K <= 10^18
long long ng = 0; // 条件を満たさない
long long ok = K; // 条件を満たす
while(ok-ng > 1){
    long long mid = ng + (ok-ng)/2;
    long long required = K/mid + (K % mid != 0);
    if(mid >= required){ // mid*mid >= K と同じ
        ok = mid;
    }
    else{
        ng = mid;
    }
}
cout << ok << endl; // 5
```

毎回、`ok` は条件を満たし、`ng` は満たさない状態を保ちます。差が1になれば境界が確定します。問題に合わせて **判定の中身と最初のok/ngを両方変更** します。条件を満たす値がない場合やK=0は別途設計が必要です。全体例：[binary_search.cpp](examples/binary_search.cpp)。

## しゃくとり法

例：**全要素が非負** の配列で、区間和がK以下になる空でない連続部分列の数を求めます（K ≥ 0）。

```cpp
vector<int> A = {2, 1, 3};
int N = A.size();
long long K = 3, sum = 0, ans = 0;
int r = 0;
for(int l = 0;l < N;l++){
    while(r < N && sum + A.at(r) <= K){
        sum += A.at(r);
        r++;
    }
    ans += r-l; // 左端がlの有効な空でない区間数
    if(r == l){
        r++; // A[l]すら入らなかった。sumは0のまま
    }
    else{
        sum -= A.at(l);
    }
}
cout << ans << endl; // 4
```

右端rが後戻りせず、全体 O(N) です。負数があると「右に伸ばすと和が減らない」という性質が崩れるため、この方法は使えません。

## グラフ：BFS・Dijkstra・トポロジカルソート

### グラフの入力

```cpp
int N, M;
cin >> N >> M;
vector<vector<int>> G(N);
for(int i = 0;i < M;i++){
    int a, b;
    cin >> a >> b;
    a--; b--;               // 入力が1始まりの場合
    G.at(a).push_back(b);
    G.at(b).push_back(a);    // 有向グラフなら、この行は書かない
}
```

### BFS：すべての辺を1回の移動として扱う最短距離

```cpp
vector<int> dist(N, -1); // -1は未訪問・到達不可
queue<int> Q;
dist.at(0) = 0;
Q.push(0);
while(!Q.empty()){
    int v = Q.front();
    Q.pop();
    for(int i = 0;i < (int)G.at(v).size();i++){
        int to = G.at(v).at(i);
        if(dist.at(to) != -1){
            continue;
        }
        dist.at(to) = dist.at(v)+1;
        Q.push(to);
    }
}
```

**queueに入れるときに訪問済みにします。** 取り出すときまで待つと重複登録が増えます。O(N+M)。全体例：[bfs.cpp](examples/bfs.cpp)。

### グリッドの4方向

```cpp
vector<int> dh = {1, 0, -1, 0};
vector<int> dw = {0, 1, 0, -1};
for(int k = 0;k < 4;k++){
    int nh = h + dh.at(k);
    int nw = w + dw.at(k);
    if(nh < 0 || nh >= H || nw < 0 || nw >= W){
        continue;
    }
    if(S.at(nh).at(nw) == '#'){
        continue;
    }
    // 移動できるマス(nh,nw)の処理
}
```

h,wは現在位置、H,Wは盤面サイズ、Sは `vector<string>` の盤面です。添字で読む前に範囲を確認します。

### Dijkstra：辺の重みがすべて非負

**負の重みがあるグラフには使いません。重みが全部1ならBFSのほうが簡単です。**

`G[v]` に `{行き先, 重み}` を入れた `vector<vector<pair<int,long long>>> G` を使います。

```cpp
const long long INF = (1LL << 60);
vector<long long> dist(N, INF);
priority_queue<pair<long long, int>, vector<pair<long long, int>>,
               greater<pair<long long, int>>> Q;
dist.at(0) = 0;
Q.push({0, 0}); // {距離, 頂点}
while(!Q.empty()){
    long long d = Q.top().first;
    int v = Q.top().second;
    Q.pop();
    if(d != dist.at(v)){
        continue; // 更新前の古い候補を捨てる
    }
    for(int i = 0;i < (int)G.at(v).size();i++){
        int to = G.at(v).at(i).first;
        long long cost = G.at(v).at(i).second;
        if(dist.at(to) > d+cost){
            dist.at(to) = d+cost;
            Q.push({dist.at(to), to});
        }
    }
}
```

この実装は辺ごとに候補を追加するため O((N+M) log(N+M)) 時間、O(N+M) メモリ。多重辺のない通常のグラフでは O((N+M) log N) とも表せます。有限の最短距離がINF未満、`d+cost` が long long に収まることを確認します。全体例：[dijkstra.cpp](examples/dijkstra.cpp)。

### トポロジカルソート：前後関係を守る並び

有向グラフで「aをbより先に処理する」なら a → b の辺を張ります。`indeg[v]` はvへ入る辺数です。

```cpp
vector<int> indeg(N, 0);
for(int v = 0;v < N;v++){
    for(int i = 0;i < (int)G.at(v).size();i++){
        indeg.at(G.at(v).at(i))++;
    }
}
queue<int> Q;
for(int v = 0;v < N;v++){
    if(indeg.at(v) == 0){
        Q.push(v);
    }
}
vector<int> order;
while(!Q.empty()){
    int v = Q.front();
    Q.pop();
    order.push_back(v);
    for(int i = 0;i < (int)G.at(v).size();i++){
        int to = G.at(v).at(i);
        indeg.at(to)--;
        if(indeg.at(to) == 0){
            Q.push(to);
        }
    }
}
bool has_cycle = (int)order.size() != N;
```

O(N+M)。有向閉路があれば全頂点を並べられません。辞書順最小の並びが必要なら、queueを最小値優先のpriority_queueに変更し、計算量は O(M+N log N) になります。

## DP：状態・遷移・初期値

**DPには万能な1つの呼び出し方はありません。何を `dp` に記録するか、どこから更新するか、最初に何を入れるかを決めます。**

### 1段 / 2段で階段を上る場合の数

- 状態：`dp[i]` = i段目からN段目へ到達する方法の数。
- 初期値：`dp[N]=1`（すでに到達している1通り）、`dp[N+1]=0`。
- 遷移：`dp[i]=dp[i+1]+dp[i+2]`。
- 計算順：iを大きいほうから小さいほうへ。O(N)時間・O(N)メモリ。

```cpp
int N = 5; // このlong long版は 0 <= N <= 91
vector<long long> dp(N+2, 0);
dp.at(N) = 1;
for(int i = N-1;i >= 0;i--){
    dp.at(i) = dp.at(i+1) + dp.at(i+2);
}
cout << dp.at(0) << endl; // 8
```

場合の数が大きい問題では、指定された余りを取ります。

### LIS：狭義単調増加部分列の最大長（O(N²)）

部分列は元の順序を守って一部を選ぶもので、連続している必要はありません。

- 状態：`dp[i]` = A[i]を最後に選ぶ増加部分列の最大長。
- 初期値：すべて1。
- 遷移：`j < i && A[j] < A[i]` なら `dp[i]=max(dp[i],dp[j]+1)`。
- 答え：dpの最大値。N=3000程度なら候補、N=2×10^5なら別の高速化が必要です。

```cpp
vector<int> A = {3, 1, 2, 5};
int N = A.size();
vector<int> dp(N, 1);
int ans = 0;
for(int i = 0;i < N;i++){
    for(int j = 0;j < i;j++){
        if(A.at(j) < A.at(i)){
            dp.at(i) = max(dp.at(i), dp.at(j)+1);
        }
    }
    ans = max(ans, dp.at(i));
}
cout << ans << endl; // 3
```

長さだけなら、次の `lower_bound` を使う方法で O(N log N) にできます。

```cpp
vector<int> tail;
for(int i = 0;i < N;i++){
    auto it = lower_bound(tail.begin(), tail.end(), A.at(i));
    if(it == tail.end()){
        tail.push_back(A.at(i));
    }
    else{
        *it = A.at(i);
    }
}
cout << tail.size() << endl;
```

`tail[k]` は「長さk+1の増加部分列の末尾として可能な最小値」です。**tail全体が実際の部分列とは限りません。** 同じ値も続けてよい非減少部分列なら `upper_bound` に変えます。

## AtCoder Library

**C++標準ライブラリとは別の追加ライブラリです。利用環境にACLのヘッダが必要です。** `bits/stdc++.h` だけでは読み込まれません。ローカルで見つからない場合は、`atcoder` フォルダの親をコンパイラのinclude先に指定します。詳細は[公式の導入説明](https://atcoder.github.io/ac-library/production/document_ja/index.html)。

```cpp
#include <bits/stdc++.h>
#include <atcoder/all>
using namespace std;
// この資料では atcoder:: をつけて呼ぶ
```

### DSU / Union-Find：グループをつなぐ

```cpp
atcoder::dsu D(5);        // 頂点0〜4。最初は全部別グループ
D.merge(0, 1);
D.merge(1, 3);
bool same = D.same(0, 3); // true
int num = D.size(0);     // 3
int root = D.leader(3);  // グループの代表頂点
```

**辺の追加と連結判定に使い、辺の削除・最短距離には使えません。** 代表頂点は最小番号とは限らず、結合すると変わることがあります。

構築 O(N)、各操作はならし O(α(N))。`D.groups()` はグループ一覧の `vector<vector<int>>` を返し O(N)。全体例：[acl_dsu.cpp](examples/acl_dsu.cpp)。[公式仕様](https://atcoder.github.io/ac-library/production/document_ja/dsu.html)

### Fenwick Tree / BIT：1点加算と区間和

```cpp
int N = 5;
atcoder::fenwick_tree<long long> F(N); // 最初は全部0
F.add(2, 7);                         // A[2] += 7
F.add(2, -3);                        // A[2] -= 3
long long ans = F.sum(1, 4);          // A[1]+A[2]+A[3] = 4
```

**`add(p,x)` は代入ではなく加算です。`sum(l,r)` は右端rを含みません。** 代入したいなら、現在値を別に持ち `F.add(p, 新値-旧値)` とします。

構築 O(N)、加算・区間和 O(log N)。初期配列の各要素を `add` で入れる場合は初期化全体 O(N log N)。全体例：[acl_fenwick.cpp](examples/acl_fenwick.cpp)。[公式仕様](https://atcoder.github.io/ac-library/production/document_ja/fenwicktree.html)

### segtree：1点代入と区間の最小・最大・和

`op` は2つの結果をまとめる関数、`e` は混ぜても結果を変えない値を返す関数です。両方を **mainの外** に置きます。

```cpp
long long op(long long a, long long b){
    return min(a, b);
}
long long e(){
    return numeric_limits<long long>::max();
}
```

mainの中：

```cpp
vector<long long> A = {5, 2, 8};
atcoder::segtree<long long, op, e> seg(A);
seg.set(1, 7);                      // A[1] = 7。加算ではない
long long x = seg.get(1);           // 7
long long ans = seg.prod(0, 3);     // [0,3)の最小値 = 5
long long all = seg.all_prod();     // 全体の最小値 = 5
```

| 求めたいもの | op(a,b) | e() |
|---|---|---|
| 最小 | `min(a,b)` | 型の最大値 |
| 最大 | `max(a,b)` | 型の最小値 |
| 和 | `a+b` | `0` |
| 最大公約数（非負整数） | `gcd(a,b)` | `0` |

**まとめる順番の括弧を変えても答えが変わらない演算に使います。** たとえば引き算は使えません。構築 O(N)、set/prod O(log N)、get/all_prod O(1)（op/eがO(1)の場合）。区間全体の更新はこのsegtreeではできず、対応する演算設計をした `lazy_segtree` などが必要です。

全体例：[acl_segtree.cpp](examples/acl_segtree.cpp)。[公式仕様](https://atcoder.github.io/ac-library/production/document_ja/segtree.html)

### modint：指定された整数で割った余りを管理

型の別名はmainの外に置くと、関数でも使えます。

```cpp
using mint = atcoder::modint998244353;
// 余りが1000000007なら atcoder::modint1000000007
```

mainの中：

```cpp
mint a = 10, b = 3;
mint ans = a*b + 5;
cout << ans.val() << endl; // 35。出力は .val()
mint p = b.pow(5);         // 3^5 の余り。指数は0以上
mint q = a/b;              // 通常の整数除算ではなく、逆元を掛ける
long long x;
cin >> x;
mint y = x;               // 入力は整数で受けて代入
```

**`a/b` は「bを掛けるとaになる余り」を計算します。切り捨て除算とは別物です。** 除数と法が互いに素である必要があり、この2つの素数の法では除数の余りが0だと割れません。比較による大小判定にも通常の整数の代わりとしては使えません。

DPの配列なら `vector<mint> dp(N+1, 0);` とします。`.val()` は表示など最後に整数が必要な場所で使います。全体例：[acl_modint.cpp](examples/acl_modint.cpp)。[公式仕様](https://atcoder.github.io/ac-library/production/document_ja/modint.html)

### その他のACL：必要になったら公式へ

| 機能 | 用途・入口 |
|---|---|
| [pow_mod](https://atcoder.github.io/ac-library/production/document_ja/math.html) | `atcoder::pow_mod(x,n,m)`：xのn乗をmで割った余り。n ≥ 0、m ≥ 1 |
| [inv_mod](https://atcoder.github.io/ac-library/production/document_ja/math.html) | `atcoder::inv_mod(x,m)`：逆元。gcd(x,m)=1、m ≥ 1 |
| [z_algorithm](https://atcoder.github.io/ac-library/production/document_ja/string.html) | `atcoder::z_algorithm(S)`：各位置からの接尾辞とSの先頭が何文字一致するか。O(N) |
| [scc](https://atcoder.github.io/ac-library/production/document_ja/scc.html) | 有向グラフを、互いに行き来できる頂点のまとまりに分解 |
| [maxflow](https://atcoder.github.io/ac-library/production/document_ja/maxflow.html) | 辺の容量制限つきで流せる最大量 |
| [lazy_segtree](https://atcoder.github.io/ac-library/production/document_ja/lazysegtree.html) | 区間更新と区間取得。演算・更新の合成方法を自分で定義する |

## 提出前チェック

- **問題の1始まりと、配列の0始まりをそろえたか。** `a--` のし忘れ・二重変換を確認。
- **区間の右端を含むか。** `substr` の第2引数は文字数、ACLの区間は基本 `[l,r)`。
- **計算の途中から long long になっているか。** `int*int`、`accumulate` の初期値、ペア数に注意。
- **存在しない位置・空の容器を読んでいないか。** `end()`、`begin()` の前、空のtop/front/back。
- **二分探索の前提があるか。** ソート済み配列か、判定が単調か。
- **毎回O(N)の処理をQ回していないか。** count/find/最大値探索、vectorの先頭削除、配列コピー。
- **初期値が目的に合うか。** 最小化ならINF、最大化で負の答えがあり得るなら0で始めない。
- **N=1・全要素同じ・解なし・全要素選択・到達不可** を確認。
- **出力形式を合わせたか。** `Yes/No` の大文字小文字、空白、改行、小数桁。
- **利用するコンテストのルールを確認済みか。** 保存資料・外部ライブラリ・生成AIの扱いはコンテストの規定に従う。

この資料は標準ライブラリとよく使う手法の参照用です。高度なアルゴリズム全般を網羅するものではありません。ACL部分は2026-11-08に公式仕様を確認しました。

## 検証記録

2026-11-08、WSLのGCC 15.2.0・C++17で、全体例7本のコンパイルと355ケースの出力照合に成功しました。単独で動く部分コード33個も、必要な前提を補ってコンパイル・実行しました。すべての手法・入力を網羅する検証ではありません。

検証時の公式ACLリビジョン：`864245a00b00dd008d1abfdc239618fdb7d139da`。再実行方法は [コード例の説明](examples/README.md) を参照してください。
