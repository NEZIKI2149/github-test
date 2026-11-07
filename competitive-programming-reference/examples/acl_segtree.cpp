#include <bits/stdc++.h>
#include <atcoder/segtree>
using namespace std;

long long op(long long a, long long b){
    return min(a, b);
}
long long e(){
    return numeric_limits<long long>::max();
}

// 入力: N Q、初期配列A、続いてQ個の操作 (添字は0始まり)
// 0 p x: A[p] = x。1 l r: [l,r)の最小値を出力
// 空区間ではe()、つまりlong longの最大値を出力
int main(){
    int N, Q;
    cin >> N >> Q;
    vector<long long> A(N);
    for(int i = 0;i < N;i++){
        cin >> A.at(i);
    }
    atcoder::segtree<long long, op, e> seg(A);
    for(int i = 0;i < Q;i++){
        int t;
        cin >> t;
        if(t == 0){
            int p;
            long long x;
            cin >> p >> x;
            seg.set(p, x);
        }
        else{
            int l, r;
            cin >> l >> r;
            cout << seg.prod(l, r) << endl;
        }
    }
}
