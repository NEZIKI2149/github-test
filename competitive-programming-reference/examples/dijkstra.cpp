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
