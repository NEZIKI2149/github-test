# アルゴリズム

名前と機能を1項目ずつ、読みの50音順で掲載。

[入口へ](../README.md)

使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。

## いもす法

**目的** : 区間への加算をすべて行った後、各要素の値を求める

計算量：O(N+Q)　メモリ：O(N)

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

## エラトステネスの篩

**目的** : N以下の整数が素数かをまとめて求める

計算量：O(N log log N)　メモリ：O(N)

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

## 階乗

**目的** : 1からNまでの整数をすべて掛けた値を求める

計算量：O(N)　メモリ：O(1)

⚠︎ この実装はNが0以上20以下のとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    long long ans = 1;
    for(int i = 1;i < N+1;i++){
        ans *= i;
    }
    cout << ans << endl;
    return 0;
}
```

### 階乗の配列を作る

目的 : int型の配列のA.at(i)にiの階乗を入れる

計算量 O(N) / メモリ O(N)

⚠︎ この実装はNが1以上12以下のとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N;
    cin >> N;
    vector<int> A(N+1, 1);
    for(int i = 1;i < N+1;i++){
        A.at(i) = A.at(i-1)*i;
    }
    for(int i = 1;i < N+1;i++){
        cout << A.at(i) << endl;
    }
    return 0;
}
```

## 強連結成分分解（SCC）

**目的** : 有向グラフを、互いに行き来できる頂点ごとに分ける

計算量：O(N+M)　メモリ：O(N+M)

⚠︎ 有向グラフ限定。グループ番号に意味はなく、実行ごとに順序が変わることがある。

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, M;
    cin >> N >> M;
    vector<vector<int>> G(N), revG(N);
    for(int i = 0;i < M;i++){
        int a, b;
        cin >> a >> b;
        a--; b--;
        G.at(a).push_back(b);
        revG.at(b).push_back(a);
    }
    vector<char> seen(N, false);
    vector<int> order;
    for(int s = 0;s < N;s++){
        if(seen.at(s)){
            continue;
        }
        vector<pair<int,int>> st;
        seen.at(s) = true;
        st.push_back({s, 0});
        while(!st.empty()){
            int v = st.back().first;
            int &i = st.back().second;
            if(i < (int)G.at(v).size()){
                int to = G.at(v).at(i);
                i++;
                if(!seen.at(to)){
                    seen.at(to) = true;
                    st.push_back({to, 0});
                }
            }
            else{
                order.push_back(v);
                st.pop_back();
            }
        }
    }
    vector<int> component(N, -1);
    int group_count = 0;
    for(int i = N-1;i >= 0;i--){
        int s = order.at(i);
        if(component.at(s) != -1){
            continue;
        }
        vector<int> st = {s};
        component.at(s) = group_count;
        while(!st.empty()){
            int v = st.back();
            st.pop_back();
            for(int j = 0;j < (int)revG.at(v).size();j++){
                int to = revG.at(v).at(j);
                if(component.at(to) == -1){
                    component.at(to) = group_count;
                    st.push_back(to);
                }
            }
        }
        group_count++;
    }
    cout << group_count << endl;
    for(int v = 0;v < N;v++){
        cout << component.at(v)+1;
        if(v+1 < N){
            cout << " ";
        }
    }
    cout << endl;
    return 0;
}
```

## グリッドBFS

**目的** : 壁のある盤面で、上下左右移動の最短距離を求める

計算量：O(HW)　メモリ：O(HW)

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

## 答えに対する二分探索

**目的** : x² ≥ Kとなる最小整数xを二分探索で求める

計算量：O(log K)　メモリ：O(1)

⚠︎ ある値以上なら必ず条件を満たす問題限定

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

## 最長増加部分列（二重ループ）

**目的** : 狭義単調増加部分列の最大長を求める（二重ループ版）

計算量：O(N²)　メモリ：O(N)

⚠︎ 同じ値を続けて選ぶことはできない

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

## 最長増加部分列（二分探索）

**目的** : 狭義単調増加部分列の最大長を求める（高速版）

計算量：O(N log N)　メモリ：O(N)

⚠︎ 同じ値を続けて選ぶことはできない。tailの中身は、実際に選べる並びとは限らない。

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

## 座標圧縮

**目的** : 値の大小関係を保ったまま、0始まりの順位へ置き換える

計算量：O(N log N)　メモリ：O(N)

⚠︎ 圧縮後の番号の差は、元の値の差にはならない

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

## しゃくとり法

**目的** : 区間の合計がK以下になる、空でない連続部分の個数を数える

計算量：O(N)　メモリ：O(N)

⚠︎ 配列の値がすべて0以上のとき限定

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

## 順列全探索

**目的** : 配列の値の全順列を列挙する

計算量：O(N × N!)　メモリ：O(N)

⚠︎ 同じ値を入れ替えただけの並びは、別の並びとして数えない

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

## 素因数分解

**目的** : 正整数Nを素因数と指数に分解する

計算量：O(√N)　メモリ：O(log N)

⚠︎ 処理後はNの値が変わる。元の値も使うなら先にコピー。

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

## 素数判定（試し割り）

**目的** : 整数Nが素数か判定する

計算量：O(√N)　メモリ：O(1)

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

## ダイクストラ法（Dijkstra）

**目的** : 一方通行のルートで、頂点1から各頂点までの最小の移動コストを求める

計算量：O((N+M) log(N+M))　メモリ：O(N+M)

⚠︎ 各ルートを通るコストがすべて0以上のとき限定

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

## ダブリング

**目的** : 各頂点から決まった回数だけ移動した先を求める

計算量：前処理 O(N log K) / 質問 O(Q log K)　メモリ：O(N log K)

⚠︎ 移動回数Kは0以上10¹⁸以下。各頂点の移動先が1つに決まるとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    int N, Q;
    cin >> N >> Q;
    vector<int> next(N);
    for(int v = 0;v < N;v++){
        cin >> next.at(v);
        next.at(v)--;
    }
    const int LOG = 61;
    vector<vector<int>> jump(LOG, vector<int>(N));
    jump.at(0) = next;
    for(int bit = 1;bit < LOG;bit++){
        for(int v = 0;v < N;v++){
            jump.at(bit).at(v) = jump.at(bit-1).at(jump.at(bit-1).at(v));
        }
    }
    for(int q = 0;q < Q;q++){
        int v;
        long long K;
        cin >> v >> K;
        v--;
        for(int bit = 0;bit < LOG;bit++){
            if((K >> bit) & 1LL){
                v = jump.at(bit).at(v);
            }
        }
        cout << v+1 << endl;
    }
    return 0;
}
```

## 動的計画法（階段）

**目的** : 1段・2段ずつN段上る方法の数を余りで求める

計算量：O(N)　メモリ：O(N)

⚠︎ 余りは998244353で計算する。AtCoder Libraryが必要。

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

## 動的計画法（ナップザック）

**目的** : 各品物を1個まで選び、重さW以下で価値の和を最大化する

計算量：O(NW)　メモリ：O(W)

⚠︎ 重さは0以上の整数限定

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

## トポロジカルソート

**目的** : 有向辺の前後関係を守る順番を求める

計算量：O(N+M)　メモリ：O(N+M)

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

## 二次元累積和

**目的** : 二次元配列の長方形内の和を求める

計算量：O(HW+Q)　メモリ：O(HW)

⚠︎ 盤面の値を途中で書き換えないとき限定

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

## 二部グラフ判定

**目的** : つながっている頂点同士を違う色にして、2色で塗り分けられるか調べる

計算量：O(N+M)　メモリ：O(N+M)

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    // N M、M本の無向辺（頂点1始まり）。塗り分け可能ならYes。
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
    vector<int> color(N, -1);
    bool ok = true;
    for(int s = 0;s < N;s++){
        if(color.at(s) != -1){continue;}
        queue<int> Q;
        color.at(s) = 0;
        Q.push(s);
        while(!Q.empty()){
            int v = Q.front();
            Q.pop();
            for(int i = 0;i < (int)G.at(v).size();i++){
                int to = G.at(v).at(i);
                if(color.at(to) == -1){
                    color.at(to) = 1-color.at(v);
                    Q.push(to);
                }
                else if(color.at(to) == color.at(v)){
                    ok = false;
                }
            }
        }
    }
    cout << (ok ? "Yes" : "No") << endl;
    return 0;
}
```

## 幅優先探索（BFS）

**目的** : 無向・重みなしグラフで頂点1からの最短距離を求める

計算量：O(N+M)　メモリ：O(N+M)

⚠︎ すべてのルートを同じ1回の移動として数えられるとき限定

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

## ビット全探索

**目的** : 各要素を選ぶ・選ばない全組合せで、和がKになる数を数える

計算量：O(N × 2ᴺ)　メモリ：O(N)

⚠︎ 何も選ばない場合も数える。Nは20前後までが目安。

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

## 深さ優先探索（DFS）

**目的** : 開始地点から、行ける頂点を順番に調べる

計算量：O(N+M)　メモリ：O(N+M)

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    // N M、M本の無向辺（頂点1始まり）、開始頂点。訪問順を出力。
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
    int start;
    cin >> start;
    start--;
    vector<char> seen(N, false);
    vector<int> st = {start};
    while(!st.empty()){
        int v = st.back();
        st.pop_back();
        if(seen.at(v)){continue;}
        seen.at(v) = true;
        cout << v+1 << endl;
        for(int i = (int)G.at(v).size()-1;i >= 0;i--){
            int to = G.at(v).at(i);
            if(!seen.at(to)){
                st.push_back(to);
            }
        }
    }
    return 0;
}
```

## ペア数の数え上げ（同じ値）

**目的** : 同じ値を持つ添字のペア数を求める

計算量：O(N log N)　メモリ：O(値の種類数)

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

## 約数列挙

**目的** : 正整数Nの約数を昇順に列挙する

計算量：O(√N + D log D)　メモリ：O(D)（Dは約数の個数）

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

## ランレングス圧縮

**目的** : 同じ文字が連続する部分を、文字と個数にまとめる

計算量：O(N)　メモリ：O(N)

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    // 空白を含まない文字列S。各連続部分の文字と個数を出力。
    string S;
    cin >> S;
    vector<pair<char,int>> runs;
    for(int i = 0;i < (int)S.size();i++){
        if(runs.empty() || runs.back().first != S.at(i)){
            runs.push_back({S.at(i), 1});
        }
        else{
            runs.back().second++;
        }
    }
    for(int i = 0;i < (int)runs.size();i++){
        cout << runs.at(i).first << " " << runs.at(i).second << endl;
    }
    return 0;
}
```

## 累積和

**目的** : 更新なしの配列で、区間の和を繰り返し求める

計算量：O(N+Q)　メモリ：O(N)

⚠︎ 配列の値を途中で書き換えないとき限定

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

## 連結成分分解（無向グラフ）

**目的** : 道でつながっている頂点ごとにグループ分けする

計算量：O(N+M)　メモリ：O(N+M)

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    // N M、M本の無向辺（頂点1始まり）。成分数と各頂点のグループ番号を出力。
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
    vector<int> component(N, -1);
    int count = 0;
    for(int s = 0;s < N;s++){
        if(component.at(s) != -1){continue;}
        vector<int> st = {s};
        component.at(s) = count;
        while(!st.empty()){
            int v = st.back();
            st.pop_back();
            for(int i = 0;i < (int)G.at(v).size();i++){
                int to = G.at(v).at(i);
                if(component.at(to) == -1){
                    component.at(to) = count;
                    st.push_back(to);
                }
            }
        }
        count++;
    }
    cout << count << endl;
    for(int v = 0;v < N;v++){
        cout << component.at(v)+1 << (v+1 == N ? '\n' : ' ');
    }
    return 0;
}
```

## ワーシャルフロイド法

**目的** : すべての頂点の組合せについて、最短距離をまとめて求める

計算量：O(N³+M)　メモリ：O(N²)

⚠︎ この実装は、各ルートを通るコストが0以上のとき限定

```cpp
// Reference: https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference
#include <bits/stdc++.h>
using namespace std;

int main(){
    // N M、M本の有向辺 a b cost（頂点1始まり）。距離行列を出力、到達不可は-1。有限の距離はINF未満。
    int N, M;
    cin >> N >> M;
    const long long INF = 4000000000000000000LL;
    vector<vector<long long>> dist(N, vector<long long>(N, INF));
    for(int v = 0;v < N;v++){dist.at(v).at(v) = 0;}
    for(int i = 0;i < M;i++){
        int a, b;
        long long cost;
        cin >> a >> b >> cost;
        a--; b--;
        dist.at(a).at(b) = min(dist.at(a).at(b), cost);
    }
    for(int k = 0;k < N;k++){
        for(int i = 0;i < N;i++){
            for(int j = 0;j < N;j++){
                if(dist.at(i).at(k) == INF || dist.at(k).at(j) == INF){continue;}
                dist.at(i).at(j) = min(dist.at(i).at(j), dist.at(i).at(k)+dist.at(k).at(j));
            }
        }
    }
    for(int i = 0;i < N;i++){
        for(int j = 0;j < N;j++){
            cout << (dist.at(i).at(j) == INF ? -1 : dist.at(i).at(j));
            cout << (j+1 == N ? '\n' : ' ');
        }
    }
    return 0;
}
```
