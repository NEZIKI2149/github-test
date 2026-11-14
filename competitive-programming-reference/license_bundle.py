"""Keep third-party notices in each standalone HTML, including offline copies."""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILES = (
    'syntax-NOTICES.txt',
    'vendor/clang-format/LICENSE',
    'vendor/clang-format/LLVM-LICENSE.txt',
    'vendor/clang-format/EMSCRIPTEN-LICENSE.txt',
)
START = '<!-- third-party-licenses:start -->'
END = '<!-- third-party-licenses:end -->'

def with_bundled_licenses(page):
    parts = []
    for name in FILES:
        text = (ROOT / name).read_text(encoding='utf-8').replace('\r\n', '\n')
        parts.append(name + '\n' + '=' * 60 + '\n' + text)
    text = '\n\n'.join(parts)
    block = (START + '\n<details id="third-party-licenses" '
             'style="max-width:1560px;margin:24px auto;padding:0 24px 24px;font-size:12px">'
             '<summary style="cursor:pointer">使用部品のライセンス</summary>'
             '<p>このHTMLに同梱した第三者部品の出典・著作権表示・ライセンス本文です。'
             'オフラインでも確認できます。</p>'
             '<pre style="white-space:pre-wrap;overflow-wrap:anywhere;font-size:11px;line-height:1.6">'
             + html.escape(text, quote=True) + '</pre></details>\n' + END)
    pattern = re.escape(START) + r'.*?' + re.escape(END)
    if START in page:
        return re.sub(pattern, lambda _: block, page, count=1, flags=re.S)
    if '</body>' not in page:
        raise ValueError('Missing body for bundled notices')
    return page.replace('</body>', block + '\n</body>', 1)
