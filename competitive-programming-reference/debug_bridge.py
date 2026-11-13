"""Local, authenticated C++ runner. Submitted programs run with YOUR user privileges."""
import http.server, json, secrets, shutil, subprocess, tempfile, threading, time, os, signal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
PORT = 8765
ORIGINS = {'https://neziki2149.github.io', f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'}
LOCK = threading.Lock()
ACTIVE = None
BUSY = False
CANCEL = threading.Event()

def terminate(p):
    if p and p.poll() is None:
        try:
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)
            else:
                os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

def execute(args, folder, stdin, seconds):
    global ACTIVE
    with tempfile.TemporaryFile() as inp, tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        inp.write(stdin.encode()); inp.seek(0)
        with LOCK:
            if CANCEL.is_set(): return {'status':'停止しました', 'stdout':'', 'stderr':'', 'exitCode':None}
            p = subprocess.Popen(args, cwd=folder, stdin=inp, stdout=out, stderr=err,
                                 start_new_session=os.name != 'nt')
            ACTIVE = p
        start = time.monotonic(); status = ''
        try:
            while p.poll() is None:
                if CANCEL.is_set(): status = '停止しました'
                elif time.monotonic()-start > seconds: status = '制限時間を超えました'
                elif os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size > 1024*1024: status = '出力上限を超えました'
                if status: terminate(p); break
                time.sleep(.02)
            p.wait()
        finally:
            # Also clean up children spawned by a program that has already exited.
            if os.name != 'nt':
                try: os.killpg(p.pid, signal.SIGKILL)
                except ProcessLookupError: pass
            with LOCK: ACTIVE = None
        out.seek(0); err.seek(0)
        return {'status':status or ('停止しました' if CANCEL.is_set() else '完了' if p.returncode == 0 else 'エラー'),
                'stdout':out.read(1024*1024).decode('utf8', 'replace'),
                'stderr':err.read(1024*1024).decode('utf8', 'replace'), 'exitCode':p.returncode}

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def allowed(self):
        return self.headers.get('Host') in {f'127.0.0.1:{PORT}', f'localhost:{PORT}'} and self.headers.get('Origin', '') in ORIGINS
    def headers_for(self, status, kind='application/json; charset=utf-8'):
        self.send_response(status)
        origin = self.headers.get('Origin', '')
        if origin in ORIGINS: self.send_header('Access-Control-Allow-Origin', origin)
        self.send_header('Vary', 'Origin')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Neziki-Key')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.send_header('Content-Type', kind)
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
    def reply(self, status, value):
        self.headers_for(status); self.wfile.write(json.dumps(value, ensure_ascii=False).encode())
    def do_OPTIONS(self):
        self.headers_for(204 if self.allowed() else 403)
    def do_GET(self):
        if self.headers.get('Host') not in {f'127.0.0.1:{PORT}', f'localhost:{PORT}'}: return self.reply(403, {})
        name = self.path.split('?')[0].lstrip('/') or 'debug.html'
        if name not in {'debug.html','mobile-editor.html'}: return self.reply(404, {})
        self.headers_for(200, 'text/html; charset=utf-8'); self.wfile.write((ROOT/name).read_bytes())
    def do_POST(self):
        global BUSY
        if not self.allowed() or not secrets.compare_digest(self.headers.get('X-Neziki-Key',''), TOKEN): return self.reply(403, {'error':'接続キーまたは接続元を確認してください'})
        if self.path == '/status': return self.reply(200, {'compiler':shutil.which('g++') or '', 'ready':bool(shutil.which('g++'))})
        if self.path == '/stop':
            with LOCK:
                CANCEL.set(); terminate(ACTIVE)
            return self.reply(200, {'status':'停止を要求しました'})
        if self.path != '/run': return self.reply(404, {})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 1024*1024: return self.reply(413, {'error':'コードと入力の合計は1 MBまでです'})
            data = json.loads(self.rfile.read(size))
            if not isinstance(data.get('code'), str) or not isinstance(data.get('input', ''), str): raise ValueError()
        except (ValueError, TypeError): return self.reply(400, {'error':'入力形式が正しくありません'})
        with LOCK:
            if BUSY: return self.reply(409, {'error':'実行中です'})
            BUSY = True; CANCEL.clear()
        try:
            compiler = shutil.which('g++')
            if not compiler: return self.reply(503, {'error':'g++ が見つかりません'})
            with tempfile.TemporaryDirectory(prefix='neziki-run-') as folder:
                source = Path(folder)/'main.cpp'; source.write_text(data['code'], encoding='utf8')
                binary = str(Path(folder)/('main.exe' if os.name == 'nt' else 'main'))
                result = execute([compiler,'-std=gnu++23','-O0','-g','-Wall','-Wextra',str(source),'-o',binary],folder,'',30)
                result['stage'] = 'コンパイル'
                if result['exitCode'] == 0 and not CANCEL.is_set():
                    result = execute([binary],folder,data.get('input',''),5); result['stage'] = '実行'
                self.reply(200, result)
        except Exception as e:
            self.reply(500, {'error':str(e)})
        finally:
            with LOCK: BUSY = False

if __name__ == '__main__':
    server = http.server.ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
    print('ネジキチートシート：PC実行補助', flush=True)
    print('自分で内容を確認したコードだけを実行してください。実行コードはこのPCのファイルにアクセスできます。', flush=True)
    print('接続キー: '+TOKEN, flush=True)
    print(f'ローカル版: http://127.0.0.1:{PORT}/#'+TOKEN, flush=True)
    print('終了: Ctrl+C', flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt:
        CANCEL.set(); terminate(ACTIVE)
    finally: server.server_close()
