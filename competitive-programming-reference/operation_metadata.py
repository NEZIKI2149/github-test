"""標準ライブラリ・ACLの操作単位の説明。アルゴリズムの情報とは独立。"""
import re

MEMORY = {
    "vector-1": "O(N)", "vector-2": "O(HW + H)", "vector-9": "再確保時 O(N)",
    "vector-11": "再確保時 O(N)", "vector-14": "再確保時 O(N)",
    "vector-15": "O(N)", "vector-16": "再確保時 O(N)", "vector-18": "O(N)",
    "string-1": "O(N)", "string-6": "再確保時 O(N)", "string-7": "再確保時 O(N + Tの長さ)",
    "string-10": "O(K)", "string-11": "O(N−pos)", "string-16": "再確保時 O(N + Tの長さ)",
    "string-18": "再確保時 O(N + Tの長さ)", "string-24": "O(桁数)",
    "string-25": "O(読み取る文字数)", "string-26": "O(読む文字数)",
    "sort-1": "O(log N)", "sort-2": "O(log N)", "sort-3": "O(log K)",
    "sort-4": "O(log N)", "sort-5": "O(log N)", "sort-6": "O(N)", "sort-7": "O(N)",
    "fill-5": "O(log N)", "modint-6": "O(N)", "acl-extra-2": "O(N)",
    "priority-queue-3": "再確保時 O(N)", "io-1": "出力バッファは実装依存", "io-4": "O(B)",
}
NOTES = {
    "vector-3": "0以上、要素数未満の添字を指定する", "vector-4": "0以上、要素数未満の添字を指定する",
    "vector-7": "", "vector-10": "配列が空のときは使えない。取り出した値は返さない",
    "vector-11": "挿入位置は0以上、要素数以下。挿入位置以降の添字が後ろにずれる",
    "vector-12": "削除位置は0以上、要素数未満。削除位置より後ろの添字が前にずれる",
    "vector-13": "0 ≤ l ≤ r ≤ 要素数。削除した区間より後ろの添字が前にずれる",
    "vector-18": "", "string-2": "0以上、文字数未満の添字を指定する",
    "string-3": "0以上、文字数未満の添字を指定する",
    "string-10": "第2引数は終点ではなく文字数。posは0以上、文字数以下。残りがk文字未満なら末尾まで",
    "string-13": "見つからなければstring::nposになる",
    "string-20": "文字が'0'〜'9'のとき限定", "string-21": "英小文字のとき限定",
    "set-4": "", "set-8": "", "set-12": "該当する値がなければendになる。endの中身は読めない",
    "set-13": "該当する値がなければendになる。endの中身は読めない",
    "map-6": "", "map-9": "", "priority-queue-5": "容器が空のときは使えない。取り出した値は返さない",
    "fill-1": "", "fill-8": "", "fill-6": "", "fill-7": "",
    "fill-4": "隣り合う重複だけが対象。掲載コードはeraseも行うので、要素数も減る",
    "fill-5": "並べ替えるので元の順序は失われる",
    "queue-16": "0以上、要素数未満の添字を指定する",
    "modint-3": "", "modint-5": "普通の整数の割り算とは異なる。bを法で割った余りが0のときは使えない",
}
EXAMPLES = {
    "vector-11": "i = 1、x = 9\n実行前：[3, 1, 4]\n実行後：[3, 9, 1, 4]",
    "vector-12": "i = 1\n実行前：[3, 1, 4]\n実行後：[3, 4]",
    "vector-13": "l = 1、r = 3\n実行前：[3, 1, 4, 2, 5]\n実行後：[3, 2, 5]",
    "reverse-2": "l = 1、r = 4\n実行前：[3, 1, 4, 2, 5]\n実行後：[3, 2, 4, 1, 5]",
    "reverse-4": 'l = 1、r = 4\n実行前："abcde"\n実行後："adcbe"',
    "reverse-5": "k = 2\n実行前：[1, 2, 3, 4, 5]\n実行後：[3, 4, 5, 1, 2]",
    "reverse-6": "k = 2\n実行前：[1, 2, 3, 4, 5]\n実行後：[4, 5, 1, 2, 3]",
    "reverse-7": "l = 1、m = 3、r = 5\n実行前：[0, 1, 2, 3, 4, 5]\n実行後：[0, 3, 4, 1, 2, 5]",
    "string-10": 'pos = 1、k = 3\n元の文字列："abcde"\n取り出す文字列："bcd"（元の文字列は変わらない）',
    "string-17": 'pos = 1、k = 2\n実行前："abcde"\n実行後："ade"',
    "fill-4": "実行前：[1, 1, 2, 1, 1]\nuniqueだけ：[1, 2, 1, ?, ?]（要素数は5のまま）\n掲載コード（eraseも実行）：[1, 2, 1]\n? の位置の値は使わない",
    "fill-5": "実行前：[3, 1, 3, 2, 1]\n実行後：[1, 2, 3]",
    "bounds-1": "A = [1, 3, 3, 7]、x = 3\n結果：1（最初の3の添字）",
    "bounds-2": "A = [1, 3, 3, 7]、x = 3\n結果：3（7の添字）",
}
ALIASES = {
    "reverse": "リバース 逆順 逆転 反転 部分リバース 部分反転",
    "erase": "消す 削除 消去", "count": "個数 数える カウント", "sort": "ソート 並べ替え 並び替え",
    "push": "追加 入れる", "pop": "削除 取り出す", "substr": "部分文字列 切り出す 取り出す",
    "find": "探す 検索 存在", "unique": "重複 ダブり 消す", "lower_bound": "二分探索 ロウワーバウンド",
    "upper_bound": "二分探索 アッパーバウンド", "accumulate": "合計 和 足す", "swap": "交換 入れ替え",
    "rotate": "回転 ローテート ずらす", "fill": "埋める 初期化", "pow": "べき乗 累乗 冪乗",
}

def enrich(groups):
    for g in groups:
        if g['page'] == 'algo':
            continue
        for i in g['items']:
            key, code = i['id'], i['code']
            i['memory'] = MEMORY.get(key, 'O(1)')
            if g['key'] == 'queue' and any(x in code for x in ['.push(', '.push_front(', '.push_back(']):
                i['memory'] = '通常 O(1) / 管理領域の拡張時 O(N)'
            cost = i['cost']
            if 'r−l' in cost:
                cost = cost.replace('(r−l)', 'K').replace('r−l', 'K').replace('logK', 'log K')
            if key == 'string-10': cost = 'O(K)'
            if key in {'map-10','map-11'}: cost = 'O(1)'
            i['cost'] = cost
            definitions = []
            combined = cost + i['memory']
            if re.search(r'\bN\b', combined):
                meaning = '文字列の文字数' if g['key'] == 'string' or key == 'sort-4' or key == 'reverse-3' or key == 'acl-extra-2' else '操作前の要素数'
                if key in {'vector-1','vector-14','vector-15','vector-16','string-1','modint-6'}: meaning = '指定した要素数'
                if key == 'vector-14' or key == 'vector-16': meaning += '（変更前の要素数は別）'
                definitions.append('N：'+meaning)
            if 'K' in combined:
                definitions.append('K：'+('キーの種類数' if g['key']=='map' else '同じ値の個数' if g['key']=='set' else '取り出す文字数' if key=='string-10' else '操作する区間の要素数'))
            if 'H' in combined: definitions += ['H：行数、W：列数']
            if 'B' in combined: definitions += ['B：bit数']
            if 'MOD' in combined: definitions += ['MOD：余りを求めるときの法']
            if key == 'modint-4': definitions += ['n：指数']
            if key == 'acl-extra-1': definitions += ['n：指数']
            if 'pos' in combined: definitions += ['pos：取り出しを始める添字']
            i['definitions'] = ' / '.join(definitions)
            note = NOTES.get(key, i['note'])
            note = note.replace('削除する場合は空でないこと','容器が空のときは使えない').replace('空でないこと', '容器が空のときは使えない')
            note = note.replace('0 ≤ pos ≤ N', 'posは0以上、文字数以下').replace('0 ≤ l ≤ r ≤ N','0 ≤ l ≤ r ≤ 要素数')
            if g['key']=='bounds': note = '配列を昇順に並べてあるとき限定。'+note
            if g['key']=='aggregate' and key in {'aggregate-7','aggregate-8'}: note = '対象の区間が空のときは使えない。'+note
            if key=='sort-1' or key=='sort-2' or key=='sort-3' or key=='sort-4' or key=='sort-5' or key=='fill-5':
                note += ' 追加メモリはGCCの一般的な実装の目安。'
            if key in {'vector-9','string-6','priority-queue-3'}: note += ' 容量が足りなくなると、メモリの確保し直しが発生する。'
            if 'ならし' in cost: note += ' 「ならし」は、操作を何度も繰り返したときの1回あたりの目安。'
            i['note'] = ('⚠︎ '+note.strip().rstrip('。！!')) if note.strip() else ''
            i['example'] = EXAMPLES.get(key, '')
            words = [g.get('keywords','')]
            for api, aliases in ALIASES.items():
                if api in code: words.append(aliases)
            i['keywords'] = ' '.join(words)
