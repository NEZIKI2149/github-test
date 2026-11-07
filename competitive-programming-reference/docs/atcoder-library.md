# AtCoder Library

グループ・区間集計・余りの計算。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

**ACLのヘッダが必要です。** ローカルでは `atcoder` フォルダの親を `-I` に指定します。

[公式ドキュメント](https://atcoder.github.io/ac-library/production/document_ja/index.html)

## modint：余りを取りながら整数計算

法は998244353か1000000007。大小比較には使えない。出力はval()、入力は通常の整数で受けて代入。

### 998244353で割った余りを管理する

計算量：O(1) / 追加メモリ：O(1)



```cpp
mint x = a;
```

⚠︎ 法を変えるには全体コードの型の別名を変更

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

### 余りを取りながら加減乗算する

計算量：O(1) / 追加メモリ：O(1)



```cpp
mint ans = a*b + c;
```

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

### 余りを整数として出力する

計算量：O(1)（桁数固定） / 追加メモリ：O(1)



```cpp
cout << x.val() << endl;
```

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

### xのn乗の余りを求める

計算量：O(log n) / 追加メモリ：O(1)

n：指数

```cpp
mint ans = x.pow(n);
```

⚠︎ n ≥ 0

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

### 逆元を掛ける割り算をする

計算量：O(log MOD) / 追加メモリ：O(1)

MOD：余りを求めるときの法

```cpp
mint ans = a/b;
```

⚠︎ 普通の整数の割り算とは異なる。bを法で割った余りが0のときは使えない

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

### 余りを管理するDP配列を作る

計算量：O(N) / 追加メモリ：O(N)

N：指定した要素数

```cpp
vector<mint> dp(N+1, 0);
```

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

## math / string：累乗・文字列処理

各機能の詳しい条件はAtCoder Libraryの公式ドキュメントを参照。

### xのn乗をmで割った余りを求める

計算量：O(log n) / 追加メモリ：O(1)

n：指数

```cpp
long long ans = atcoder::pow_mod(x, n, m);
```

⚠︎ n ≥ 0、1 ≤ m ≤ intの最大値

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

### 各位置からの接尾辞と先頭が一致する長さを求める

計算量：O(N) / 追加メモリ：O(N)

N：文字列の文字数

```cpp
vector<int> Z = atcoder::z_algorithm(S);
```

⚠︎ Z[i]はSの先頭とS[i..N)の共通接頭辞長

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
