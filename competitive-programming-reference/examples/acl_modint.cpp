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
