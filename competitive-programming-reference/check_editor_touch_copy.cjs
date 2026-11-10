const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const playwright=require(process.env.PLAYWRIGHT_PATH||'playwright');
const sample='#include <bits/stdc++.h>\n// 日本語\nint main(){return 0;}';
(async()=>{
 const engine=process.env.COPY_BROWSER||'webkit';
 const browser=await playwright[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1194,height:700},isMobile:true,hasTouch:true});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  let source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
  source=source.replace('\nrender();\n})();',`\nwindow.__touchCopy={reset:()=>{closeManualCopy();stopRepeat();code=${JSON.stringify(sample)};anchor=2;head=8;autoPairs=[];ctrl=false;shift=0;render();document.getElementById('copy-status').textContent='';},state:()=>({code,anchor,head})};\nrender();\n})();`);
  await page.route('https://editor.test/**',r=>r.fulfill({status:200,contentType:'text/html; charset=utf-8',body:source}));
  await page.goto('https://editor.test/mobile');await page.evaluate(()=>window.vscodeCppHighlighter);await page.clock.install();
  await page.evaluate(()=>{
   window.__realExec=document.execCommand;window.__nativeCopies=[];
   document.addEventListener('copy',()=>{const field=document.activeElement;if(field&&typeof field.value==='string')window.__nativeCopies.push(field.value.slice(field.selectionStart,field.selectionEnd));});
  });
  async function setup(legacy,api){
   await page.clock.runFor(900);
   await page.evaluate(({legacy,api})=>{
    window.__touchCopy.reset();window.__execCalls=0;window.__apiCalls=0;window.__nativeCopies=[];window.__apiText='';
    document.execCommand=function(...args){window.__execCalls++;return legacy==='native'?window.__realExec.apply(this,args):false;};
    Object.defineProperty(navigator,'clipboard',{configurable:true,value:api==='missing'?undefined:{writeText:text=>{
     window.__apiCalls++;window.__apiText=text;
     return api==='pending'?new Promise(()=>{}):api==='success'?Promise.resolve():Promise.reject(new DOMException('expected denial','NotAllowedError'));
    }}});
   },{legacy,api});
  }
  const state=()=>page.evaluate(()=>window.__touchCopy.state());
  const status=()=>page.locator('#copy-status').textContent();
  let count=0;
  await setup('native','pending');await page.locator('#copy').tap();
  await page.waitForFunction(()=>document.getElementById('copy-status').textContent==='コピーしました');
  assert.equal(await page.evaluate(()=>window.__apiCalls),0);assert.deepEqual(await page.evaluate(()=>window.__nativeCopies),[sample]);count++;
  const calls=await page.evaluate(()=>window.__execCalls);await page.locator('#copy').dispatchEvent('click',{detail:1});assert.equal(await page.evaluate(()=>window.__execCalls),calls);count++;
  await setup('false','pending');await page.locator('#copy').tap();assert.equal(await status(),'コピー処理中…');count++;
  await page.clock.runFor(1600);await page.waitForFunction(()=>!document.getElementById('manual-copy-panel').hidden);
  assert.equal(await page.locator('#manual-copy-text').inputValue(),sample);assert.deepEqual(await state(),{code:sample,anchor:2,head:8});assert.equal(await page.locator('#keyboard-dock').isVisible(),false);count++;
  await page.locator('#manual-copy-select').tap();
  const selection=await page.locator('#manual-copy-text').evaluate(e=>[e.selectionStart,e.selectionEnd,e.readOnly,getComputedStyle(e).webkitTouchCallout]);
  assert.equal(selection[0],0);assert.equal(selection[1],sample.length);assert.equal(selection[2],true);count++;
  await page.locator('#manual-copy-text').press('Control+c');assert.deepEqual(await page.evaluate(()=>window.__nativeCopies),[sample]);count++;
  await page.locator('#manual-copy-close').tap();assert.equal(await page.locator('#manual-copy-panel').isVisible(),false);assert.equal(await page.locator('#keyboard-dock').isVisible(),true);count++;
  await setup('false','success');await page.locator('#copy').tap();await page.waitForFunction(()=>document.getElementById('copy-status').textContent==='コピーしました');assert.equal(await page.evaluate(()=>window.__apiText),sample);count++;
  for(const api of ['denied','missing']){
   await setup('false',api);await page.locator('#copy').tap();await page.waitForFunction(()=>!document.getElementById('manual-copy-panel').hidden);assert.deepEqual(await state(),{code:sample,anchor:2,head:8});count++;
  }
  for(const cancel of ['move','cancel']){
   await setup('native','success');
   await page.locator('#copy').evaluate((button,cancel)=>{
    const r=button.getBoundingClientRect(),point={identifier:11,target:button,clientX:r.x+r.width/2,clientY:r.y+r.height/2};
    const touch=point;const send=(name,touches,changedTouches=[])=>{const event=new Event(name,{bubbles:true,cancelable:true});Object.defineProperties(event,{touches:{value:touches},changedTouches:{value:changedTouches}});button.dispatchEvent(event);};send('touchstart',[touch],[touch]);
    if(cancel==='move')send('touchmove',[{...point,clientX:point.clientX-30}]);
    send(cancel==='cancel'?'touchcancel':'touchend',[],[touch]);
    button.dispatchEvent(new MouseEvent('click',{bubbles:true,detail:1}));
   },cancel);
   assert.equal(await page.evaluate(()=>window.__execCalls+window.__apiCalls),0);count++;
  }
  for(const viewport of [{width:1194,height:700},{width:390,height:700}]){
   await page.setViewportSize(viewport);await setup('false','denied');await page.locator('#copy').tap();await page.waitForFunction(()=>!document.getElementById('manual-copy-panel').hidden);
   const visible=await page.locator('.manual-copy-content').evaluate(e=>{const r=e.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight});assert(visible);count++;
  }
  assert.deepEqual(errors,[]);console.log(JSON.stringify({engine,touchCopyChecks:count,pageErrors:errors}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
