# 定番アルゴリズム・実装

名前と機能を1項目ずつ、読みの50音順で掲載。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

## いもす法

添字と区間は0始まり。和・加算結果はlong longに収まること。

### 区間への加算をすべて行った後、各要素の値を求める

計算量：更新合計 O(Q) / 復元 O(N) / メモリ O(N)

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, Q;
    cin >> N >> Q;
    vector<long long> D(N+1, 0);
    for(int i = 0;i < Q;i++){
        int l, r;
        long long x;
        cin >> l >> r >> x; // 添字l以上r未満
        D.at(l) += x;
        D.at(r) -= x;
    }
    for(int i = 0;i < N;i++){
        if(i > 0){
            D.at(i) += D.at(i-1);
        }
        cout << D.at(i) << endl;
    }
    return 0;
}
```

</details>

## エラトステネスの篩

### N以下の整数が素数かをまとめて求める

計算量：時間 O(N log log N) / メモリ O(N)

N ≥ 0。vector<char>の0/1で管理する。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<char> prime(N+1, true);
    prime.at(0) = false;
    if(N >= 1){
        prime.at(1) = false;
    }
    for(long long x = 2;x*x <= N;x++){
        if(!prime.at(x)){
            continue;
        }
        for(long long y = x*x;y <= N;y += x){
            prime.at(y) = false;
        }
    }
    for(int x = 2;x <= N;x++){
        if(prime.at(x)){
            cout << x << endl;
        }
    }
    return 0;
}
```

</details>

## 階段DP

### 1段・2段ずつN段上る方法の数を余りで求める

計算量：時間 O(N) / メモリ O(N)

法998244353。ACLが必要。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
#include <atcoder/modint>
using namespace std;
using mint = atcoder::modint998244353;

// 入力: N (0 <= N <= 10^6 を想定)
// 出力: 1段/2段ずつN段上る方法の数を998244353で割った余り
int main(){
    int N;
    cin >> N;
    vector<mint> dp(N+2, 0);
    dp.at(N) = 1;
    for(int i = N-1;i >= 0;i--){
        dp.at(i) = dp.at(i+1) + dp.at(i+2);
    }
    cout << dp.at(0).val() << endl;
}
```

</details>

## グリッドBFS

### 壁のある盤面で、上下左右移動の最短距離を求める

計算量：時間 O(HW) / メモリ O(HW)

入力はH W、開始h w、目標h w、盤面。座標0始まり、#は壁。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int H, W, sh, sw, gh, gw;
    cin >> H >> W >> sh >> sw >> gh >> gw;
    vector<string> S(H);
    for(int h = 0;h < H;h++){
        cin >> S.at(h);
    }
    vector<vector<int>> dist(H, vector<int>(W, -1));
    queue<pair<int,int>> Q;
    if(S.at(sh).at(sw) != '#'){
        dist.at(sh).at(sw) = 0;
        Q.push({sh, sw});
    }
    vector<int> dh = {1,0,-1,0}, dw = {0,1,0,-1};
    while(!Q.empty()){
        int h = Q.front().first, w = Q.front().second;
        Q.pop();
        for(int k = 0;k < 4;k++){
            int nh = h+dh.at(k), nw = w+dw.at(k);
            if(nh < 0 || nh >= H || nw < 0 || nw >= W){
                continue;
            }
            if(S.at(nh).at(nw) == '#' || dist.at(nh).at(nw) != -1){
                continue;
            }
            dist.at(nh).at(nw) = dist.at(h).at(w)+1;
            Q.push({nh,nw});
        }
    }
    cout << dist.at(gh).at(gw) << endl;
    return 0;
}
```

</details>

## 答えに対する二分探索

### x² ≥ Kとなる最小整数xを二分探索で求める

計算量：時間 O(log K) / メモリ O(1)

1 ≤ K ≤ 10¹⁸。一般の問題では判定と初期ok/ngを両方変更する。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

// 入力: K (1 <= K <= 10^18)
// 出力: x*x >= K となる最小の非負整数x
int main(){
    long long K;
    cin >> K;
    long long ng = 0;
    long long ok = K;
    while(ok-ng > 1){
        long long mid = ng + (ok-ng)/2;
        long long required = K/mid + (K % mid != 0);
        if(mid >= required){
            ok = mid;
        }
        else{
            ng = mid;
        }
    }
    cout << ok << endl;
}
```

</details>

## 最長増加部分列（二重ループ）

### 狭義単調増加部分列の最大長を求める（二重ループ版）

計算量：時間 O(N²) / メモリ O(N)

同じ値を連続して選ばない。高速版のtail全体は実際の部分列とは限らない。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<int> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }

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
    cout << ans << endl;
    return 0;
}
```

</details>

## 最長増加部分列（二分探索）

### 狭義単調増加部分列の最大長を求める（高速版）

計算量：時間 O(N log N) / メモリ O(N)

同じ値を連続して選ばない。高速版のtail全体は実際の部分列とは限らない。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<int> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }

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
    return 0;
}
```

</details>

## 座標圧縮

### 値の大小関係を保ったまま、0始まりの順位へ置き換える

計算量：時間 O(N log N) / メモリ O(N)

値の差・距離は保たない。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<long long> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }
    vector<long long> B = A;
    sort(B.begin(), B.end());
    B.erase(unique(B.begin(), B.end()), B.end());
    for(int i = 0;i < N;i++){
        int p = lower_bound(B.begin(), B.end(), A.at(i)) - B.begin();
        cout << p << endl;
    }
    return 0;
}
```

</details>

## しゃくとり法

### 非負配列で、区間和がK以下の空でない連続部分列を数える

計算量：時間 O(N) / メモリ O(N)

Aの全要素 ≥ 0、K ≥ 0。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    long long K;
    cin >> N >> K;
    vector<long long> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }
    int r = 0;
    long long sum = 0, ans = 0;
    for(int l = 0;l < N;l++){
        while(r < N && sum + A.at(r) <= K){
            sum += A.at(r);
            r++;
        }
        ans += r-l;
        if(r == l){
            r++;
        }
        else{
            sum -= A.at(l);
        }
    }
    cout << ans << endl;
    return 0;
}
```

</details>

## 順列全探索

### 配列の値の全順列を列挙する

計算量：時間 O(N × N!) / メモリ O(N)

同じ値の並びは重複して出力しない。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<int> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }
    sort(A.begin(), A.end());
    do{
        for(int i = 0;i < N;i++){
            if(i > 0){
                cout << " ";
            }
            cout << A.at(i);
        }
        cout << endl;
    }while(next_permutation(A.begin(), A.end()));
    return 0;
}
```

</details>

## 素因数分解

### 正整数Nを素因数と指数に分解する

計算量：時間 O(√N) / メモリ O(log N)

N ≥ 1。N自体を途中で変更する。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long N;
    cin >> N;
    vector<pair<long long,int>> factors;
    for(long long x = 2;x <= N/x;x++){
        int cnt = 0;
        while(N % x == 0){
            N /= x;
            cnt++;
        }
        if(cnt > 0){
            factors.push_back({x,cnt});
        }
    }
    if(N > 1){
        factors.push_back({N,1});
    }
    for(int i = 0;i < (int)factors.size();i++){
        cout << factors.at(i).first << " " << factors.at(i).second << endl;
    }
    return 0;
}
```

</details>

## 素数判定（試し割り）

### 整数Nが素数か判定する

計算量：時間 O(√N) / 追加メモリ O(1)

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

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

int main(){
    long long N;
    cin >> N;
    cout << (is_prime(N) ? "Yes" : "No") << endl;
    return 0;
}
```

</details>

## ダイクストラ法（Dijkstra）

### 非負重みの有向グラフで頂点1からの最短距離を求める

計算量：時間 O((N+M) log(N+M)) / メモリ O(N+M)

重み ≥ 0。有限の最短距離 < INF、距離+重みがlong long内。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

// 入力: N M、続いてM本の有向辺 a b cost (頂点は1始まり)
// N >= 1、cost >= 0、有限の最短距離はINF未満、距離+costはlong long内
// 出力: 頂点1から各頂点への最短距離。到達不可は-1
int main(){
    int N, M;
    cin >> N >> M;
    vector<vector<pair<int, long long>>> G(N);
    for(int i = 0;i < M;i++){
        int a, b;
        long long cost;
        cin >> a >> b >> cost;
        a--; b--;
        G.at(a).push_back({b, cost});
        // 無向グラフなら次の行も有効にする
        // G.at(b).push_back({a, cost});
    }
    const long long INF = (1LL << 60);
    vector<long long> dist(N, INF);
    priority_queue<pair<long long, int>, vector<pair<long long, int>>,
                   greater<pair<long long, int>>> Q;
    dist.at(0) = 0;
    Q.push({0, 0});
    while(!Q.empty()){
        long long d = Q.top().first;
        int v = Q.top().second;
        Q.pop();
        if(d != dist.at(v)){
            continue;
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
    for(int i = 0;i < N;i++){
        if(dist.at(i) == INF){
            cout << -1 << endl;
        }
        else{
            cout << dist.at(i) << endl;
        }
    }
}
```

</details>

## トポロジカルソート

### 有向辺の前後関係を守る順番を求める

計算量：時間 O(N+M) / メモリ O(N+M)

N M、M本の有向辺a b（1始まり）を入力。閉路があれば−1。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, M;
    cin >> N >> M;
    vector<vector<int>> G(N);
    vector<int> indeg(N, 0);
    for(int i = 0;i < M;i++){
        int a, b;
        cin >> a >> b;
        a--; b--;
        G.at(a).push_back(b);
        indeg.at(b)++;
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
    if((int)order.size() != N){
        cout << -1 << endl;
    }
    else{
        for(int i = 0;i < N;i++){
            cout << order.at(i)+1 << endl;
        }
    }
    return 0;
}
```

</details>

## ナップサックDP（0/1）

### 各品物を1個まで選び、重さW以下で価値の和を最大化する

計算量：時間 O(NW) / メモリ O(W)

N W、各品物の重さ・価値を入力。重さは正整数。価値の合計はlong long内。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, W;
    cin >> N >> W;
    vector<long long> dp(W+1, 0);
    for(int i = 0;i < N;i++){
        int weight;
        long long value;
        cin >> weight >> value;
        for(int w = W;w >= weight;w--){
            dp.at(w) = max(dp.at(w), dp.at(w-weight)+value);
        }
    }
    cout << dp.at(W) << endl;
    return 0;
}
```

</details>

## 二次元累積和

添字と区間は0始まり。和・加算結果はlong longに収まること。

### 二次元配列の長方形内の和を求める

計算量：前処理 O(HW) / 質問 O(1) / メモリ O(HW)

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int H, W, Q;
    cin >> H >> W >> Q;
    vector<vector<long long>> S(H+1, vector<long long>(W+1, 0));
    for(int h = 0;h < H;h++){
        for(int w = 0;w < W;w++){
            long long x;
            cin >> x;
            S.at(h+1).at(w+1) = x + S.at(h).at(w+1) + S.at(h+1).at(w) - S.at(h).at(w);
        }
    }
    for(int i = 0;i < Q;i++){
        int h1, w1, h2, w2;
        cin >> h1 >> w1 >> h2 >> w2; // 行[h1,h2)、列[w1,w2)
        long long ans = S.at(h2).at(w2)-S.at(h1).at(w2)-S.at(h2).at(w1)+S.at(h1).at(w1);
        cout << ans << endl;
    }
    return 0;
}
```

</details>

## 幅優先探索（BFS）

### 無向・重みなしグラフで頂点1からの最短距離を求める

計算量：時間 O(N+M) / メモリ O(N+M)

頂点番号は入力が1始まり、内部は0始まり。到達不可は−1。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

// 入力: N M、続いてM本の無向辺 a b (頂点は1始まり)。N >= 1
// 出力: 頂点1から各頂点への最短距離。到達不可は-1
int main(){
    int N, M;
    cin >> N >> M;
    vector<vector<int>> G(N);
    for(int i = 0;i < M;i++){
        int a, b;
        cin >> a >> b;
        a--; b--;
        G.at(a).push_back(b);
        G.at(b).push_back(a);
    }
    vector<int> dist(N, -1);
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
    for(int i = 0;i < N;i++){
        cout << dist.at(i) << endl;
    }
}
```

</details>

## ビット全探索

### 各要素を選ぶ・選ばない全組合せで、和がKになる数を数える

計算量：時間 O(N × 2ᴺ) / メモリ O(N)

空集合も含む。Nは典型的には20前後。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    long long K;
    cin >> N >> K;
    vector<long long> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }
    long long ans = 0;
    for(long long bit = 0;bit < (1LL << N);bit++){
        long long sum = 0;
        for(int i = 0;i < N;i++){
            if((bit >> i) & 1LL){
                sum += A.at(i);
            }
        }
        if(sum == K){
            ans++;
        }
    }
    cout << ans << endl;
    return 0;
}
```

</details>

## ペア数の数え上げ（同じ値）

### 同じ値を持つ**添字**のペア数を求める

計算量：時間 O(N log N) / メモリ O(値の種類数)

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    map<long long, long long> cnt;
    for(int i = 0;i < N;i++){
        long long x;
        cin >> x;
        cnt[x]++;
    }
    long long ans = 0;
    for(auto it = cnt.begin();it != cnt.end();it++){
        long long num = it->second;
        ans += num*(num-1)/2;
    }
    cout << ans << endl;
    return 0;
}
```

</details>

## 約数列挙

### 正整数Nの約数を昇順に列挙する

計算量：時間 O(√N + D log D) / メモリ O(D)

Dは約数の個数。N ≥ 1。

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    long long N;
    cin >> N;
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
    for(int i = 0;i < (int)D.size();i++){
        cout << D.at(i) << endl;
    }
    return 0;
}
```

</details>

## 累積和

添字と区間は0始まり。和・加算結果はlong longに収まること。

### 更新なしの配列で、区間の和を繰り返し求める

計算量：前処理 O(N) / 質問 O(1) / メモリ O(N)

<details>
<summary>コンパイルできる全体コード</summary>

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, Q;
    cin >> N >> Q;
    vector<long long> A(N), S(N+1, 0);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
        S.at(i+1) = S.at(i) + A.at(i);
    }
    for(int i = 0;i < Q;i++){
        int l, r;
        cin >> l >> r; // 添字l以上r未満
        cout << S.at(r)-S.at(l) << endl;
    }
    return 0;
}
```

</details>
