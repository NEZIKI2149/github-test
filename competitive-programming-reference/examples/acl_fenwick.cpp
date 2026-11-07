#include <bits/stdc++.h>
#include <atcoder/fenwicktree>
using namespace std;

// 入力: N Q、初期配列A、続いてQ個の操作 (添字は0始まり)
// 0 p x: A[p] += x。1 l r: [l,r)の和を出力
// 全要素・区間和はlong longの範囲内
int main(){
    int N, Q;
    cin >> N >> Q;
    atcoder::fenwick_tree<long long> F(N);
    for(int i = 0;i < N;i++){
        long long x;
        cin >> x;
        F.add(i, x);
    }
    for(int i = 0;i < Q;i++){
        int t;
        cin >> t;
        if(t == 0){
            int p;
            long long x;
            cin >> p >> x;
            F.add(p, x);
        }
        else{
            int l, r;
            cin >> l >> r;
            cout << F.sum(l, r) << endl;
        }
    }
}
