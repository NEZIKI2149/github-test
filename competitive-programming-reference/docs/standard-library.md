# 標準ライブラリ

容器と操作関数を、名前から引く。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

**容器**：vector・string・set・map・queue・stack・deque・priority_queue・pair・tuple

**操作関数**：sort・reverse・rotate・fill・unique・二分探索・集計・数値計算・入出力

## vector：可変長の配列

Nは現在の要素数。front・back・pop_backは空の配列に使わない。atは範囲外で例外になる。

### N個の要素を0で初期化する

計算量：O(N) / 追加メモリ：O(N)

N：指定した要素数

```cpp
vector<int> A(N, 0);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N = 5;
    vector<int> A(N, 0);
    return 0;
}
```

### H行W列を−1で初期化する

計算量：O(HW) / 追加メモリ：O(HW + H)

H：行数、W：列数

```cpp
vector<vector<int>> A(H, vector<int>(W, -1));
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int H = 3, W = 4;
    vector<vector<int>> A(H, vector<int>(W, -1));
    return 0;
}
```

### 添字iの要素を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = A.at(i);
```

⚠︎ 0以上、要素数未満の添字を指定する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4};
    int i = 1;
    int x = A.at(i);
    return 0;
}
```

### 添字iの要素を変更する

計算量：O(1) / 追加メモリ：O(1)



```cpp
A.at(i) = x;
```

⚠︎ 0以上、要素数未満の添字を指定する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.at(i) = x;
    return 0;
}
```

### 先頭の要素を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = A.front();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4};
    int i = 1;
    int x = A.front();
    return 0;
}
```

### 末尾の要素を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = A.back();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4};
    int i = 1;
    int x = A.back();
    return 0;
}
```

### 要素数を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
int N = A.size();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4};
    int N = A.size();
    return 0;
}
```

### 空か判定する

計算量：O(1) / 追加メモリ：O(1)



```cpp
bool empty = A.empty();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    bool empty = A.empty();
    return 0;
}
```

### 末尾にxを追加する

計算量：ならし O(1) / 追加メモリ：再確保時 O(N)

N：操作前の要素数

```cpp
A.push_back(x);
```

⚠︎ 容量が足りなくなると、メモリの確保し直しが発生する。 「ならし」は、操作を何度も繰り返したときの1回あたりの目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.push_back(x);
    return 0;
}
```

### 末尾の1要素を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
A.pop_back();
```

⚠︎ 配列が空のときは使えない。取り出した値は返さない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.pop_back();
    return 0;
}
```

### 添字iの直前にxを挿入する

計算量：O(N) / 追加メモリ：再確保時 O(N)

N：操作前の要素数

```cpp
A.insert(A.begin()+i, x);
```

⚠︎ 挿入位置は0以上、要素数以下。挿入位置以降の添字が後ろにずれる

```text
i = 1、x = 9
実行前：[3, 1, 4]
実行後：[3, 9, 1, 4]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.insert(A.begin()+i, x);
    return 0;
}
```

### 添字iの1要素を削除する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.erase(A.begin()+i);
```

⚠︎ 削除位置は0以上、要素数未満。削除位置より後ろの添字が前にずれる

```text
i = 1
実行前：[3, 1, 4]
実行後：[3, 4]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.erase(A.begin()+i);
    return 0;
}
```

### 添字l以上r未満を削除する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.erase(A.begin()+l, A.begin()+r);
```

⚠︎ 0 ≤ l ≤ r ≤ 要素数。削除した区間より後ろの添字が前にずれる

```text
l = 1、r = 3
実行前：[3, 1, 4, 2, 5]
実行後：[3, 2, 5]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.erase(A.begin()+l, A.begin()+r);
    return 0;
}
```

### 要素数をNにする

計算量：O(N + 変更前の要素数) / 追加メモリ：再確保時 O(N)

N：指定した要素数（変更前の要素数は別）

```cpp
A.resize(N, -1);
```

⚠︎ 増えた要素だけ−1。減らした部分は失われる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.resize(N, -1);
    return 0;
}
```

### N要素ぶんの容量を予約する

計算量：再確保時 O(現在の要素数) / 追加メモリ：O(N)

N：指定した要素数

```cpp
A.reserve(N);
```

⚠︎ 要素数は増えない。atで新しい位置を読めるようにはならない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.reserve(N);
    return 0;
}
```

### 全体をxがN個の配列に置き換える

計算量：O(N + 変更前の要素数) / 追加メモリ：再確保時 O(N)

N：指定した要素数（変更前の要素数は別）

```cpp
A.assign(N, x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.assign(N, x);
    return 0;
}
```

### 全要素を削除する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.clear();
```

⚠︎ 確保済みの容量は通常残る

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    A.clear();
    return 0;
}
```

### 配列全体をコピーする

計算量：O(N) / 追加メモリ：O(N)

N：操作前の要素数

```cpp
vector<int> B = A;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3, 1, 4, 1, 5};
    int N = A.size();
    int i = 2, x = 9, l = 1, r = 4;
    vector<int> B = A;
    return 0;
}
```

## string：文字列

Nは文字列長、Kは対象の文字数。添字は0始まり。末尾の読み取り・削除は空なら使わない。

### 同じ文字をN個並べる

計算量：O(N) / 追加メモリ：O(N)

N：指定した要素数

```cpp
string S(N, 'a');
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N = 5;
    string S(N, 'a');
    return 0;
}
```

### 添字iの文字を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
char c = S.at(i);
```

⚠︎ 0以上、文字数未満の添字を指定する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abc"; int i = 1;
    char c = S.at(i);
    return 0;
}
```

### 添字iの文字を変更する

計算量：O(1) / 追加メモリ：O(1)



```cpp
S.at(i) = c;
```

⚠︎ 0以上、文字数未満の添字を指定する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.at(i) = c;
    return 0;
}
```

### 文字数を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
int N = S.size();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    int N = S.size();
    return 0;
}
```

### 空か判定する

計算量：O(1) / 追加メモリ：O(1)



```cpp
bool empty = S.empty();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    bool empty = S.empty();
    return 0;
}
```

### 末尾に1文字追加する

計算量：ならし O(1) / 追加メモリ：再確保時 O(N)

N：文字列の文字数

```cpp
S.push_back(c);
```

⚠︎ 容量が足りなくなると、メモリの確保し直しが発生する。 「ならし」は、操作を何度も繰り返したときの1回あたりの目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.push_back(c);
    return 0;
}
```

### 末尾に文字列Tを連結する

計算量：ならし O(Tの長さ) / 追加メモリ：再確保時 O(N + Tの長さ)

N：文字列の文字数

```cpp
S += T;
```

⚠︎ 再確保時は元の文字列のコピーも発生 「ならし」は、操作を何度も繰り返したときの1回あたりの目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S += T;
    return 0;
}
```

### 末尾の文字を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
char last = S.back();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    char last = S.back();
    return 0;
}
```

### 末尾の1文字を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
S.pop_back();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.pop_back();
    return 0;
}
```

### 添字posからk文字を取り出す

計算量：O(K) / 追加メモリ：O(K)

K：取り出す文字数

```cpp
string U = S.substr(pos, k);
```

⚠︎ 第2引数は終点ではなく文字数。posは0以上、文字数以下。残りがk文字未満なら末尾まで

```text
pos = 1、k = 3
元の文字列："abcde"
取り出す文字列："bcd"（元の文字列は変わらない）
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    string U = S.substr(pos, k);
    return 0;
}
```

### 添字posから末尾まで取り出す

計算量：O(N−pos) / 追加メモリ：O(N−pos)

N：文字列の文字数 / pos：取り出しを始める添字

```cpp
string U = S.substr(pos);
```

⚠︎ posは0以上、文字数以下

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    string U = S.substr(pos);
    return 0;
}
```

### 文字列Tが最初に現れる位置を探す

計算量：最悪 O(N × Tの長さ) / 追加メモリ：O(1)

N：文字列の文字数

```cpp
size_t p = S.find(T);
```

⚠︎ なければstring::npos。文字1個の検索はO(N)

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    size_t p = S.find(T);
    return 0;
}
```

### 添字pos以降で文字列Tを探す

計算量：最悪 O(N × Tの長さ) / 追加メモリ：O(1)

N：文字列の文字数

```cpp
size_t p = S.find(T, pos);
```

⚠︎ 見つからなければstring::nposになる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    size_t p = S.find(T, pos);
    return 0;
}
```

### 文字列Tが最後に現れる位置を探す

計算量：最悪 O(N × Tの長さ) / 追加メモリ：O(1)

N：文字列の文字数

```cpp
size_t p = S.rfind(T);
```

⚠︎ なければstring::npos

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    size_t p = S.rfind(T);
    return 0;
}
```

### 検索結果が見つかったか判定する

計算量：O(1) / 追加メモリ：O(1)



```cpp
bool found = p != string::npos;
```

⚠︎ 見つからない位置をatで読まない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    size_t p = S.find(T);
    bool found = p != string::npos;
    return 0;
}
```

### 添字posの直前にTを挿入する

計算量：O(N + Tの長さ) / 追加メモリ：再確保時 O(N + Tの長さ)

N：文字列の文字数

```cpp
S.insert(pos, T);
```

⚠︎ posは0以上、文字数以下

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.insert(pos, T);
    return 0;
}
```

### 添字posからk文字を削除する

計算量：O(N) / 追加メモリ：O(1)

N：文字列の文字数

```cpp
S.erase(pos, k);
```

⚠︎ 第2引数は文字数

```text
pos = 1、k = 2
実行前："abcde"
実行後："ade"
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.erase(pos, k);
    return 0;
}
```

### 添字posからk文字をTに置き換える

計算量：O(N + Tの長さ) / 追加メモリ：再確保時 O(N + Tの長さ)

N：文字列の文字数

```cpp
S.replace(pos, k, T);
```

⚠︎ 第2引数は文字数

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    S.replace(pos, k, T);
    return 0;
}
```

### 文字列の大小を辞書順で比較する

計算量：O(比較する文字数) / 追加メモリ：O(1)



```cpp
bool smaller = S < T;
```

⚠︎ 大文字・小文字などは文字コード順

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcabc";
    int i = 1, pos = 1, k = 3;
    char c = 'x';
    string T = "bc";
    bool smaller = S < T;
    return 0;
}
```

### 文字の数字を整数にする

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = c - '0';
```

⚠︎ 文字が'0'〜'9'のとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    char c = '7';
    int x = c - '0';
    return 0;
}
```

### 英小文字を0〜25の番号にする

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = c - 'a';
```

⚠︎ 英小文字のとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    char c = 'c';
    int x = c - 'a';
    return 0;
}
```

### 文字列をintに変換する

計算量：O(読み取る文字数) / 追加メモリ：O(1)



```cpp
int x = stoi(S);
```

⚠︎ 変換不能・型の範囲外で例外。先頭の数値部分だけを読む場合がある

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "123";
    int x = stoi(S);
    return 0;
}
```

### 文字列をlong longに変換する

計算量：O(読み取る文字数) / 追加メモリ：O(1)



```cpp
long long x = stoll(S);
```

⚠︎ 変換不能・型の範囲外で例外

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "12345678900";
    long long x = stoll(S);
    return 0;
}
```

### 整数を文字列に変換する

計算量：O(桁数) / 追加メモリ：O(桁数)



```cpp
string S = to_string(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long x = 123;
    string S = to_string(x);
    return 0;
}
```

### 空白を含む1行を読み取る

計算量：O(読み取る文字数) / 追加メモリ：O(読み取る文字数)



```cpp
getline(cin, S);
```

⚠︎ 直前の >> が残した改行に注意

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S;
    getline(cin, S);
    return 0;
}
```

### 整数入力の後に、次の1行を読み取る

計算量：O(読み捨てる文字数 + 読む文字数) / 追加メモリ：O(読む文字数)



```cpp
cin.ignore(numeric_limits<streamsize>::max(), '\n');
getline(cin, S);
```

⚠︎ 行末まで捨ててから読む。次の行の先頭空白は保持

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    string S;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    getline(cin, S);
    return 0;
}
```

## set / multiset：順序つきの集合

setは重複なし、multisetは重複あり。添字アクセス不可。Kは同じ値の個数。 setではS.lower_bound(x)を使う。lower_bound(S.begin(), S.end(), x)やdistanceによる順位取得はO(N)の移動が発生する。

### 重複なしの集合を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
set<int> S;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S;
    return 0;
}
```

### 重複ありの集合を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
multiset<int> S;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S;
    return 0;
}
```

### xを追加する

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
S.insert(x);
```

⚠︎ setでは同じ値は増えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S; int x = 3;
    S.insert(x);
    return 0;
}
```

### xがあるか判定する

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
bool exists = S.find(x) != S.end();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9}; int x = 5;
    bool exists = S.find(x) != S.end();
    return 0;
}
```

### 要素数を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
int N = S.size();
```

⚠︎ multisetでは重複も数える

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S = {2,5,5};
    int N = S.size();
    return 0;
}
```

### xの個数を求める

計算量：set: O(log N) / multiset: O(log N + K) / 追加メモリ：O(1)

N：操作前の要素数 / K：同じ値の個数

```cpp
int cnt = S.count(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S = {2,5,5}; int x = 5;
    int cnt = S.count(x);
    return 0;
}
```

### xをすべて削除する

計算量：O(log N + 削除数) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
S.erase(x);
```

⚠︎ multisetでは同じ値が全部消える

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S = {2,5,5}; int x = 5;
    S.erase(x);
    return 0;
}
```

### xを1個だけ削除する

計算量：検索 O(log N) / 位置指定削除はならし O(1) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = S.find(x);
if(it != S.end()){
    S.erase(it);
}
```

⚠︎ 「ならし」は、操作を何度も繰り返したときの1回あたりの目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S = {2,5,5}; int x = 5;
    auto it = S.find(x);
    if(it != S.end()){
        S.erase(it);
    }
    return 0;
}
```

### 最小値を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = *S.begin();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9};
    int x = *S.begin();
    return 0;
}
```

### 最大値を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = *S.rbegin();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9};
    int x = *S.rbegin();
    return 0;
}
```

### 最小値を1個削除する

計算量：ならし O(1) / 追加メモリ：O(1)



```cpp
S.erase(S.begin());
```

⚠︎ 容器が空のときは使えない 「ならし」は、操作を何度も繰り返したときの1回あたりの目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    multiset<int> S = {2,5,5};
    S.erase(S.begin());
    return 0;
}
```

### x以上の最小値を探す

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = S.lower_bound(x);
if(it != S.end()){
    int ans = *it;
}
```

⚠︎ 該当する値がなければendになる。endの中身は読めない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9}; int x = 6;
    auto it = S.lower_bound(x);
    if(it != S.end()){
        int ans = *it;
    }
    return 0;
}
```

### xより大きい最小値を探す

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = S.upper_bound(x);
if(it != S.end()){
    int ans = *it;
}
```

⚠︎ 該当する値がなければendになる。endの中身は読めない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9}; int x = 5;
    auto it = S.upper_bound(x);
    if(it != S.end()){
        int ans = *it;
    }
    return 0;
}
```

### x未満の最大値を探す

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = S.lower_bound(x);
if(it != S.begin()){
    it--;
    int ans = *it;
}
```

⚠︎ beginから前に戻さない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9}; int x = 6;
    auto it = S.lower_bound(x);
    if(it != S.begin()){
        it--;
        int ans = *it;
    }
    return 0;
}
```

### x以下の最大値を探す

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = S.upper_bound(x);
if(it != S.begin()){
    it--;
    int ans = *it;
}
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9}; int x = 5;
    auto it = S.upper_bound(x);
    if(it != S.begin()){
        it--;
        int ans = *it;
    }
    return 0;
}
```

### 小さい順に全要素を読む

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
for(auto it = S.begin();it != S.end();it++){
    cout << *it << endl;
}
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    set<int> S = {2,5,9};
    for(auto it = S.begin();it != S.end();it++){
        cout << *it << endl;
    }
    return 0;
}
```

## map / unordered_map：キーごとの値

Kはキーの種類数。mapの操作はO(log K)。文字列キーでは比較する文字数も考慮する。

### 整数ごとに回数を持つ

計算量：構築 O(1) / 追加メモリ：O(1)



```cpp
map<int, long long> cnt;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt;
    return 0;
}
```

### 文字列ごとに回数を持つ

計算量：構築 O(1) / 追加メモリ：O(1)



```cpp
map<string, int> cnt;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<string, int> cnt;
    return 0;
}
```

### xの回数を1増やす

計算量：O(log K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
cnt[x]++;
```

⚠︎ キーがなければ0から始まる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt; int x = 5;
    cnt[x]++;
    return 0;
}
```

### キーxの値を読む

計算量：O(log K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
long long num = cnt[x];
```

⚠︎ キーがないと値0の要素を追加する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt; int x = 5;
    long long num = cnt[x];
    return 0;
}
```

### キーxがあるか判定する

計算量：O(log K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
bool exists = cnt.count(x) > 0;
```

⚠︎ 値が0かどうかとは別。要素は追加しない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt; int x = 5;
    bool exists = cnt.count(x) > 0;
    return 0;
}
```

### キーxがあれば値を読む

計算量：O(log K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
auto it = cnt.find(x);
if(it != cnt.end()){
    long long num = it->second;
}
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt; int x = 5;
    auto it = cnt.find(x);
    if(it != cnt.end()){
        long long num = it->second;
    }
    return 0;
}
```

### キーxとその値を削除する

計算量：O(log K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
cnt.erase(x);
```

⚠︎ 値を0にするだけではキーは消えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt; int x = 5;
    cnt.erase(x);
    return 0;
}
```

### キーの種類数を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
int kinds = cnt.size();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt;
    int kinds = cnt.size();
    return 0;
}
```

### キーの昇順にキーと値を読む

計算量：O(K) / 追加メモリ：O(1)

K：キーの種類数

```cpp
for(auto it = cnt.begin();it != cnt.end();it++){
    cout << it->first << " " << it->second << endl;
}
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    map<int, long long> cnt = {{5,2},{2,1}};
    for(auto it = cnt.begin();it != cnt.end();it++){
        cout << it->first << " " << it->second << endl;
    }
    return 0;
}
```

### 順序なしの対応表を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
unordered_map<int, int> M;
```

⚠︎ lower_bound・大小順の走査は不可

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    unordered_map<int, int> M;
    return 0;
}
```

### 順序なしの重複しない集合を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
unordered_set<int> S;
```

⚠︎ 順序不要でも最悪計算量に注意

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    unordered_set<int> S;
    return 0;
}
```

## queue / stack / deque：取り出す順番

読む・削除する前に空でないことを確認する。popは値を返さない。

### queue：先に入れた順で取り出す容器を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
queue<int> Q;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q;
    return 0;
}
```

### queue：先に入れた順の容器へ追加する

計算量：O(1) / 追加メモリ：通常 O(1) / 管理領域の拡張時 O(N)

N：操作前の要素数

```cpp
Q.push(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q; int x = 3;
    Q.push(x);
    return 0;
}
```

### queue：先に入れた順の次の値を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int ans = Q.front();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q; Q.push(3);
    int ans = Q.front();
    return 0;
}
```

### queue：先に入れた順の次の要素を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
Q.pop();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q; Q.push(3);
    Q.pop();
    return 0;
}
```

### stack：後に入れた順で取り出す容器を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
stack<int> Q;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    stack<int> Q;
    return 0;
}
```

### stack：後に入れた順の容器へ追加する

計算量：O(1) / 追加メモリ：通常 O(1) / 管理領域の拡張時 O(N)

N：操作前の要素数

```cpp
Q.push(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    stack<int> Q; int x = 3;
    Q.push(x);
    return 0;
}
```

### stack：後に入れた順の次の値を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int ans = Q.top();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    stack<int> Q; Q.push(3);
    int ans = Q.top();
    return 0;
}
```

### stack：後に入れた順の次の要素を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
Q.pop();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    stack<int> Q; Q.push(3);
    Q.pop();
    return 0;
}
```

### 空か判定する（各容器共通）

計算量：O(1) / 追加メモリ：O(1)



```cpp
bool empty = Q.empty();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q;
    bool empty = Q.empty();
    return 0;
}
```

### 要素数を求める（各容器共通）

計算量：O(1) / 追加メモリ：O(1)



```cpp
int N = Q.size();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    queue<int> Q;
    int N = Q.size();
    return 0;
}
```

### 両端から操作できる配列を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
deque<int> D;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D;
    return 0;
}
```

### 先頭にxを追加する

計算量：O(1) / 追加メモリ：通常 O(1) / 管理領域の拡張時 O(N)

N：操作前の要素数

```cpp
D.push_front(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D = {1,2,3}; int x = 9, i = 1;
    D.push_front(x);
    return 0;
}
```

### 末尾にxを追加する

計算量：O(1) / 追加メモリ：通常 O(1) / 管理領域の拡張時 O(N)

N：操作前の要素数

```cpp
D.push_back(x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D = {1,2,3}; int x = 9, i = 1;
    D.push_back(x);
    return 0;
}
```

### 先頭の要素を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
D.pop_front();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D = {1,2,3}; int x = 9, i = 1;
    D.pop_front();
    return 0;
}
```

### 末尾の要素を削除する

計算量：O(1) / 追加メモリ：O(1)



```cpp
D.pop_back();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D = {1,2,3}; int x = 9, i = 1;
    D.pop_back();
    return 0;
}
```

### 添字iの要素を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int ans = D.at(i);
```

⚠︎ 0以上、要素数未満の添字を指定する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    deque<int> D = {1,2,3}; int x = 9, i = 1;
    int ans = D.at(i);
    return 0;
}
```

## priority_queue：最大値・最小値を先に取り出す

途中の任意の値の削除・変更はできない。top/popは空のとき使わない。

### 最大値を先に取り出す容器を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
priority_queue<int> Q;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<int> Q;
    return 0;
}
```

### 最小値を先に取り出す容器を作る

計算量：O(1) / 追加メモリ：O(1)



```cpp
priority_queue<int, vector<int>, greater<int>> Q;
```

⚠︎ long longなら3か所のintをlong longにする

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<int, vector<int>, greater<int>> Q;
    return 0;
}
```

### 値xを追加する

計算量：O(log N) / 追加メモリ：再確保時 O(N)

N：操作前の要素数

```cpp
Q.push(x);
```

⚠︎ 容量が足りなくなると、メモリの確保し直しが発生する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<int> Q; int x = 3;
    Q.push(x);
    return 0;
}
```

### 次に取り出す値を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int ans = Q.top();
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<int> Q; Q.push(3);
    int ans = Q.top();
    return 0;
}
```

### 次の要素を削除する

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
Q.pop();
```

⚠︎ 容器が空のときは使えない。取り出した値は返さない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<int> Q; Q.push(3);
    Q.pop();
    return 0;
}
```

### 距離・頂点の組を距離の小さい順に取り出す

計算量：構築 O(1) / 追加メモリ：O(1)



```cpp
priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> Q;
```

⚠︎ pairはfirst、同値ならsecondで比較する

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> Q;
    return 0;
}
```

## pair / tuple：複数の値をまとめる

比較は先頭から順に行う。pairはfirst、同値ならsecond。tupleはget<0>、get<1>…の順。

### 2つの値をまとめる

計算量：O(1) / 追加メモリ：O(1)



```cpp
pair<int, int> P = {3, 7};
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    pair<int, int> P = {3, 7};
    return 0;
}
```

### 組の1つ目・2つ目を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int a = P.first;
int b = P.second;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    pair<int, int> P = {3,7};
    int a = P.first;
    int b = P.second;
    return 0;
}
```

### 3つの値をまとめる

計算量：O(1) / 追加メモリ：O(1)



```cpp
tuple<int, int, int> T = {2, 5, 8};
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    tuple<int, int, int> T = {2, 5, 8};
    return 0;
}
```

### tupleの添字1の項目を読む

計算量：O(1) / 追加メモリ：O(1)



```cpp
int x = get<1>(T);
```

⚠︎ getの< >内はコンパイル時に決まる整数

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    tuple<int,int,int> T = {2,5,8};
    int x = get<1>(T);
    return 0;
}
```

### 組の中身を変数に分ける

計算量：O(1) / 追加メモリ：O(1)



```cpp
auto [a, b] = P;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    pair<int,int> P = {3,7};
    auto [a, b] = P;
    return 0;
}
```

## sort / stable_sort：並べ替え

Nは並べ替える要素数。元の並びを変更する。区間は添字l以上r未満。

### 配列全体を昇順にする

計算量：O(N log N) / 追加メモリ：O(log N)

N：操作前の要素数

```cpp
sort(A.begin(), A.end());
```

⚠︎ 追加メモリはGCCの一般的な実装の目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    sort(A.begin(), A.end());
    return 0;
}
```

### 配列全体を降順にする

計算量：O(N log N) / 追加メモリ：O(log N)

N：操作前の要素数

```cpp
sort(A.begin(), A.end(), greater<int>());
```

⚠︎ 追加メモリはGCCの一般的な実装の目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    sort(A.begin(), A.end(), greater<int>());
    return 0;
}
```

### 添字l以上r未満を昇順にする

計算量：O(K log K) / 追加メモリ：O(log K)

K：操作する区間の要素数

```cpp
sort(A.begin()+l, A.begin()+r);
```

⚠︎ 0 ≤ l ≤ r ≤ 要素数 追加メモリはGCCの一般的な実装の目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    sort(A.begin()+l, A.begin()+r);
    return 0;
}
```

### 文字列を文字コード順に並べる

計算量：O(N log N) / 追加メモリ：O(log N)

N：文字列の文字数

```cpp
sort(S.begin(), S.end());
```

⚠︎ 追加メモリはGCCの一般的な実装の目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "cabca";
    sort(S.begin(), S.end());
    return 0;
}
```

### pairをfirst優先の昇順にする

計算量：O(N log N) / 追加メモリ：O(log N)

N：操作前の要素数

```cpp
sort(A.begin(), A.end());
```

⚠︎ 追加メモリはGCCの一般的な実装の目安

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<pair<int,int>> A = {{2,8},{1,9},{2,3}};
    sort(A.begin(), A.end());
    return 0;
}
```

### 同じ値の元の順序を保って並べる

計算量：通常 O(N log N) / 補助メモリ不足時 O(N log² N) / 追加メモリ：O(N)

N：操作前の要素数

```cpp
stable_sort(A.begin(), A.end(), [](pair<int,int> a, pair<int,int> b){
    return a.first < b.first;
});
```

⚠︎ 同じfirst同士の順序を保つ

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<pair<int,int>> A = {{2,8},{1,9},{2,3}};
    stable_sort(A.begin(), A.end(), [](pair<int,int> a, pair<int,int> b){
        return a.first < b.first;
    });
    return 0;
}
```

### 元の添字を値の降順・同値なら添字の昇順に並べる

計算量：O(N log N) / 追加メモリ：O(N)

N：操作前の要素数

```cpp
sort(order.begin(), order.end(), [&](int i, int j){
    if(A.at(i) != A.at(j)){
        return A.at(i) > A.at(j);
    }
    return i < j;
});
```

⚠︎ 比較は同じもの同士でfalseになるようにする。<=や>=は不可

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {30,10,30};
    int N = A.size();
    vector<int> order(N);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int i, int j){
        if(A.at(i) != A.at(j)){
            return A.at(i) > A.at(j);
        }
        return i < j;
    });
    return 0;
}
```

## reverse / rotate：反転・回転

配列も文字列も同じ書き方。区間は添字l以上r未満。

### 配列全体の並びを反転する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
reverse(A.begin(), A.end());
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    reverse(A.begin(), A.end());
    return 0;
}
```

### 添字l以上r未満の並びを反転する

計算量：OK / 追加メモリ：O(1)

K：操作する区間の要素数

```cpp
reverse(A.begin()+l, A.begin()+r);
```

⚠︎ 0 ≤ l ≤ r ≤ 要素数

```text
l = 1、r = 4
実行前：[3, 1, 4, 2, 5]
実行後：[3, 2, 4, 1, 5]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    reverse(A.begin()+l, A.begin()+r);
    return 0;
}
```

### 文字列全体の並びを反転する

計算量：O(N) / 追加メモリ：O(1)

N：文字列の文字数

```cpp
reverse(S.begin(), S.end());
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcde";
    reverse(S.begin(), S.end());
    return 0;
}
```

### 文字列の添字l以上r未満を反転する

計算量：OK / 追加メモリ：O(1)

K：操作する区間の要素数

```cpp
reverse(S.begin()+l, S.begin()+r);
```

```text
l = 1、r = 4
実行前："abcde"
実行後："adcbe"
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    string S = "abcde"; int l = 1, r = 4;
    reverse(S.begin()+l, S.begin()+r);
    return 0;
}
```

### 配列全体を左にk個ぶん回転する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
rotate(A.begin(), A.begin()+k, A.end());
```

⚠︎ 0 ≤ k ≤ N。先頭k個を末尾へ移す

```text
k = 2
実行前：[1, 2, 3, 4, 5]
実行後：[3, 4, 5, 1, 2]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {0,1,2,3,4}; int k = 2;
    rotate(A.begin(), A.begin()+k, A.end());
    return 0;
}
```

### 配列全体を右にk個ぶん回転する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
rotate(A.begin(), A.end()-k, A.end());
```

⚠︎ 0 ≤ k ≤ N。末尾k個を先頭へ移す

```text
k = 2
実行前：[1, 2, 3, 4, 5]
実行後：[4, 5, 1, 2, 3]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {0,1,2,3,4}; int k = 2;
    rotate(A.begin(), A.end()-k, A.end());
    return 0;
}
```

### 添字l以上r未満を、添字mが先頭になるよう回転する

計算量：OK / 追加メモリ：O(1)

K：操作する区間の要素数

```cpp
rotate(A.begin()+l, A.begin()+m, A.begin()+r);
```

⚠︎ 0 ≤ l ≤ m ≤ r ≤ N

```text
l = 1、m = 3、r = 5
実行前：[0, 1, 2, 3, 4, 5]
実行後：[0, 3, 4, 1, 2, 5]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {0,1,2,3,4}; int l = 1, m = 2, r = 4;
    rotate(A.begin()+l, A.begin()+m, A.begin()+r);
    return 0;
}
```

## fill / iota / unique / remove：一括操作・削除

uniqueとremoveは新しい終端を返す。要素数を減らすにはeraseも必要。

### 全要素をxにする

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
fill(A.begin(), A.end(), x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4; int x = 9;
    fill(A.begin(), A.end(), x);
    return 0;
}
```

### 添字l以上r未満をxにする

計算量：OK / 追加メモリ：O(1)

K：操作する区間の要素数

```cpp
fill(A.begin()+l, A.begin()+r, x);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4; int x = 9;
    fill(A.begin()+l, A.begin()+r, x);
    return 0;
}
```

### 先頭から0,1,2,…を入れる

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
iota(A.begin(), A.end(), 0);
```

⚠︎ 末尾の引数が開始値

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A(5);
    iota(A.begin(), A.end(), 0);
    return 0;
}
```

### 隣接する同じ値を1個にまとめる

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.erase(unique(A.begin(), A.end()), A.end());
```

⚠︎ 隣り合う重複だけが対象。掲載コードはeraseも行うので、要素数も減る

```text
実行前：[1, 1, 2, 1, 1]
uniqueだけ：[1, 2, 1, ?, ?]（要素数は5のまま）
掲載コード（eraseも実行）：[1, 2, 1]
? の位置の値は使わない
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,1,3,3,1};
    A.erase(unique(A.begin(), A.end()), A.end());
    return 0;
}
```

### 配列全体から重複を取り除く

計算量：O(N log N) / 追加メモリ：O(log N)

N：操作前の要素数

```cpp
sort(A.begin(), A.end());
A.erase(unique(A.begin(), A.end()), A.end());
```

⚠︎ 並べ替えるので元の順序は失われる 追加メモリはGCCの一般的な実装の目安

```text
実行前：[3, 1, 3, 2, 1]
実行後：[1, 2, 3]
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4;
    sort(A.begin(), A.end());
    A.erase(unique(A.begin(), A.end()), A.end());
    return 0;
}
```

### 値xの要素を全部削除する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.erase(remove(A.begin(), A.end(), x), A.end());
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4; int x = 1;
    A.erase(remove(A.begin(), A.end(), x), A.end());
    return 0;
}
```

### 条件を満たす要素を全部削除する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
A.erase(remove_if(A.begin(), A.end(), [](int x){
    return x < 0;
}), A.end());
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,-1,4,-2};
    A.erase(remove_if(A.begin(), A.end(), [](int x){
        return x < 0;
    }), A.end());
    return 0;
}
```

### 値xを全部yに置き換える

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
replace(A.begin(), A.end(), x, y);
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {3,1,4,1,5};
    int l = 1, r = 4; int x = 1, y = 9;
    replace(A.begin(), A.end(), x, y);
    return 0;
}
```

## lower_bound / upper_bound / binary_search：二分探索

昇順にソート済みのvectorが前提。Nは配列長。返る位置がNなら該当なし。setではメンバ関数を使う。

### x以上の値が最初に現れる添字を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = lower_bound(A.begin(), A.end(), x) - A.begin();
```

⚠︎ 配列を昇順に並べてあるとき限定。値そのものではなく添字

```text
A = [1, 3, 3, 7]、x = 3
結果：1（最初の3の添字）
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int p = lower_bound(A.begin(), A.end(), x) - A.begin();
    return 0;
}
```

### xより大きい値が最初に現れる添字を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = upper_bound(A.begin(), A.end(), x) - A.begin();
```

⚠︎ 配列を昇順に並べてあるとき限定。値そのものではなく添字

```text
A = [1, 3, 3, 7]、x = 3
結果：3（7の添字）
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int p = upper_bound(A.begin(), A.end(), x) - A.begin();
    return 0;
}
```

### x未満の要素数を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = lower_bound(A.begin(), A.end(), x) - A.begin();
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int cnt = lower_bound(A.begin(), A.end(), x) - A.begin();
    return 0;
}
```

### x以下の要素数を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = upper_bound(A.begin(), A.end(), x) - A.begin();
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int cnt = upper_bound(A.begin(), A.end(), x) - A.begin();
    return 0;
}
```

### x以上の要素数を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = N - (lower_bound(A.begin(), A.end(), x) - A.begin());
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int cnt = N - (lower_bound(A.begin(), A.end(), x) - A.begin());
    return 0;
}
```

### xより大きい要素数を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = N - (upper_bound(A.begin(), A.end(), x) - A.begin());
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int cnt = N - (upper_bound(A.begin(), A.end(), x) - A.begin());
    return 0;
}
```

### xと等しい要素数を求める

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = upper_bound(A.begin(), A.end(), x) - lower_bound(A.begin(), A.end(), x);
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int cnt = upper_bound(A.begin(), A.end(), x) - lower_bound(A.begin(), A.end(), x);
    return 0;
}
```

### xがあるか判定する

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
bool exists = binary_search(A.begin(), A.end(), x);
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    bool exists = binary_search(A.begin(), A.end(), x);
    return 0;
}
```

### x以上で最小の値を読む

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = lower_bound(A.begin(), A.end(), x) - A.begin();
if(p < N){
    int ans = A.at(p);
}
```

⚠︎ 配列を昇順に並べてあるとき限定。p==Nなら該当なし

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int p = lower_bound(A.begin(), A.end(), x) - A.begin();
    if(p < N){
        int ans = A.at(p);
    }
    return 0;
}
```

### x未満で最大の値を読む

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = lower_bound(A.begin(), A.end(), x) - A.begin();
if(p > 0){
    int ans = A.at(p-1);
}
```

⚠︎ 配列を昇順に並べてあるとき限定。p==0なら該当なし

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int p = lower_bound(A.begin(), A.end(), x) - A.begin();
    if(p > 0){
        int ans = A.at(p-1);
    }
    return 0;
}
```

### x以下で最大の値を読む

計算量：O(log N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = upper_bound(A.begin(), A.end(), x) - A.begin();
if(p > 0){
    int ans = A.at(p-1);
}
```

⚠︎ 配列を昇順に並べてあるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {1,3,3,7};
    int N = A.size();
    int x = 3;
    int p = upper_bound(A.begin(), A.end(), x) - A.begin();
    if(p > 0){
        int ans = A.at(p-1);
    }
    return 0;
}
```

## min / max / accumulate / count / find：集計・検索

配列を走査する操作を質問ごとに繰り返すとO(NQ)になる。最小・最大の位置の読み取りは空の配列では使えない。

### 2つの値の小さい方を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
int ans = min(a, b);
```

⚠︎ 2引数の型をそろえる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int a = 3, b = 5;
    int ans = min(a, b);
    return 0;
}
```

### 2つの値の大きい方を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long ans = max(0LL, x);
```

⚠︎ xがlong longなら0LL

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long x = 5;
    long long ans = max(0LL, x);
    return 0;
}
```

### 複数の値の最大を求める

計算量：O(個数) / 追加メモリ：O(1)



```cpp
int ans = max({a, b, c});
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int a = 2, b = 5, c = 3;
    int ans = max({a, b, c});
    return 0;
}
```

### 2つの変数の値を交換する

計算量：O(1) / 追加メモリ：O(1)



```cpp
swap(a, b);
```

⚠︎ intなどの値の場合

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int a = 2, b = 5;
    swap(a, b);
    return 0;
}
```

### 配列の最小値を求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int ans = *min_element(A.begin(), A.end());
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    int ans = *min_element(A.begin(), A.end());
    return 0;
}
```

### 配列の最大値を求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int ans = *max_element(A.begin(), A.end());
```

⚠︎ 容器が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    int ans = *max_element(A.begin(), A.end());
    return 0;
}
```

### 最小値が最初に現れる添字を求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int p = min_element(A.begin(), A.end()) - A.begin();
```

⚠︎ 対象の区間が空のときは使えない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    int p = min_element(A.begin(), A.end()) - A.begin();
    return 0;
}
```

### 添字l以上r未満の最大値を求める

計算量：OK / 追加メモリ：O(1)

K：操作する区間の要素数

```cpp
int ans = *max_element(A.begin()+l, A.begin()+r);
```

⚠︎ 対象の区間が空のときは使えない。l < r

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4; int l = 0, r = 2;
    int ans = *max_element(A.begin()+l, A.begin()+r);
    return 0;
}
```

### 配列の合計をlong longで求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
long long sum = accumulate(A.begin(), A.end(), 0LL);
```

⚠︎ 0ではなく0LLを使う

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    long long sum = accumulate(A.begin(), A.end(), 0LL);
    return 0;
}
```

### 値xの個数を数える

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = count(A.begin(), A.end(), x);
```

⚠︎ ソート不要

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    int cnt = count(A.begin(), A.end(), x);
    return 0;
}
```

### 条件を満たす要素数を求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
int cnt = count_if(A.begin(), A.end(), [](int x){
    return x % 2 == 0;
});
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    int cnt = count_if(A.begin(), A.end(), [](int x){
        return x % 2 == 0;
    });
    return 0;
}
```

### 値xが最初に現れる添字を求める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
auto it = find(A.begin(), A.end(), x);
if(it != A.end()){
    int p = it - A.begin();
}
```

⚠︎ 見つからないとend。ソート不要

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    auto it = find(A.begin(), A.end(), x);
    if(it != A.end()){
        int p = it - A.begin();
    }
    return 0;
}
```

### 全要素が条件を満たすか判定する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
bool ok = all_of(A.begin(), A.end(), [](int x){
    return x >= 0;
});
```

⚠︎ 空ならtrue

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    bool ok = all_of(A.begin(), A.end(), [](int x){
        return x >= 0;
    });
    return 0;
}
```

### 1個以上の要素が条件を満たすか判定する

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
bool ok = any_of(A.begin(), A.end(), [](int x){
    return x >= 0;
});
```

⚠︎ 空ならfalse

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {4,1,7}; int x = 4;
    bool ok = any_of(A.begin(), A.end(), [](int x){
        return x >= 0;
    });
    return 0;
}
```

## gcd / lcm / abs / sqrt：数値計算

intの積は代入先がlong longでも先にintで計算される。1LLを掛けてから計算する。

### 最大公約数を求める

計算量：O(log min(a,b))（正整数） / 追加メモリ：O(1)



```cpp
long long g = gcd(a, b);
```

⚠︎ gcd(0,0)=0。絶対値が型に収まること

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long a = 12, b = 18;
    long long g = gcd(a, b);
    return 0;
}
```

### 最小公倍数を求める

計算量：O(log min(a,b))（正整数） / 追加メモリ：O(1)



```cpp
long long l = lcm(a, b);
```

⚠︎ 最小公倍数が型に収まること

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long a = 12, b = 18;
    long long l = lcm(a, b);
    return 0;
}
```

### 絶対値を求める

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long d = abs(x);
```

⚠︎ long longの最小値の絶対値は型に収まらない

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long x = -5;
    long long d = abs(x);
    return 0;
}
```

### 平方根を実数で求める

計算量：通常 O(1) / 追加メモリ：O(1)



```cpp
double x = sqrt(2.0);
```

⚠︎ 浮動小数点の丸め誤差あり

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    double x = sqrt(2.0);
    return 0;
}
```

### 非負整数aを正整数bで割って切り上げる

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long ans = a/b + (a % b != 0);
```

⚠︎ a ≥ 0、b > 0

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long a = 17, b = 5;
    long long ans = a/b + (a % b != 0);
    return 0;
}
```

### 余りを0以上MOD未満にそろえる

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long r = x % MOD;
if(r < 0){
    r += MOD;
}
```

⚠︎ MOD > 0

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long x = -3, MOD = 5;
    long long r = x % MOD;
    if(r < 0){
        r += MOD;
    }
    return 0;
}
```

### int同士の積をlong longで計算する

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long ans = 1LL * a * b;
```

⚠︎ 最終結果はlong long内に収まること

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int a = 200000, b = 200000;
    long long ans = 1LL * a * b;
    return 0;
}
```

### 型の最大値・最小値を得る

計算量：O(1) / 追加メモリ：O(1)



```cpp
long long hi = numeric_limits<long long>::max();
long long lo = numeric_limits<long long>::lowest();
```

⚠︎ INFに最大値を使って足し算するとあふれる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long hi = numeric_limits<long long>::max();
    long long lo = numeric_limits<long long>::lowest();
    return 0;
}
```

## cin / cout / bitset / next_permutation：入出力・その他

全体コードはC++23 (GCC 15.2.0)。bits/stdc++.hはGCC系環境向け。

### 小数点以下k桁で出力する

計算量：出力文字数に比例 / 追加メモリ：出力バッファは実装依存



```cpp
cout << fixed << setprecision(k) << x << endl;
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    double x = sqrt(2.0); int k = 10;
    cout << fixed << setprecision(k) << x << endl;
    return 0;
}
```

### 大量入出力を高速化する

計算量：設定 O(1) / 追加メモリ：O(1)



```cpp
ios::sync_with_stdio(false);
cin.tie(nullptr);
```

⚠︎ mainの先頭、最初の入出力より前に置く。大量出力は'\n'を使う

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    return 0;
}
```

### 次の辞書順の順列に進める

計算量：O(N) / 追加メモリ：O(1)

N：操作前の要素数

```cpp
bool exists = next_permutation(A.begin(), A.end());
```

⚠︎ 最後の並びから呼ぶと最初の並びに戻ってfalse。全列挙は昇順からdo-while

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    vector<int> A = {0,1,2};
    bool exists = next_permutation(A.begin(), A.end());
    return 0;
}
```

### 整数を固定長の2進文字列にする

計算量：O(B) / 追加メモリ：O(B)

B：bit数

```cpp
string S = bitset<8>(x).to_string();
```

⚠︎ Bはbit数。ここでは8。上位の余分なbitは切り捨てる

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    unsigned long long x = 5;
    string S = bitset<8>(x).to_string();
    return 0;
}
```

### 固定長bit列の1の個数を数える

計算量：O(Bのbit数) / 追加メモリ：O(1)

B：bit数

```cpp
int cnt = B.count();
```

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    bitset<8> B(5);
    int cnt = B.count();
    return 0;
}
```
