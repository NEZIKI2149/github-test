# AtCoder Library

グループ・区間集計・余りの計算。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

**ACLのヘッダが必要です。** ローカルでは `atcoder` フォルダの親を `-I` に指定します。

[公式ドキュメント](https://atcoder.github.io/ac-library/production/document_ja/index.html)

## dsu：グループ結合・連結判定

Union-Find。頂点0〜N−1。辺の削除・距離計算はできない。α(N)は逆アッカーマン関数で、実用的には非常に小さい。

### N頂点を別々のグループとして作る

計算量：O(N)

```cpp
atcoder::dsu D(N);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    int N = 5;
    atcoder::dsu D(N);
    return 0;
}
```

</details>

### 頂点aとbのグループを結合する

計算量：ならし O(α(N))

```cpp
D.merge(a, b);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);
    D.merge(a, b);
    return 0;
}
```

</details>

### 頂点aとbが同じグループか判定する

計算量：ならし O(α(N))

```cpp
bool same = D.same(a, b);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);
    bool same = D.same(a, b);
    return 0;
}
```

</details>

### 頂点aのグループの頂点数を求める

計算量：ならし O(α(N))

```cpp
int size = D.size(a);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);
    int size = D.size(a);
    return 0;
}
```

</details>

### 頂点aのグループの代表頂点を求める

計算量：ならし O(α(N))

```cpp
int root = D.leader(a);
```

代表は最小頂点とは限らず、結合で変わる

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);
    int root = D.leader(a);
    return 0;
}
```

</details>

### 全グループの頂点一覧を得る

計算量：O(N)

```cpp
vector<vector<int>> groups = D.groups();
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/dsu>
using namespace std;

int main(){
    atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);
    vector<vector<int>> groups = D.groups();
    return 0;
}
```

</details>

## fenwick_tree：1点加算・区間和

BITとも呼ぶ。0始まり、区間の右端は含まない。初期値はすべて0。sumはlong long内に収まるようにする。

### 長さNの配列をすべて0で作る

計算量：O(N)

```cpp
atcoder::fenwick_tree<long long> F(N);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/fenwicktree>
using namespace std;

int main(){
    int N = 5;
    atcoder::fenwick_tree<long long> F(N);
    return 0;
}
```

</details>

### **添字**pの値にxを加算する

計算量：O(log N)

```cpp
F.add(p, x);
```

代入ではない

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/fenwicktree>
using namespace std;

int main(){
    atcoder::fenwick_tree<long long> F(5); int p = 2; long long x = 7;
    F.add(p, x);
    return 0;
}
```

</details>

### **添字**l以上r未満の和を求める

計算量：O(log N)

```cpp
long long ans = F.sum(l, r);
```

0 ≤ l ≤ r ≤ N

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/fenwicktree>
using namespace std;

int main(){
    atcoder::fenwick_tree<long long> F(5); int l = 1, r = 4;
    long long ans = F.sum(l, r);
    return 0;
}
```

</details>

### **添字**pの値をxへ変更する

計算量：O(log N)

```cpp
F.add(p, x-A.at(p));
A.at(p) = x;
```

現在値Aを別に持つ

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/fenwicktree>
using namespace std;

int main(){
    vector<long long> A = {1,2,3};
    atcoder::fenwick_tree<long long> F(3);
    for(int i = 0;i < 3;i++){
        F.add(i, A.at(i));
    }
    int p = 1; long long x = 9;
    F.add(p, x-A.at(p));
    A.at(p) = x;
    return 0;
}
```

</details>

## segtree：1点代入・区間集計

opは2つの結果をまとめる関数、eは混ぜても結果を変えない値。括弧の付け方で結果が変わらない演算に使う。

### 1点更新に対応する区間の最小値を求める

計算量：構築 O(N) / 更新・取得 O(log N)

```cpp
atcoder::segtree<long long, op, e> seg(A);
seg.set(p, x);
long long ans = seg.prod(l, r);
```

setは代入。prodは添字l以上r未満。最大公約数は非負整数を前提。和は型に収まること。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){
    return min(a, b);
}
long long e(){
    return numeric_limits<long long>::max();
}

int main(){
    vector<long long> A = {5,2,8};
    int p = 1, l = 0, r = 3;
    long long x = 7;
    atcoder::segtree<long long, op, e> seg(A);
    seg.set(p, x);
    long long ans = seg.prod(l, r);
    return 0;
}
```

</details>

### 1点更新に対応する区間の最大値を求める

計算量：構築 O(N) / 更新・取得 O(log N)

```cpp
atcoder::segtree<long long, op, e> seg(A);
seg.set(p, x);
long long ans = seg.prod(l, r);
```

setは代入。prodは添字l以上r未満。最大公約数は非負整数を前提。和は型に収まること。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){
    return max(a, b);
}
long long e(){
    return numeric_limits<long long>::lowest();
}

int main(){
    vector<long long> A = {5,2,8};
    int p = 1, l = 0, r = 3;
    long long x = 7;
    atcoder::segtree<long long, op, e> seg(A);
    seg.set(p, x);
    long long ans = seg.prod(l, r);
    return 0;
}
```

</details>

### 1点更新に対応する区間の和を求める

計算量：構築 O(N) / 更新・取得 O(log N)

```cpp
atcoder::segtree<long long, op, e> seg(A);
seg.set(p, x);
long long ans = seg.prod(l, r);
```

setは代入。prodは添字l以上r未満。最大公約数は非負整数を前提。和は型に収まること。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){
    return a+b;
}
long long e(){
    return 0;
}

int main(){
    vector<long long> A = {5,2,8};
    int p = 1, l = 0, r = 3;
    long long x = 7;
    atcoder::segtree<long long, op, e> seg(A);
    seg.set(p, x);
    long long ans = seg.prod(l, r);
    return 0;
}
```

</details>

### 1点更新に対応する区間の最大公約数を求める

計算量：構築 O(N) / 更新・取得 O(log N)

```cpp
atcoder::segtree<long long, op, e> seg(A);
seg.set(p, x);
long long ans = seg.prod(l, r);
```

setは代入。prodは添字l以上r未満。最大公約数は非負整数を前提。和は型に収まること。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){
    return gcd(a, b);
}
long long e(){
    return 0;
}

int main(){
    vector<long long> A = {5,2,8};
    int p = 1, l = 0, r = 3;
    long long x = 7;
    atcoder::segtree<long long, op, e> seg(A);
    seg.set(p, x);
    long long ans = seg.prod(l, r);
    return 0;
}
```

</details>

### **添字**pの現在値を読む

計算量：O(1)

```cpp
long long x = seg.get(p);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){ return min(a,b); }
long long e(){ return LLONG_MAX; }
int main(){
    vector<long long> A = {5,2,8};
    atcoder::segtree<long long, op, e> seg(A); int p = 1;
    long long x = seg.get(p);
    return 0;
}
```

</details>

### 全区間の集計値を読む

計算量：O(1)

```cpp
long long ans = seg.all_prod();
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){ return min(a,b); }
long long e(){ return LLONG_MAX; }
int main(){
    vector<long long> A = {5,2,8};
    atcoder::segtree<long long, op, e> seg(A);
    long long ans = seg.all_prod();
    return 0;
}
```

</details>

## modint：余りを取りながら整数計算

法は998244353か1000000007。大小比較には使えない。出力はval()、入力は通常の整数で受けて代入。

### 998244353で割った余りを管理する

計算量：O(1)

```cpp
mint x = a;
```

法を変えるには全体コードの型の別名を変更

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    long long a = 123;
    mint x = a;
    return 0;
}
```

</details>

### 余りを取りながら加減乗算する

計算量：O(1)

```cpp
mint ans = a*b + c;
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    mint a = 10, b = 3, c = 5;
    mint ans = a*b + c;
    return 0;
}
```

</details>

### 余りを整数として出力する

計算量：O(1)（桁数固定）

```cpp
cout << x.val() << endl;
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    mint x = 123;
    cout << x.val() << endl;
    return 0;
}
```

</details>

### xのn乗の余りを求める

計算量：O(log n)

```cpp
mint ans = x.pow(n);
```

n ≥ 0

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    mint x = 3; long long n = 5;
    mint ans = x.pow(n);
    return 0;
}
```

</details>

### 逆元を掛ける割り算をする

計算量：O(log MOD)

```cpp
mint ans = a/b;
```

整数の切り捨て除算ではない。bの余りが0なら不可

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    mint a = 10, b = 3;
    mint ans = a/b;
    return 0;
}
```

</details>

### 余りを管理するDP配列を作る

計算量：O(N)

```cpp
vector<mint> dp(N+1, 0);
```

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;

using mint = atcoder::modint998244353;

int main(){
    int N = 5;
    vector<mint> dp(N+1, 0);
    return 0;
}
```

</details>

## math / string：累乗・文字列処理

各機能の詳しい条件はAtCoder Libraryの公式ドキュメントを参照。

### xのn乗をmで割った余りを求める

計算量：O(log n)

```cpp
long long ans = atcoder::pow_mod(x, n, m);
```

n ≥ 0、1 ≤ m ≤ intの最大値

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/math>
using namespace std;

int main(){
    long long x = 3, n = 5; int m = 7;
    long long ans = atcoder::pow_mod(x, n, m);
    return 0;
}
```

</details>

### 各位置からの接尾辞と先頭が一致する長さを求める

計算量：O(N)

```cpp
vector<int> Z = atcoder::z_algorithm(S);
```

Z[i]はSの先頭とS[i..N)の共通接頭辞長

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/string>
using namespace std;

int main(){
    string S = "ababa";
    vector<int> Z = atcoder::z_algorithm(S);
    return 0;
}
```

</details>
