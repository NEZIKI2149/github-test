"""Generate a CSP for the reviewed inline scripts; no runtime dependencies."""
import base64
import hashlib
import html
import re


def with_security_policy(page, *, wasm=False):
    # HTML parsers normalize CRLF before checking inline-script hashes.
    page = page.replace("\r\n", "\n").replace("\r", "\n")
    page = re.sub(r'<meta http-equiv="Content-Security-Policy" content="[^"]*">\n?', '', page)
    hashes = []
    for attrs, body in re.findall(r'<script\b([^>]*)>(.*?)</script>', page, re.S | re.I):
        if re.search(r'\btype=[\"\x27]application/json[\"\x27]', attrs, re.I):
            continue
        if re.search(r'\bsrc\s*=', attrs, re.I):
            raise ValueError("External scripts require explicit security review")
        digest = base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode('ascii')
        hashes.append("'sha256-" + digest + "'")
    scripts = ' '.join(hashes + (["'wasm-unsafe-eval'"] if wasm else [])) or "'none'"
    policy = ("default-src 'none'; script-src " + scripts + "; "
              "script-src-attr 'none'; style-src 'unsafe-inline'; "
              "img-src 'self' data:; connect-src 'none'; object-src 'none'; "
              "base-uri 'none'; form-action 'self'")
    meta = '<meta http-equiv="Content-Security-Policy" content="' + html.escape(policy, quote=True) + '">'
    marker = '<meta charset="utf-8">'
    if marker not in page:
        raise ValueError("Missing charset marker for early CSP insertion")
    return page.replace(marker, marker + '\n' + meta, 1)
