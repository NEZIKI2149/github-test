// Exercise the production HTML with its actual CSP, without editor test hooks.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const pw=require(process.env.PLAYWRIGHT_PATH||'playwright');
const root=__dirname;
(async()=>{
 const server=http.createServer((req,res)=>{
  const name=new URL(req.url,'http://localhost').pathname;
  const file=name==='/mobile-editor.html'?'mobile-editor.html':'index.html';
  res.setHeader('Content-Type','text/html; charset=utf-8');res.end(fs.readFileSync(path.join(root,file)));
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const origin='http://127.0.0.1:'+server.address().port;
 const engine=process.env.SECURITY_BROWSER||'chromium';
 const browser=await pw[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const context=await browser.newContext();
  const page=await context.newPage(),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
  await page.addInitScript(()=>{
   window.__violations=[];
   document.addEventListener('securitypolicyviolation',e=>window.__violations.push(e.effectiveDirective));
  });
  for(const hash of ['#%','#%E0%A4%A','#%FF','#algo/imos']){
   await page.goto(origin+'/'+hash);
   await page.locator('#search').fill('vector');
   assert(await page.locator('.side-link').count()>0);
  }
  await page.goto(origin+'/?security-copy=1#algo/imos');
  await page.locator('[data-copy]').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent.includes('コピー'));
  assert.deepEqual(await page.evaluate(()=>window.__violations),[]);
  await page.evaluate(()=>localStorage.setItem('neziki-cpp-mobile-editor-v1',JSON.stringify({code:'int main(){int x=1;return x;}',anchor:27,head:27})));
  await page.goto(origin+'/mobile-editor.html');
  await page.evaluate(()=>window.vscodeCppHighlighter);
  await page.waitForFunction(()=>document.querySelector('#syntax-layer span'));
  await page.locator('#format-code').click();
  await page.waitForFunction(()=>document.querySelector('#toast').textContent==='コード全体を整形しました');
  assert((await page.locator('#editor').inputValue()).includes('\n'));
  await page.locator('#copy').click();
  await page.waitForFunction(()=>document.querySelector('#copy-status').textContent.length>0);
  assert.deepEqual(errors,[]);
  assert.deepEqual(await page.evaluate(()=>window.__violations),[]);
  // Pasted markup is text, not executable HTML.
  const payload='<img src=x onerror="window.__injected=true"><script>window.__injected=true</script>';
  await page.addInitScript(payload=>localStorage.setItem('neziki-cpp-mobile-editor-v1',JSON.stringify({code:payload,anchor:0,head:0})),payload);
  await page.reload();await page.evaluate(()=>window.vscodeCppHighlighter);
  assert.equal(await page.locator('#editor').inputValue(),payload);
  assert.equal(await page.locator('#syntax-layer').textContent(),payload);
  assert.equal(await page.evaluate(()=>window.__injected),undefined);
  // A new inline script and fetch are both blocked by the production CSP.
  await page.evaluate(()=>{const s=document.createElement('script');s.textContent='window.__unapproved=true';document.body.append(s);});
  assert.equal(await page.evaluate(()=>window.__unapproved),undefined);
  assert.equal(await page.evaluate(()=>fetch('/blocked').then(()=>false,()=>true)),true);
  await page.waitForFunction(()=>window.__violations.includes('connect-src'));
  assert((await page.evaluate(()=>window.__violations)).some(x=>x==='script-src-elem'||x==='script-src'));
  assert(requests.every(url=>new URL(url).origin===origin));
  assert(!requests.some(url=>url.endsWith('/blocked')));
  console.log('PASS '+engine+': malformed URLs, search, copy, highlighting, WASM formatting, text safety, blocked script and fetch; no unexpected requests/errors');
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
