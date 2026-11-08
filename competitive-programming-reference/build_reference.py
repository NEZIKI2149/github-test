"""Python 3: 静的HTMLとMarkdownを同じデータから生成する。外部依存なし。"""
import html
import json
import math
import pathlib
import re
import textwrap
import unicodedata
from operation_metadata import enrich

ROOT = pathlib.Path(__file__).resolve().parent
PUBLIC = "https://github.com/NEZIKI2149/github-test/tree/master/competitive-programming-reference"
GROUPS = []
HIDDEN_GROUPS = {"dsu", "fenwick", "segtree"}


def group(page, key, title, note=""):
    g = dict(page=page, key=key, title=title, note=note, items=[])
    GROUPS.append(g)
    return g


def program(body, before="", includes=""):
    body = textwrap.dedent(body).strip()
    return ("#include <bits/stdc++.h>\n" + includes + "using namespace std;\n\n" + before
            + "int main(){\n" + textwrap.indent(body, "    ") + "\n    return 0;\n}\n")


def add(g, desc, code, cost, setup="", note="", body=None, before="", includes="", input="", expected=None):
    full = program(body if body is not None else setup + "\n" + code, before, includes)
    key = g["key"] + "-" + str(len(g["items"])+1)
    g["items"].append(dict(id=key, desc=desc, code=code, cost=cost, note=note,
                           full=full, input=input, expected=expected))


g = group("std", "vector", "vector：可変長の配列", "Nは現在の要素数。front・back・pop_backは空の配列に使わない。atは範囲外で例外になる。")
V = "vector<int> A = {3, 1, 4, 1, 5};\nint N = A.size();\nint i = 2, x = 9, l = 1, r = 4;"
for desc, code, cost, note in [
    ("N個の要素を0で初期化する", "vector<int> A(N, 0);", "O(N)", ""),
    ("H行W列を−1で初期化する", "vector<vector<int>> A(H, vector<int>(W, -1));", "O(HW)", ""),
    ("添字iの要素を読む", "int x = A.at(i);", "O(1)", "0 ≤ i < N"),
    ("添字iの要素を変更する", "A.at(i) = x;", "O(1)", "0 ≤ i < N"),
    ("先頭の要素を読む", "int x = A.front();", "O(1)", "空でないこと"),
    ("末尾の要素を読む", "int x = A.back();", "O(1)", "空でないこと"),
    ("要素数を求める", "int N = A.size();", "O(1)", "size()自体は符号なし整数を返す"),
    ("空か判定する", "bool empty = A.empty();", "O(1)", ""),
    ("末尾にxを追加する", "A.push_back(x);", "ならし O(1)", ""),
    ("末尾の1要素を削除する", "A.pop_back();", "O(1)", "値は返さない。空でないこと"),
    ("添字iの直前にxを挿入する", "A.insert(A.begin()+i, x);", "O(N)", "0 ≤ i ≤ N。後ろの添字がずれる"),
    ("添字iの1要素を削除する", "A.erase(A.begin()+i);", "O(N)", "後ろの添字がずれる"),
    ("添字l以上r未満を削除する", "A.erase(A.begin()+l, A.begin()+r);", "O(N)", "0 ≤ l ≤ r ≤ N"),
    ("要素数をNにする", "A.resize(N, -1);", "O(N + 変更前の要素数)", "増えた要素だけ−1。減らした部分は失われる"),
    ("N要素ぶんの容量を予約する", "A.reserve(N);", "再確保時 O(現在の要素数)", "要素数は増えない。atで新しい位置を読めるようにはならない"),
    ("全体をxがN個の配列に置き換える", "A.assign(N, x);", "O(N + 変更前の要素数)", ""),
    ("全要素を削除する", "A.clear();", "O(N)", "確保済みの容量は通常残る"),
    ("配列全体をコピーする", "vector<int> B = A;", "O(N)", "Bにも要素ぶんのメモリが必要"),
]:
    setup = V
    if code.startswith("vector<int> A(N"):
        setup = "int N = 5;"
    elif code.startswith("vector<vector"):
        setup = "int H = 3, W = 4;"
    elif code == "int x = A.at(i);" or code.startswith("int x = A."):
        setup = "vector<int> A = {3,1,4};\nint i = 1;"
    elif code == "int N = A.size();":
        setup = "vector<int> A = {3,1,4};"
    add(g, desc, code, cost, setup, note)

g = group("std", "string", "string：文字列", "Nは文字列長、Kは対象の文字数。添字は0始まり。末尾の読み取り・削除は空なら使わない。")
S = 'string S = "abcabc";\nint i = 1, pos = 1, k = 3;\nchar c = \'x\';\nstring T = "bc";'
specs = [
    ("同じ文字をN個並べる", "string S(N, 'a');", "O(N)", "int N = 5;", ""),
    ("添字iの文字を読む", "char c = S.at(i);", "O(1)", 'string S = "abc"; int i = 1;', ""),
    ("添字iの文字を変更する", "S.at(i) = c;", "O(1)", S, ""),
    ("文字数を求める", "int N = S.size();", "O(1)", S, ""),
    ("空か判定する", "bool empty = S.empty();", "O(1)", S, ""),
    ("末尾に1文字追加する", "S.push_back(c);", "ならし O(1)", S, ""),
    ("末尾に文字列Tを連結する", "S += T;", "ならし O(Tの長さ)", S, "再確保時は元の文字列のコピーも発生"),
    ("末尾の文字を読む", "char last = S.back();", "O(1)", S, "空でないこと"),
    ("末尾の1文字を削除する", "S.pop_back();", "O(1)", S, "空でないこと"),
    ("添字posからk文字を取り出す", "string U = S.substr(pos, k);", "O(取り出す文字数)", S, "第2引数は終点ではなく文字数。残りがk未満なら末尾まで"),
    ("添字posから末尾まで取り出す", "string U = S.substr(pos);", "O(N−pos)", S, "0 ≤ pos ≤ N"),
    ("文字列Tが最初に現れる位置を探す", "size_t p = S.find(T);", "最悪 O(N × Tの長さ)", S, "なければstring::npos。文字1個の検索はO(N)"),
    ("添字pos以降で文字列Tを探す", "size_t p = S.find(T, pos);", "最悪 O(N × Tの長さ)", S, "posから検索開始"),
    ("文字列Tが最後に現れる位置を探す", "size_t p = S.rfind(T);", "最悪 O(N × Tの長さ)", S, "なければstring::npos"),
    ("検索結果が見つかったか判定する", "bool found = p != string::npos;", "O(1)", S+'\nsize_t p = S.find(T);', "見つからない位置をatで読まない"),
    ("添字posの直前にTを挿入する", "S.insert(pos, T);", "O(N + Tの長さ)", S, "0 ≤ pos ≤ N"),
    ("添字posからk文字を削除する", "S.erase(pos, k);", "O(N)", S, "第2引数は文字数"),
    ("添字posからk文字をTに置き換える", "S.replace(pos, k, T);", "O(N + Tの長さ)", S, "第2引数は文字数"),
    ("文字列の大小を辞書順で比較する", "bool smaller = S < T;", "O(比較する文字数)", S, "大文字・小文字などは文字コード順"),
    ("文字の数字を整数にする", "int x = c - '0';", "O(1)", "char c = '7';", "cが'0'〜'9'であること"),
    ("英小文字を0〜25の番号にする", "int x = c - 'a';", "O(1)", "char c = 'c';", "英小文字を前提とする"),
    ("文字列をintに変換する", "int x = stoi(S);", "O(読み取る文字数)", 'string S = "123";', "変換不能・型の範囲外で例外。先頭の数値部分だけを読む場合がある"),
    ("文字列をlong longに変換する", "long long x = stoll(S);", "O(読み取る文字数)", 'string S = "12345678900";', "変換不能・型の範囲外で例外"),
    ("整数を文字列に変換する", "string S = to_string(x);", "O(桁数)", "long long x = 123;", ""),
    ("空白を含む1行を読み取る", "getline(cin, S);", "O(読み取る文字数)", "string S;", "直前の >> が残した改行に注意"),
    ("整数入力の後に、次の1行を読み取る", "cin.ignore(numeric_limits<streamsize>::max(), '\\n');\ngetline(cin, S);", "O(読み捨てる文字数 + 読む文字数)", "int N;\ncin >> N;\nstring S;", "行末まで捨ててから読む。次の行の先頭空白は保持"),
]
for desc, code, cost, setup, note in specs:
    add(g, desc, code, cost, setup, note, input="1\nhello world\n")

g = group("std", "set", "set / multiset：順序つきの集合", "setは重複なし、multisetは重複あり。添字アクセス不可。Kは同じ値の個数。")
for desc, code, cost, setup, note in [
    ("重複なしの集合を作る", "set<int> S;", "O(1)", "", ""),
    ("重複ありの集合を作る", "multiset<int> S;", "O(1)", "", ""),
    ("xを追加する", "S.insert(x);", "O(log N)", "set<int> S; int x = 3;", "setでは同じ値は増えない"),
    ("xがあるか判定する", "bool exists = S.find(x) != S.end();", "O(log N)", "set<int> S = {2,5,9}; int x = 5;", "multisetでも同じ"),
    ("要素数を求める", "int N = S.size();", "O(1)", "multiset<int> S = {2,5,5};", "multisetでは重複も数える"),
    ("xの個数を求める", "int cnt = S.count(x);", "set: O(log N) / multiset: O(log N + K)", "multiset<int> S = {2,5,5}; int x = 5;", ""),
    ("xをすべて削除する", "S.erase(x);", "O(log N + 削除数)", "multiset<int> S = {2,5,5}; int x = 5;", "multisetでは同じ値が全部消える"),
    ("xを1個だけ削除する", "auto it = S.find(x);\nif(it != S.end()){\n    S.erase(it);\n}", "検索 O(log N) / 位置指定削除はならし O(1)", "multiset<int> S = {2,5,5}; int x = 5;", "存在しない場合は削除しない"),
    ("最小値を読む", "int x = *S.begin();", "O(1)", "set<int> S = {2,5,9};", "空でないこと"),
    ("最大値を読む", "int x = *S.rbegin();", "O(1)", "set<int> S = {2,5,9};", "空でないこと"),
    ("最小値を1個削除する", "S.erase(S.begin());", "ならし O(1)", "multiset<int> S = {2,5,5};", "空でないこと"),
    ("x以上の最小値を探す", "auto it = S.lower_bound(x);\nif(it != S.end()){\n    int ans = *it;\n}", "O(log N)", "set<int> S = {2,5,9}; int x = 6;", "endなら該当なし"),
    ("xより大きい最小値を探す", "auto it = S.upper_bound(x);\nif(it != S.end()){\n    int ans = *it;\n}", "O(log N)", "set<int> S = {2,5,9}; int x = 5;", ""),
    ("x未満の最大値を探す", "auto it = S.lower_bound(x);\nif(it != S.begin()){\n    it--;\n    int ans = *it;\n}", "O(log N)", "set<int> S = {2,5,9}; int x = 6;", "beginから前に戻さない"),
    ("x以下の最大値を探す", "auto it = S.upper_bound(x);\nif(it != S.begin()){\n    it--;\n    int ans = *it;\n}", "O(log N)", "set<int> S = {2,5,9}; int x = 5;", ""),
    ("小さい順に全要素を読む", "for(auto it = S.begin();it != S.end();it++){\n    cout << *it << endl;\n}", "O(N)", "set<int> S = {2,5,9};", ""),
]:
    add(g, desc, code, cost, setup, note)
g["note"] += " setではS.lower_bound(x)を使う。lower_bound(S.begin(), S.end(), x)やdistanceによる順位取得はO(N)の移動が発生する。"

g = group("std", "map", "map / unordered_map：キーごとの値", "Kはキーの種類数。mapの操作はO(log K)。文字列キーでは比較する文字数も考慮する。")
for desc, code, cost, setup, note in [
    ("整数ごとに回数を持つ", "map<int, long long> cnt;", "構築 O(1)", "", ""),
    ("文字列ごとに回数を持つ", "map<string, int> cnt;", "構築 O(1)", "", ""),
    ("xの回数を1増やす", "cnt[x]++;", "O(log K)", "map<int, long long> cnt; int x = 5;", "キーがなければ0から始まる"),
    ("キーxの値を読む", "long long num = cnt[x];", "O(log K)", "map<int, long long> cnt; int x = 5;", "キーがないと値0の要素を追加する"),
    ("キーxがあるか判定する", "bool exists = cnt.count(x) > 0;", "O(log K)", "map<int, long long> cnt; int x = 5;", "値が0かどうかとは別。要素は追加しない"),
    ("キーxがあれば値を読む", "auto it = cnt.find(x);\nif(it != cnt.end()){\n    long long num = it->second;\n}", "O(log K)", "map<int, long long> cnt; int x = 5;", "要素を追加しない"),
    ("キーxとその値を削除する", "cnt.erase(x);", "O(log K)", "map<int, long long> cnt; int x = 5;", "値を0にするだけではキーは消えない"),
    ("キーの種類数を求める", "int kinds = cnt.size();", "O(1)", "map<int, long long> cnt;", ""),
    ("キーの昇順にキーと値を読む", "for(auto it = cnt.begin();it != cnt.end();it++){\n    cout << it->first << \" \" << it->second << endl;\n}", "O(K)", "map<int, long long> cnt = {{5,2},{2,1}};", "firstがキー、secondが値"),
    ("順序なしの対応表を作る", "unordered_map<int, int> M;", "検索等は平均 O(1) / 最悪 O(K)", "", "lower_bound・大小順の走査は不可"),
    ("順序なしの重複しない集合を作る", "unordered_set<int> S;", "検索等は平均 O(1) / 最悪 O(N)", "", "順序不要でも最悪計算量に注意"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "queue", "queue / stack / deque：取り出す順番", "読む・削除する前に空でないことを確認する。popは値を返さない。")
for name, decl, push, read, pop in [
    ("queue：先に入れた順", "queue<int> Q;", "Q.push(x);", "Q.front()", "Q.pop();"),
    ("stack：後に入れた順", "stack<int> Q;", "Q.push(x);", "Q.top()", "Q.pop();"),
]:
    add(g, name+"で取り出す容器を作る", decl, "O(1)")
    add(g, name+"の容器へ追加する", push, "O(1)", decl+" int x = 3;")
    add(g, name+"の次の値を読む", "int ans = "+read+";", "O(1)", decl+" Q.push(3);", "空でないこと")
    add(g, name+"の次の要素を削除する", pop, "O(1)", decl+" Q.push(3);", "空でないこと")
add(g, "空か判定する（各容器共通）", "bool empty = Q.empty();", "O(1)", "queue<int> Q;")
add(g, "要素数を求める（各容器共通）", "int N = Q.size();", "O(1)", "queue<int> Q;")
for desc, code in [
    ("両端から操作できる配列を作る", "deque<int> D;"),
    ("先頭にxを追加する", "D.push_front(x);"),
    ("末尾にxを追加する", "D.push_back(x);"),
    ("先頭の要素を削除する", "D.pop_front();"),
    ("末尾の要素を削除する", "D.pop_back();"),
    ("添字iの要素を読む", "int ans = D.at(i);"),
]:
    add(g, desc, code, "O(1)", "" if code.startswith("deque") else "deque<int> D = {1,2,3}; int x = 9, i = 1;",
        "削除する場合は空でないこと" if "pop_" in code else "")

g = group("std", "priority-queue", "priority_queue：最大値・最小値を先に取り出す", "途中の任意の値の削除・変更はできない。top/popは空のとき使わない。")
for desc, code, cost, setup, note in [
    ("最大値を先に取り出す容器を作る", "priority_queue<int> Q;", "O(1)", "", ""),
    ("最小値を先に取り出す容器を作る", "priority_queue<int, vector<int>, greater<int>> Q;", "O(1)", "", "long longなら3か所のintをlong longにする"),
    ("値xを追加する", "Q.push(x);", "O(log N)", "priority_queue<int> Q; int x = 3;", ""),
    ("次に取り出す値を読む", "int ans = Q.top();", "O(1)", "priority_queue<int> Q; Q.push(3);", "空でないこと"),
    ("次の要素を削除する", "Q.pop();", "O(log N)", "priority_queue<int> Q; Q.push(3);", "値は返さない"),
    ("距離・頂点の組を距離の小さい順に取り出す", "priority_queue<pair<long long, int>, vector<pair<long long, int>>, greater<pair<long long, int>>> Q;", "構築 O(1)", "", "pairはfirst、同値ならsecondで比較する"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "pair", "pair / tuple：複数の値をまとめる", "比較は先頭から順に行う。pairはfirst、同値ならsecond。tupleはget<0>、get<1>…の順。")
for desc, code, setup in [
    ("2つの値をまとめる", "pair<int, int> P = {3, 7};", ""),
    ("組の1つ目・2つ目を読む", "int a = P.first;\nint b = P.second;", "pair<int, int> P = {3,7};"),
    ("3つの値をまとめる", "tuple<int, int, int> T = {2, 5, 8};", ""),
    ("tupleの添字1の項目を読む", "int x = get<1>(T);", "tuple<int,int,int> T = {2,5,8};"),
    ("組の中身を変数に分ける", "auto [a, b] = P;", "pair<int,int> P = {3,7};"),
]:
    add(g, desc, code, "O(1)", setup, "getの< >内はコンパイル時に決まる整数" if "get<" in code else "")

g = group("std", "sort", "sort / stable_sort：並べ替え", "Nは並べ替える要素数。元の並びを変更する。区間は添字l以上r未満。")
V = "vector<int> A = {3,1,4,1,5};\nint l = 1, r = 4;"
add(g, "配列全体を昇順にする", "sort(A.begin(), A.end());", "O(N log N)", V)
add(g, "配列全体を降順にする", "sort(A.begin(), A.end(), greater<int>());", "O(N log N)", V)
add(g, "添字l以上r未満を昇順にする", "sort(A.begin()+l, A.begin()+r);", "O((r−l) log(r−l))", V, "0 ≤ l ≤ r ≤ N")
add(g, "文字列を文字コード順に並べる", "sort(S.begin(), S.end());", "O(N log N)", 'string S = "cabca";')
add(g, "pairをfirst優先の昇順にする", "sort(A.begin(), A.end());", "O(N log N)", "vector<pair<int,int>> A = {{2,8},{1,9},{2,3}};")
add(g, "同じ値の元の順序を保って並べる", "stable_sort(A.begin(), A.end(), [](pair<int,int> a, pair<int,int> b){\n    return a.first < b.first;\n});", "通常 O(N log N) / 補助メモリ不足時 O(N log² N)", "vector<pair<int,int>> A = {{2,8},{1,9},{2,3}};", "同じfirst同士の順序を保つ")
add(g, "元の添字を値の降順・同値なら添字の昇順に並べる", "sort(order.begin(), order.end(), [&](int i, int j){\n    if(A.at(i) != A.at(j)){\n        return A.at(i) > A.at(j);\n    }\n    return i < j;\n});", "O(N log N)", "vector<int> A = {30,10,30};\nint N = A.size();\nvector<int> order(N);\niota(order.begin(), order.end(), 0);", "比較は同じもの同士でfalseになるようにする。<=や>=は不可")

g = group("std", "reverse", "reverse / rotate：反転・回転", "配列も文字列も同じ書き方。区間は添字l以上r未満。")
for desc, code, cost, setup, note in [
    ("配列全体の並びを反転する", "reverse(A.begin(), A.end());", "O(N)", V, ""),
    ("添字l以上r未満の並びを反転する", "reverse(A.begin()+l, A.begin()+r);", "O(r−l)", V, "0 ≤ l ≤ r ≤ N"),
    ("文字列全体の並びを反転する", "reverse(S.begin(), S.end());", "O(N)", 'string S = "abcde";', ""),
    ("文字列の添字l以上r未満を反転する", "reverse(S.begin()+l, S.begin()+r);", "O(r−l)", 'string S = "abcde"; int l = 1, r = 4;', ""),
    ("配列全体を左にk個ぶん回転する", "rotate(A.begin(), A.begin()+k, A.end());", "O(N)", "vector<int> A = {0,1,2,3,4}; int k = 2;", "0 ≤ k ≤ N。先頭k個を末尾へ移す"),
    ("配列全体を右にk個ぶん回転する", "rotate(A.begin(), A.end()-k, A.end());", "O(N)", "vector<int> A = {0,1,2,3,4}; int k = 2;", "0 ≤ k ≤ N。末尾k個を先頭へ移す"),
    ("添字l以上r未満を、添字mが先頭になるよう回転する", "rotate(A.begin()+l, A.begin()+m, A.begin()+r);", "O(r−l)", "vector<int> A = {0,1,2,3,4}; int l = 1, m = 2, r = 4;", "0 ≤ l ≤ m ≤ r ≤ N"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "fill", "fill / iota / unique / remove：一括操作・削除", "uniqueとremoveは新しい終端を返す。要素数を減らすにはeraseも必要。")
for desc, code, cost, setup, note in [
    ("全要素をxにする", "fill(A.begin(), A.end(), x);", "O(N)", V+" int x = 9;", "要素数は変えない"),
    ("添字l以上r未満をxにする", "fill(A.begin()+l, A.begin()+r, x);", "O(r−l)", V+" int x = 9;", ""),
    ("先頭から0,1,2,…を入れる", "iota(A.begin(), A.end(), 0);", "O(N)", "vector<int> A(5);", "末尾の引数が開始値"),
    ("隣接する同じ値を1個にまとめる", "A.erase(unique(A.begin(), A.end()), A.end());", "O(N)", "vector<int> A = {1,1,3,3,1};", "離れた同じ値は消えない"),
    ("配列全体から重複を取り除く", "sort(A.begin(), A.end());\nA.erase(unique(A.begin(), A.end()), A.end());", "O(N log N)", V, "元の順序は失われる"),
    ("値xの要素を全部削除する", "A.erase(remove(A.begin(), A.end(), x), A.end());", "O(N)", V+" int x = 1;", "残る要素の相対順序は保つ"),
    ("条件を満たす要素を全部削除する", "A.erase(remove_if(A.begin(), A.end(), [](int x){\n    return x < 0;\n}), A.end());", "O(N)", "vector<int> A = {3,-1,4,-2};", "trueを返した要素を削除する"),
    ("値xを全部yに置き換える", "replace(A.begin(), A.end(), x, y);", "O(N)", V+" int x = 1, y = 9;", "要素数は変わらない"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "bounds", "lower_bound / upper_bound / binary_search：二分探索", "昇順にソート済みのvectorが前提。Nは配列長。返る位置がNなら該当なし。setではメンバ関数を使う。")
V = "vector<int> A = {1,3,3,7};\nint N = A.size();\nint x = 3;"
LB = "lower_bound(A.begin(), A.end(), x) - A.begin()"
UB = "upper_bound(A.begin(), A.end(), x) - A.begin()"
for desc, code, note in [
    ("x以上の値が最初に現れる添字を求める", "int p = "+LB+";", "値そのものではなく添字"),
    ("xより大きい値が最初に現れる添字を求める", "int p = "+UB+";", "値そのものではなく添字"),
    ("x未満の要素数を求める", "int cnt = "+LB+";", ""),
    ("x以下の要素数を求める", "int cnt = "+UB+";", ""),
    ("x以上の要素数を求める", "int cnt = N - ("+LB+");", ""),
    ("xより大きい要素数を求める", "int cnt = N - ("+UB+");", ""),
    ("xと等しい要素数を求める", "int cnt = upper_bound(A.begin(), A.end(), x) - lower_bound(A.begin(), A.end(), x);", ""),
    ("xがあるか判定する", "bool exists = binary_search(A.begin(), A.end(), x);", ""),
    ("x以上で最小の値を読む", "int p = "+LB+";\nif(p < N){\n    int ans = A.at(p);\n}", "p==Nなら該当なし"),
    ("x未満で最大の値を読む", "int p = "+LB+";\nif(p > 0){\n    int ans = A.at(p-1);\n}", "p==0なら該当なし"),
    ("x以下で最大の値を読む", "int p = "+UB+";\nif(p > 0){\n    int ans = A.at(p-1);\n}", ""),
]:
    add(g, desc, code, "O(log N)", V, note)

g = group("std", "aggregate", "min / max / accumulate / count / find：集計・検索", "配列を走査する操作を質問ごとに繰り返すとO(NQ)になる。最小・最大の位置の読み取りは空の配列では使えない。")
V = "vector<int> A = {4,1,7}; int x = 4;"
for desc, code, cost, setup, note in [
    ("2つの値の小さい方を求める", "int ans = min(a, b);", "O(1)", "int a = 3, b = 5;", "2引数の型をそろえる"),
    ("2つの値の大きい方を求める", "long long ans = max(0LL, x);", "O(1)", "long long x = 5;", "xがlong longなら0LL"),
    ("複数の値の最大を求める", "int ans = max({a, b, c});", "O(個数)", "int a = 2, b = 5, c = 3;", ""),
    ("2つの変数の値を交換する", "swap(a, b);", "O(1)", "int a = 2, b = 5;", "intなどの値の場合"),
    ("配列の最小値を求める", "int ans = *min_element(A.begin(), A.end());", "O(N)", V, "空でないこと"),
    ("配列の最大値を求める", "int ans = *max_element(A.begin(), A.end());", "O(N)", V, "空でないこと"),
    ("最小値が最初に現れる添字を求める", "int p = min_element(A.begin(), A.end()) - A.begin();", "O(N)", V, ""),
    ("添字l以上r未満の最大値を求める", "int ans = *max_element(A.begin()+l, A.begin()+r);", "O(r−l)", V+" int l = 0, r = 2;", "l < r"),
    ("配列の合計をlong longで求める", "long long sum = accumulate(A.begin(), A.end(), 0LL);", "O(N)", V, "0ではなく0LLを使う"),
    ("値xの個数を数える", "int cnt = count(A.begin(), A.end(), x);", "O(N)", V, "ソート不要"),
    ("条件を満たす要素数を求める", "int cnt = count_if(A.begin(), A.end(), [](int x){\n    return x % 2 == 0;\n});", "O(N)", V, ""),
    ("値xが最初に現れる添字を求める", "auto it = find(A.begin(), A.end(), x);\nif(it != A.end()){\n    int p = it - A.begin();\n}", "O(N)", V, "見つからないとend。ソート不要"),
    ("全要素が条件を満たすか判定する", "bool ok = all_of(A.begin(), A.end(), [](int x){\n    return x >= 0;\n});", "O(N)", V, "空ならtrue"),
    ("1個以上の要素が条件を満たすか判定する", "bool ok = any_of(A.begin(), A.end(), [](int x){\n    return x >= 0;\n});", "O(N)", V, "空ならfalse"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "numeric", "gcd / lcm / abs / sqrt：数値計算", "intの積は代入先がlong longでも先にintで計算される。1LLを掛けてから計算する。")
for desc, code, cost, setup, note in [
    ("最大公約数を求める", "long long g = gcd(a, b);", "O(log min(a,b))（正整数）", "long long a = 12, b = 18;", "gcd(0,0)=0。絶対値が型に収まること"),
    ("最小公倍数を求める", "long long l = lcm(a, b);", "O(log min(a,b))（正整数）", "long long a = 12, b = 18;", "最小公倍数が型に収まること"),
    ("絶対値を求める", "long long d = abs(x);", "O(1)", "long long x = -5;", "long longの最小値の絶対値は型に収まらない"),
    ("平方根を実数で求める", "double x = sqrt(2.0);", "通常 O(1)", "", "浮動小数点の丸め誤差あり"),
    ("非負整数aを正整数bで割って切り上げる", "long long ans = a/b + (a % b != 0);", "O(1)", "long long a = 17, b = 5;", "a ≥ 0、b > 0"),
    ("余りを0以上MOD未満にそろえる", "long long r = x % MOD;\nif(r < 0){\n    r += MOD;\n}", "O(1)", "long long x = -3, MOD = 5;", "MOD > 0"),
    ("int同士の積をlong longで計算する", "long long ans = 1LL * a * b;", "O(1)", "int a = 200000, b = 200000;", "最終結果はlong long内に収まること"),
    ("型の最大値・最小値を得る", "long long hi = numeric_limits<long long>::max();\nlong long lo = numeric_limits<long long>::lowest();", "O(1)", "", "INFに最大値を使って足し算するとあふれる"),
]:
    add(g, desc, code, cost, setup, note)

g = group("std", "io", "cin / cout / bitset / next_permutation：入出力・その他", "全体コードはC++23 (GCC 15.2.0)。bits/stdc++.hはGCC系環境向け。")
add(g, "小数点以下k桁で出力する", "cout << fixed << setprecision(k) << x << endl;", "出力文字数に比例", "double x = sqrt(2.0); int k = 10;")
add(g, "大量入出力を高速化する", "ios::sync_with_stdio(false);\ncin.tie(nullptr);", "設定 O(1)", "", "mainの先頭、最初の入出力より前に置く。大量出力は'\\n'を使う")
add(g, "次の辞書順の順列に進める", "bool exists = next_permutation(A.begin(), A.end());", "O(N)", "vector<int> A = {0,1,2};", "最後の並びから呼ぶと最初の並びに戻ってfalse。全列挙は昇順からdo-while")
add(g, "整数を固定長の2進文字列にする", "string S = bitset<8>(x).to_string();", "O(B)", "unsigned long long x = 5;", "Bはbit数。ここでは8。上位の余分なbitは切り捨てる")
add(g, "固定長bit列の1の個数を数える", "int cnt = B.count();", "O(Bのbit数)", "bitset<8> B(5);")

# ACL
g = group("acl", "dsu", "dsu：グループ結合・連結判定", "Union-Find。頂点0〜N−1。辺の削除・距離計算はできない。α(N)は逆アッカーマン関数で、実用的には非常に小さい。")
for desc, code, cost, note in [
    ("N頂点を別々のグループとして作る", "atcoder::dsu D(N);", "O(N)", ""),
    ("頂点aとbのグループを結合する", "D.merge(a, b);", "ならし O(α(N))", ""),
    ("頂点aとbが同じグループか判定する", "bool same = D.same(a, b);", "ならし O(α(N))", ""),
    ("頂点aのグループの頂点数を求める", "int size = D.size(a);", "ならし O(α(N))", ""),
    ("頂点aのグループの代表頂点を求める", "int root = D.leader(a);", "ならし O(α(N))", "代表は最小頂点とは限らず、結合で変わる"),
    ("全グループの頂点一覧を得る", "vector<vector<int>> groups = D.groups();", "O(N)", ""),
]:
    add(g, desc, code, cost, "int N = 5;" if code.startswith("atcoder") else "atcoder::dsu D(5); int a = 0, b = 1; D.merge(0, 1);", note, includes="#include <atcoder/dsu>\n")

g = group("acl", "fenwick", "fenwick_tree：1点加算・区間和", "BITとも呼ぶ。0始まり、区間の右端は含まない。初期値はすべて0。sumはlong long内に収まるようにする。")
for desc, code, cost, setup, note in [
    ("長さNの配列をすべて0で作る", "atcoder::fenwick_tree<long long> F(N);", "O(N)", "int N = 5;", ""),
    ("添字pの値にxを加算する", "F.add(p, x);", "O(log N)", "atcoder::fenwick_tree<long long> F(5); int p = 2; long long x = 7;", "代入ではない"),
    ("添字l以上r未満の和を求める", "long long ans = F.sum(l, r);", "O(log N)", "atcoder::fenwick_tree<long long> F(5); int l = 1, r = 4;", "0 ≤ l ≤ r ≤ N"),
    ("添字pの値をxへ変更する", "F.add(p, x-A.at(p));\nA.at(p) = x;", "O(log N)", "vector<long long> A = {1,2,3};\natcoder::fenwick_tree<long long> F(3);\nfor(int i = 0;i < 3;i++){\n    F.add(i, A.at(i));\n}\nint p = 1; long long x = 9;", "現在値Aを別に持つ"),
]:
    add(g, desc, code, cost, setup, note, includes="#include <atcoder/fenwicktree>\n")

g = group("acl", "segtree", "segtree：1点代入・区間集計", "opは2つの結果をまとめる関数、eは混ぜても結果を変えない値。括弧の付け方で結果が変わらない演算に使う。")
for mode, operation, identity in [("最小値", "min(a, b)", "numeric_limits<long long>::max()"), ("最大値", "max(a, b)", "numeric_limits<long long>::lowest()"), ("和", "a+b", "0"), ("最大公約数", "gcd(a, b)", "0")]:
    before = f"long long op(long long a, long long b){{\n    return {operation};\n}}\nlong long e(){{\n    return {identity};\n}}\n\n"
    add(g, f"1点更新に対応する区間の{mode}を求める", "atcoder::segtree<long long, op, e> seg(A);\nseg.set(p, x);\nlong long ans = seg.prod(l, r);", "構築 O(N) / 更新・取得 O(log N)", "vector<long long> A = {5,2,8};\nint p = 1, l = 0, r = 3;\nlong long x = 7;", "setは代入。prodは添字l以上r未満。最大公約数は非負整数を前提。和は型に収まること。", before=before, includes="#include <atcoder/segtree>\n")
add(g, "添字pの現在値を読む", "long long x = seg.get(p);", "O(1)", "vector<long long> A = {5,2,8};\natcoder::segtree<long long, op, e> seg(A); int p = 1;", before="long long op(long long a, long long b){ return min(a,b); }\nlong long e(){ return LLONG_MAX; }\n", includes="#include <atcoder/segtree>\n")
add(g, "全区間の集計値を読む", "long long ans = seg.all_prod();", "O(1)", "vector<long long> A = {5,2,8};\natcoder::segtree<long long, op, e> seg(A);", before="long long op(long long a, long long b){ return min(a,b); }\nlong long e(){ return LLONG_MAX; }\n", includes="#include <atcoder/segtree>\n")

g = group("acl", "modint", "modint：余りを取りながら整数計算", "法は998244353か1000000007。大小比較には使えない。出力はval()、入力は通常の整数で受けて代入。")
before = "using mint = atcoder::modint998244353;\n\n"
for desc, code, cost, setup, note in [
    ("998244353で割った余りを管理する", "mint x = a;", "O(1)", "long long a = 123;", "法を変えるには全体コードの型の別名を変更"),
    ("余りを取りながら加減乗算する", "mint ans = a*b + c;", "O(1)", "mint a = 10, b = 3, c = 5;", ""),
    ("余りを整数として出力する", "cout << x.val() << endl;", "O(1)（桁数固定）", "mint x = 123;", ""),
    ("xのn乗の余りを求める", "mint ans = x.pow(n);", "O(log n)", "mint x = 3; long long n = 5;", "n ≥ 0"),
    ("逆元を掛ける割り算をする", "mint ans = a/b;", "O(log MOD)", "mint a = 10, b = 3;", "整数の切り捨て除算ではない。bの余りが0なら不可"),
    ("余りを管理するDP配列を作る", "vector<mint> dp(N+1, 0);", "O(N)", "int N = 5;", ""),
]:
    add(g, desc, code, cost, setup, note, before=before, includes="#include <atcoder/modint>\n")

g = group("acl", "acl-extra", "math / string：累乗・文字列処理", "各機能の詳しい条件はAtCoder Libraryの公式ドキュメントを参照。")
add(g, "xのn乗をmで割った余りを求める", "long long ans = atcoder::pow_mod(x, n, m);", "O(log n)", "long long x = 3, n = 5; int m = 7;", "n ≥ 0、1 ≤ m ≤ intの最大値", includes="#include <atcoder/math>\n")
add(g, "各位置からの接尾辞と先頭が一致する長さを求める", "vector<int> Z = atcoder::z_algorithm(S);", "O(N)", 'string S = "ababa";', "Z[i]はSの先頭とS[i..N)の共通接頭辞長", includes="#include <atcoder/string>\n")

# 定番実装。説明と全体コードのみを表示する。
g = group("algo", "prefix", "累積和・いもす法", "添字と区間は0始まり。和・加算結果はlong longに収まること。")
add(g, "更新なしの配列で、区間の和を繰り返し求める", "S.at(r) - S.at(l)", "前処理 O(N) / 質問 O(1) / メモリ O(N)", body="""
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
""", input="4 3\n3 1 4 2\n1 3\n0 4\n2 2\n", expected="5\n10\n0\n")
add(g, "二次元配列の長方形内の和を求める", "S.at(h2).at(w2)-S.at(h1).at(w2)-S.at(h2).at(w1)+S.at(h1).at(w1)", "前処理 O(HW) / 質問 O(1) / メモリ O(HW)", body="""
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
""", input="2 2 1\n1 2\n3 4\n0 1 2 2\n", expected="6\n")
add(g, "区間への加算をすべて行った後、各要素の値を求める", "D.at(l) += x; D.at(r) -= x;", "更新合計 O(Q) / 復元 O(N) / メモリ O(N)", body="""
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
""", input="5 1\n1 4 3\n", expected="0\n3\n3\n3\n0\n")

g = group("algo", "enumeration", "全探索・座標圧縮・数え上げ")
add(g, "各要素を選ぶ・選ばない全組合せで、和がKになる数を数える", "if((bit >> i) & 1LL)", "時間 O(N × 2ᴺ) / メモリ O(N)", note="空集合も含む。Nは典型的には20前後。", body="""
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
""", input="3 5\n2 3 5\n", expected="2\n")
add(g, "配列の値の全順列を列挙する", "do{ ... }while(next_permutation(A.begin(), A.end()));", "時間 O(N × N!) / メモリ O(N)", note="同じ値の並びは重複して出力しない。", body="""
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
""", input="2\n2 1\n", expected="1 2\n2 1\n")
add(g, "値の大小関係を保ったまま、0始まりの順位へ置き換える", "lower_bound(B.begin(), B.end(), A.at(i)) - B.begin()", "時間 O(N log N) / メモリ O(N)", note="値の差・距離は保たない。", body="""
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
""", input="4\n100 5 100 20\n", expected="2\n0\n2\n1\n")
add(g, "同じ値を持つ添字のペア数を求める", "num * (num-1) / 2", "時間 O(N log N) / メモリ O(値の種類数)", body="""
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
""", input="5\n2 2 2 3 3\n", expected="4\n")

g = group("algo", "answer-search", "答えの二分探索・しゃくとり法")
binary = (ROOT / "examples/binary_search.cpp").read_text(encoding="utf-8")
add(g, "x² ≥ Kとなる最小整数xを二分探索で求める", "while(ok-ng > 1)", "時間 O(log K) / メモリ O(1)", note="1 ≤ K ≤ 10¹⁸。一般の問題では判定と初期ok/ngを両方変更する。", body="")
g["items"][-1].update(full=binary, input="20\n", expected="5\n")
add(g, "非負配列で、区間和がK以下の空でない連続部分列を数える", "ans += r-l;", "時間 O(N) / メモリ O(N)", note="Aの全要素 ≥ 0、K ≥ 0。", body="""
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
""", input="3 3\n2 1 3\n", expected="4\n")

g = group("algo", "graph", "BFS・Dijkstra・トポロジカルソート")
for desc, name, cost, note, inp, exp in [
    ("無向・重みなしグラフで頂点1からの最短距離を求める", "bfs", "時間 O(N+M) / メモリ O(N+M)", "頂点番号は入力が1始まり、内部は0始まり。到達不可は−1。", "4 2\n1 2\n2 3\n", "0\n1\n2\n-1\n"),
    ("非負重みの有向グラフで頂点1からの最短距離を求める", "dijkstra", "時間 O((N+M) log(N+M)) / メモリ O(N+M)", "重み ≥ 0。有限の最短距離 < INF、距離+重みがlong long内。", "4 3\n1 2 8\n1 3 2\n3 2 1\n", "0\n3\n2\n-1\n"),
]:
    add(g, desc, name, cost, note=note, body="")
    g["items"][-1].update(full=(ROOT / f"examples/{name}.cpp").read_text(encoding="utf-8"), input=inp, expected=exp)
add(g, "壁のある盤面で、上下左右移動の最短距離を求める", "queue<pair<int,int>> Q;", "時間 O(HW) / メモリ O(HW)", note="入力はH W、開始h w、目標h w、盤面。座標0始まり、#は壁。", body="""
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
""", input="2 3 0 0 1 2\n.#.\n...\n", expected="3\n")
add(g, "有向辺の前後関係を守る順番を求める", "入次数0の頂点からqueueで取り出す", "時間 O(N+M) / メモリ O(N+M)", note="N M、M本の有向辺a b（1始まり）を入力。閉路があれば−1。", body="""
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
""", input="3 2\n1 2\n2 3\n", expected="1\n2\n3\n")

add(g, "各頂点から決まった回数だけ移動した先を求める", "jump.at(bit).at(v)", "前処理 O(N log K) / 質問 O(Q log K) / メモリ O(N log K)", note="⚠︎ 移動回数Kは0以上10¹⁸以下。各頂点の移動先が1つに決まるとき限定", body="""
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
""", input="4 3\n2 3 4 2\n1 0\n1 3\n4 10\n", expected="1\n4\n2\n")

add(g, "有向グラフを、互いに行き来できる頂点ごとに分ける", "component.at(v)", "時間 O(N+M) / メモリ O(N+M)", note="⚠︎ 有向グラフ限定。グループ番号に意味はなく、実行ごとに順序が変わることがある。", body="""
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
""", input="5 6\n1 2\n2 1\n2 3\n3 4\n4 3\n4 5\n", expected="3\n1 1 2 2 3\n")

g = group("algo", "dp", "DP：階段・LIS・ナップサック")
add(g, "1段・2段ずつN段上る方法の数を余りで求める", "dp.at(i) = dp.at(i+1)+dp.at(i+2);", "時間 O(N) / メモリ O(N)", body="")
g["items"][-1].update(full=(ROOT / "examples/acl_modint.cpp").read_text(encoding="utf-8"), input="5\n", expected="8\n", note="法998244353。ACLが必要。")
for fast in [False, True]:
    body = """
int N;
cin >> N;
vector<int> A(N);
for(int i = 0;i < N;i++){
    cin >> A.at(i);
}
"""
    body += """
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
""" if fast else """
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
"""
    add(g, "狭義単調増加部分列の最大長を求める"+("（高速版）" if fast else "（二重ループ版）"), "LIS", "時間 "+("O(N log N)" if fast else "O(N²)")+" / メモリ O(N)", note="同じ値を連続して選ばない。高速版のtail全体は実際の部分列とは限らない。", body=body, input="4\n3 1 2 5\n", expected="3\n")
add(g, "各品物を1個まで選び、重さW以下で価値の和を最大化する", "dp.at(w) = max(dp.at(w), dp.at(w-weight)+value);", "時間 O(NW) / メモリ O(W)", note="N W、各品物の重さ・価値を入力。重さは正整数。価値の合計はlong long内。", body="""
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
""", input="3 5\n2 3\n3 4\n4 5\n", expected="7\n")

g = group("algo", "number", "約数・素数・素因数分解")
add(g, "正整数Nの約数を昇順に列挙する", "for(long long x = 1;x <= N/x;x++)", "時間 O(√N + D log D) / メモリ O(D)", note="Dは約数の個数。N ≥ 1。", body="""
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
""", input="12\n", expected="1\n2\n3\n4\n6\n12\n")
add(g, "整数Nが素数か判定する", "is_prime(N)", "時間 O(√N) / 追加メモリ O(1)", before="""bool is_prime(long long N){
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

""", body="long long N;\ncin >> N;\ncout << (is_prime(N) ? \"Yes\" : \"No\") << endl;", input="97\n", expected="Yes\n")
add(g, "N以下の整数が素数かをまとめて求める", "エラトステネスの篩", "時間 O(N log log N) / メモリ O(N)", note="N ≥ 0。vector<char>の0/1で管理する。", body="""
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
""", input="10\n", expected="2\n3\n5\n7\n")
add(g, "正整数Nを素因数と指数に分解する", "while(N % x == 0)", "時間 O(√N) / メモリ O(log N)", note="N ≥ 1。N自体を途中で変更する。", body="""
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
""", input="360\n", expected="2 3\n3 2\n5 1\n")


g = group("algo", 'dfs', '深さ優先探索（DFS）')
add(g, '開始地点から、行ける頂点を順番に調べる', 'dfs', '時間 O(N+M) / メモリ O(N+M)', body='// N M、M本の無向辺（頂点1始まり）、開始頂点。訪問順を出力。\nint N, M;\ncin >> N >> M;\nvector<vector<int>> G(N);\nfor(int i = 0;i < M;i++){\n    int a, b;\n    cin >> a >> b;\n    a--; b--;\n    G.at(a).push_back(b);\n    G.at(b).push_back(a);\n}\nint start;\ncin >> start;\nstart--;\nvector<char> seen(N, false);\nvector<int> st = {start};\nwhile(!st.empty()){\n    int v = st.back();\n    st.pop_back();\n    if(seen.at(v)){continue;}\n    seen.at(v) = true;\n    cout << v+1 << endl;\n    for(int i = (int)G.at(v).size()-1;i >= 0;i--){\n        int to = G.at(v).at(i);\n        if(!seen.at(to)){\n            st.push_back(to);\n        }\n    }\n}\n')
g = group("algo", 'connected-components', '連結成分分解（無向グラフ）')
add(g, '道でつながっている頂点ごとにグループ分けする', 'connected-components', '時間 O(N+M) / メモリ O(N+M)', body="// N M、M本の無向辺（頂点1始まり）。成分数と各頂点のグループ番号を出力。\nint N, M;\ncin >> N >> M;\nvector<vector<int>> G(N);\nfor(int i = 0;i < M;i++){\n    int a, b;\n    cin >> a >> b;\n    a--; b--;\n    G.at(a).push_back(b);\n    G.at(b).push_back(a);\n}\nvector<int> component(N, -1);\nint count = 0;\nfor(int s = 0;s < N;s++){\n    if(component.at(s) != -1){continue;}\n    vector<int> st = {s};\n    component.at(s) = count;\n    while(!st.empty()){\n        int v = st.back();\n        st.pop_back();\n        for(int i = 0;i < (int)G.at(v).size();i++){\n            int to = G.at(v).at(i);\n            if(component.at(to) == -1){\n                component.at(to) = count;\n                st.push_back(to);\n            }\n        }\n    }\n    count++;\n}\ncout << count << endl;\nfor(int v = 0;v < N;v++){\n    cout << component.at(v)+1 << (v+1 == N ? '\\n' : ' ');\n}\n")
g = group("algo", 'bipartite', '二部グラフ判定')
add(g, 'つながっている頂点同士を違う色にして、2色で塗り分けられるか調べる', 'bipartite', '時間 O(N+M) / メモリ O(N+M)', body='// N M、M本の無向辺（頂点1始まり）。塗り分け可能ならYes。\nint N, M;\ncin >> N >> M;\nvector<vector<int>> G(N);\nfor(int i = 0;i < M;i++){\n    int a, b;\n    cin >> a >> b;\n    a--; b--;\n    G.at(a).push_back(b);\n    G.at(b).push_back(a);\n}\nvector<int> color(N, -1);\nbool ok = true;\nfor(int s = 0;s < N;s++){\n    if(color.at(s) != -1){continue;}\n    queue<int> Q;\n    color.at(s) = 0;\n    Q.push(s);\n    while(!Q.empty()){\n        int v = Q.front();\n        Q.pop();\n        for(int i = 0;i < (int)G.at(v).size();i++){\n            int to = G.at(v).at(i);\n            if(color.at(to) == -1){\n                color.at(to) = 1-color.at(v);\n                Q.push(to);\n            }\n            else if(color.at(to) == color.at(v)){\n                ok = false;\n            }\n        }\n    }\n}\ncout << (ok ? "Yes" : "No") << endl;\n')
g = group("algo", 'floyd-warshall', 'ワーシャルフロイド法')
add(g, 'すべての頂点の組合せについて、最短距離をまとめて求める', 'floyd-warshall', '時間 O(N³+M) / メモリ O(N²)', body="// N M、M本の有向辺 a b cost（頂点1始まり）。距離行列を出力、到達不可は-1。有限の距離はINF未満。\nint N, M;\ncin >> N >> M;\nconst long long INF = 4000000000000000000LL;\nvector<vector<long long>> dist(N, vector<long long>(N, INF));\nfor(int v = 0;v < N;v++){dist.at(v).at(v) = 0;}\nfor(int i = 0;i < M;i++){\n    int a, b;\n    long long cost;\n    cin >> a >> b >> cost;\n    a--; b--;\n    dist.at(a).at(b) = min(dist.at(a).at(b), cost);\n}\nfor(int k = 0;k < N;k++){\n    for(int i = 0;i < N;i++){\n        for(int j = 0;j < N;j++){\n            if(dist.at(i).at(k) == INF || dist.at(k).at(j) == INF){continue;}\n            dist.at(i).at(j) = min(dist.at(i).at(j), dist.at(i).at(k)+dist.at(k).at(j));\n        }\n    }\n}\nfor(int i = 0;i < N;i++){\n    for(int j = 0;j < N;j++){\n        cout << (dist.at(i).at(j) == INF ? -1 : dist.at(i).at(j));\n        cout << (j+1 == N ? '\\n' : ' ');\n    }\n}\n")
g = group("algo", 'run-length', 'ランレングス圧縮')
add(g, '同じ文字が連続する部分を、文字と個数にまとめる', 'run-length', '時間 O(N) / メモリ O(N)', body='// 空白を含まない文字列S。各連続部分の文字と個数を出力。\nstring S;\ncin >> S;\nvector<pair<char,int>> runs;\nfor(int i = 0;i < (int)S.size();i++){\n    if(runs.empty() || runs.back().first != S.at(i)){\n        runs.push_back({S.at(i), 1});\n    }\n    else{\n        runs.back().second++;\n    }\n}\nfor(int i = 0;i < (int)runs.size();i++){\n    cout << runs.at(i).first << " " << runs.at(i).second << endl;\n}\n')

def table(headers, rows):
    return '<div class="table-wrap"><table><thead><tr>' + ''.join('<th>'+h+'</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows) + '</tbody></table></div>'


def limits_sections():
    result = []
    result.append(dict(key="time-guide", title="計算量：制約から見る候補", content=table(["入力規模", "候補になる計算量"], [
        ["N ≲ 10", "O(N × N!)"], ["N ≲ 20", "O(N × 2ᴺ)"], ["N ≲ 3×10³", "O(N²)"],
        ["N ≲ 2×10⁵", "O(N log N)、O(N)"], ["値の範囲が10⁹〜10¹⁸", "二分探索・数式など。値を1ずつ列挙しない"]]) + '<p class="note">制限時間・処理内容・定数倍で変わる目安。秒数の保証ではない。</p>'))
    def sci(x):
        if x == 0: return "0"
        n = int(math.floor(math.log10(x)))
        a = x / 10**n
        sup = str(n).translate(str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))
        return ("" if abs(a-1) < 0.00001 else f"{a:.2g}×") + "10"+sup
    rows = []
    for n in [10**2, 10**3, 3*10**3, 10**4, 2*10**5, 10**6]:
        rows.append([sci(n), sci(n*math.log2(n)), sci(n*n), sci(n**3)])
    result.append(dict(key="time-count", title="計算量：式にNを入れた規模", content=table(["N / O(N)", "N log₂N", "N²", "N³"], rows) + table(["N", "2ᴺ", "N × 2ᴺ", "N!"], [[str(n), sci(2**n), sci(n*2**n), sci(math.factorial(n))] for n in [10, 15, 20, 25, 30]]) + '<p class="note">実際のCPU命令数ではなく、計算量の式の値。文字列コピーやmap操作などは単純な加算より重い。</p>'))
    result.append(dict(key="type-memory", title="型と配列のメモリ", content=table(["型", "1要素の目安", "10⁵要素", "10⁶要素", "10⁷要素"], [
        ["char", "0.000001 MB", "0.1 MB", "1 MB", "10 MB"], ["int", "0.000004 MB", "0.4 MB", "4 MB", "40 MB"],
        ["long long / double", "0.000008 MB", "0.8 MB", "8 MB", "80 MB"], ["pair&lt;int,int&gt;", "通常0.000008 MB", "約0.8 MB", "約8 MB", "約80 MB"]])))
    result.append(dict(key="matrix-memory", title="二次元配列のメモリ", content=table(["H × W", "要素数", "int", "long long / double"], [
        ["10² × 10²", "10⁴", "0.04 MB", "0.08 MB"], ["10³ × 10³", "10⁶", "4 MB", "8 MB"],
        ["2×10³ × 2×10³", "4×10⁶", "16 MB", "32 MB"], ["3×10³ × 3×10³", "9×10⁶", "36 MB", "72 MB"],
        ["5×10³ × 5×10³", "2.5×10⁷", "100 MB", "200 MB"], ["10⁴ × 10⁴", "10⁸", "400 MB", "800 MB"]])))
    result.append(dict(key="memory-extra", title="容器・グラフ・コピーの注意", content=table(["対象", "容量の見積もり"], [
        ["vector&lt;T&gt;", "確保済みcapacity × sizeof(T) ÷ 10⁶ MB + 管理領域。sizeだけでは正確に見積もれない"],
        ["vector&lt;vector&lt;T&gt;&gt;", "各行のcapacity × sizeof(T) ÷ 10⁶ MB + H個のvector管理領域 + 各確保の管理領域"],
        ["map / set / multiset", "ノードごとの参照などで、値本体より大きくなる。要素数 × sizeof(値) ÷ 10⁶ MBだけでは不足"],
        ["unordered_map / unordered_set", "要素ノードに加え、バケット配列も必要"],
        ["無向グラフの隣接リスト", "頂点数N、辺数Mの場合、intの行き先を通常2M個持つ。本体約M × 0.000008 MB + N個のvectorなど"],
        ["vector&lt;bool&gt;", "一般にbit圧縮。通常のbool配列とは扱いが異なる。分かりやすさ重視ならvector&lt;char&gt;"],
        ["関数の引数", "vector&lt;int&gt; Aはコピー。const vector&lt;int&gt;&amp; Aなら読むだけで参照"],
        ["再帰DFS", "呼び出しごとのスタックも消費。深いグラフではstackなどの反復実装を検討"]])))
    return result


# 表示するアルゴリズムは1機能ずつ独立させ、明示した読みで並べる。
# 元の項目IDはコードや検証データの対応を保つため変更しない。
ALGORITHM_SECTIONS = {
    'dfs-1': ('dfs', '深さ優先探索（DFS）', 'ふかさゆうせんたんさく'),
    'connected-components-1': ('connected-components', '連結成分分解（無向グラフ）', 'れんけつせいぶんぶんかいむこうぐらふ'),
    'bipartite-1': ('bipartite', '二部グラフ判定', 'にぶぐらふはんてい'),
    'floyd-warshall-1': ('floyd-warshall', 'ワーシャルフロイド法', 'わーしゃるふろいどほう'),
    'run-length-1': ('run-length', 'ランレングス圧縮', 'らんれんぐすあっしゅく'),

    "prefix-1": ("prefix-sum", "累積和", "るいせきわ"),
    "prefix-2": ("prefix-sum-2d", "二次元累積和", "にじげんるいせきわ"),
    "prefix-3": ("imos", "いもす法", "いもすほう"),
    "enumeration-1": ("bit-enumeration", "ビット全探索", "びっとぜんたんさく"),
    "enumeration-2": ("permutation-enumeration", "順列全探索", "じゅんれつぜんたんさく"),
    "enumeration-3": ("coordinate-compression", "座標圧縮", "ざひょうあっしゅく"),
    "enumeration-4": ("equal-pair-count", "ペア数の数え上げ（同じ値）", "ぺあすうのかぞえあげおなじあたい"),
    "answer-search-1": ("answer-binary-search", "答えに対する二分探索", "こたえにたいするにぶんたんさく"),
    "answer-search-2": ("two-pointers", "しゃくとり法", "しゃくとりほう"),
    "graph-1": ("bfs", "幅優先探索（BFS）", "はばゆうせんたんさく"),
    "graph-2": ("dijkstra", "ダイクストラ法（Dijkstra）", "だいくすとらほう"),
    "graph-3": ("grid-bfs", "グリッドBFS", "ぐりっどびーえふえす"),
    "graph-4": ("topological-sort", "トポロジカルソート", "とぽろじかるそーと"),
    "graph-5": ("doubling", "ダブリング", "だぶりんぐ"),
    "graph-6": ("scc", "強連結成分分解（SCC）", "きょうれんけつせいぶんぶんかい"),
    "dp-1": ("stair-dp", "動的計画法（階段）", "どうてきけいかくほうかいだん"),
    "dp-2": ("lis-quadratic", "最長増加部分列（二重ループ）", "さいちょうぞうかぶぶんれつにじゅうるーぷ"),
    "dp-3": ("lis-binary-search", "最長増加部分列（二分探索）", "さいちょうぞうかぶぶんれつにぶんたんさく"),
    "dp-4": ("knapsack", "動的計画法（ナップザック）", "どうてきけいかくほうなっぷざっく"),
    "number-1": ("divisors", "約数列挙", "やくすうれっきょ"),
    "number-2": ("primality-trial", "素数判定（試し割り）", "そすうはんていためしわり"),
    "number-3": ("sieve", "エラトステネスの篩", "えらとすてねすのふるい"),
    "number-4": ("prime-factorization", "素因数分解", "そいんすうぶんかい"),
}

# 各実装を使うときに確認する条件を、入力に即した短い言葉で示す。
ALGORITHM_NOTES = {
    'dfs-1': '',
    'connected-components-1': '',
    'bipartite-1': '',
    'floyd-warshall-1': '⚠︎ この実装は、各ルートを通るコストが0以上のとき限定',
    'run-length-1': '',

    "prefix-1": "⚠︎ 配列の値を途中で書き換えないとき限定",
    "prefix-2": "⚠︎ 盤面の値を途中で書き換えないとき限定",
    "prefix-3": "",
    "enumeration-1": "⚠︎ 何も選ばない場合も数える。Nは20前後までが目安。",
    "enumeration-2": "⚠︎ 同じ値を入れ替えただけの並びは、別の並びとして数えない",
    "enumeration-3": "⚠︎ 圧縮後の番号の差は、元の値の差にはならない",
    "enumeration-4": "",
    "answer-search-1": "⚠︎ ある値以上なら必ず条件を満たす問題限定",
    "answer-search-2": "⚠︎ 配列の値がすべて0以上のとき限定",
    "graph-1": "⚠︎ すべてのルートを同じ1回の移動として数えられるとき限定",
    "graph-2": "⚠︎ 各ルートを通るコストがすべて0以上のとき限定",
    "graph-3": "",
    "graph-4": "",
    "graph-5": "⚠︎ 移動回数Kは0以上10¹⁸以下。各頂点の移動先が1つに決まるとき限定",
    "graph-6": "⚠︎ 有向グラフ限定。グループ番号に意味はなく、実行ごとに順序が変わることがある。",
    "dp-1": "⚠︎ 余りは998244353で計算する。AtCoder Libraryが必要。",
    "dp-2": "⚠︎ 同じ値を続けて選ぶことはできない",
    "dp-3": "⚠︎ 同じ値を続けて選ぶことはできない。tailの中身は、実際に選べる並びとは限らない。",
    "dp-4": "⚠︎ 重さは0以上の整数限定",
    "number-1": "",
    "number-2": "",
    "number-3": "",
    "number-4": "⚠︎ 処理後はNの値が変わる。元の値も使うなら先にコピー。",
}


def gojuon_key(reading):
    # 濁音・半濁音と小書き文字を基本の仮名にそろえて50音順にする。
    large = str.maketrans("ぁぃぅぇぉっゃゅょゎ", "あいうえおつやゆよわ")
    plain = "".join(c for c in unicodedata.normalize("NFD", reading) if not unicodedata.combining(c))
    return plain.translate(large), reading


def display_groups():
    ordinary = [g for g in GROUPS if g["page"] != "algo"]
    algorithms = []
    found = set()
    for g in GROUPS:
        if g["page"] != "algo":
            continue
        for item in g["items"]:
            key, title, reading = ALGORITHM_SECTIONS[item["id"]]
            found.add(item["id"])
            total_cost = {
                "prefix-1": "時間 O(N+Q) / メモリ O(N)",
                "prefix-2": "時間 O(HW+Q) / メモリ O(HW)",
                "prefix-3": "時間 O(N+Q) / メモリ O(N)",
            }.get(item["id"], item["cost"].replace("追加メモリ", "メモリ"))
            time, memory = total_cost.removeprefix("時間 ").split(" / メモリ ")
            item = dict(item, cost=total_cost, time=time, memory=memory,
                        note=ALGORITHM_NOTES[item["id"]])
            if item["id"] == "number-1":
                item["cost_definition"] = "Dは約数の個数"
            if item["id"] == "graph-2":
                item["desc"] = "一方通行のルートで、頂点1から各頂点までの最小の移動コストを求める"
            elif item["id"] == "answer-search-2":
                item["desc"] = "区間の合計がK以下になる、空でない連続部分の個数を数える"
            algorithms.append(dict(page="algo", key=key, title=title, reading=reading,
                                   note="", items=[item]))
    assert found == set(ALGORITHM_SECTIONS), "アルゴリズム名と機能の対応を確認してください"
    return ordinary + sorted(algorithms, key=lambda g: gojuon_key(g["reading"]))


PAGES = {
    "std": dict(title="標準ライブラリ", subtitle="容器と操作関数を、名前から引く。", file="standard-library.md"),
    "acl": dict(title="AtCoder Library", subtitle="グループ・区間集計・余りの計算。", file="atcoder-library.md"),
    "algo": dict(title="アルゴリズム", subtitle="名前と機能を1項目ずつ、読みの50音順で掲載。", file="algorithms.md"),
    "limits": dict(title="計算量・メモリ", subtitle="制約と必要な容量を確認する。", file="complexity-memory.md"),
    "notes": dict(title="更新履歴・制作者メモ", subtitle="公開した更新と制作者メモ。", file="site-notes.md"),
}


def generate():
    groups = [g for g in display_groups() if g["key"] not in HIDDEN_GROUPS]
    for g in groups:
        for item in g["items"]:
            if "// Reference:" not in item["full"]:
                item["full"] = "// Reference: " + PUBLIC + "\n" + item["full"]
        if g["key"] == "reverse":
            g["keywords"] = "リバース 逆順 逆転 部分反転 部分リバース 回転"
        elif g["key"] == "doubling":
            g["keywords"] = "doubling 2乗前計算 関数合成 K回移動"
        elif g["key"] == "scc":
            g["keywords"] = "強連結成分 strongly connected components Kosaraju"
    enrich(groups)
    limits = limits_sections()
    limits.insert(2, dict(key="memory-calculator", title="メモリ計算機", tool="memory", content="<p>コンテナを選択してメモリ容量を計算する。配列（vector）は一次元／二次元を切り替えられる。set・multiset・map・unordered_set・unordered_mapにも対応し、管理領域込みの推定容量を選択式のメモリ制限と比較する。</p>"))
    for section in limits:
        if section["key"] == "time-count":
            section.update(title="計算量計算機", tool="time")
    notes = json.loads((ROOT / "site-notes.json").read_text(encoding="utf-8"))
    local_notes_path = ROOT / "site-notes.local.json"
    local_notes = json.loads(local_notes_path.read_text(encoding="utf-8")) if local_notes_path.exists() else {"memos": []}
    public_notes = [dict(note, kind="updates") for note in notes["updates"] if note["published"]]
    public_notes += [dict(note, kind="memos") for note in local_notes["memos"] if note["published"]]
    payload = dict(pages=PAGES, groups=groups, limits=limits, notes=public_notes, source=PUBLIC)
    (ROOT / "reference-data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    template = (ROOT / "page-template.html").read_text(encoding="utf-8")
    packed = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    (ROOT / "index.html").write_text(template.replace("__REFERENCE_DATA__", packed), encoding="utf-8")
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    for page, info in PAGES.items():
        lines = ["# "+info["title"], "", info["subtitle"], "", "[入口へ](../README.md)", ""]
        lines += ["使用言語：**C++23 (GCC 15.2.0)**。ローカルのコンパイル設定は `-std=gnu++23`。", ""]
        if page == "limits":
            for section in limits:
                lines += ["## "+section["title"], "", section["content"], ""]
        else:
            if page == "std":
                lines += ["**容器**：vector・string・set・map・queue・stack・deque・priority_queue・pair・tuple", "", "**操作関数**：sort・reverse・rotate・fill・unique・二分探索・集計・数値計算・入出力", ""]
            if page == "acl":
                lines += ["**ACLのヘッダが必要です。** ローカルでは `atcoder` フォルダの親を `-I` に指定します。", "", "[公式ドキュメント](https://atcoder.github.io/ac-library/production/document_ja/index.html)", ""]
            for g in groups:
                if g["page"] != page: continue
                lines += ["## "+g["title"], ""]
                if g["note"] and page != "algo": lines += [g["note"], ""]
                for item in g["items"]:
                    desc = item["desc"]
                    if page == "algo":
                        definition = "（"+item["cost_definition"]+"）" if item.get("cost_definition") else ""
                        lines += ["**目的** : "+desc, "", "計算量："+item["time"]+"　メモリ："+item["memory"]+definition, ""]
                        for note in [g["note"], item["note"]]:
                            if note: lines += [note, ""]
                        lines += ["```cpp", item["full"].rstrip(), "```", ""]
                        continue
                    lines += ["### "+desc, "", "計算量："+item["cost"]+" / 追加メモリ："+item["memory"], "", item["definitions"], ""]
                    if page != "algo": lines += ["```cpp", item["code"], "```", ""]
                    if item["note"]: lines += [item["note"], ""]
                    if item.get("example"): lines += ["```text", item["example"], "```", ""]
                    lines += ["```cpp", item["full"].rstrip(), "```", ""]
        (docs / info["file"]).write_text("\n".join(lines), encoding="utf-8")
    (docs / "site-notes.md").write_text(
        "# 更新履歴・制作者メモ\n\n"
        "[入口へ](../README.md)\n\n"
        "更新履歴と公開済みの記録は `site-notes.json`、制作者用の下書きはローカル専用の `site-notes.local.json` で管理します。\n"
        "公開対象は `published: true` の項目だけです。ローカル下書きファイルは公開リポジトリへアップロードしないでください。\n",
        encoding="utf-8",
    )
    print(f"Generated: {len(groups)} sections, {sum(len(g['items']) for g in groups)} complete examples")


if __name__ == "__main__":
    generate()
