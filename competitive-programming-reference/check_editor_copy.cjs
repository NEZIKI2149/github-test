const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const sample='#include <bits/stdc++.h>\n// 日本語のコメント\nint main(){cout << "<>&\\n";}';
const origin='https://editor.test';
function instrument(source){
 const hook=`
 window.__copyTest={reset:(text,a=0,h=a)=>{closeManualCopy();stopRepeat();code=text;anchor=a;head=h;autoPairs=[];undo.length=redo.length=0;stopUndoGroup();ctrl=false;shift=0;render();},
 copy:()=>copy(code),state:()=>({code,anchor,head,undo:undo.length})};
 render();
 })();`;
 return source.replace(/\r\n/g,'\n').replace('\nrender();\n})();',hook);
}
(async()=>{
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1280,height:846},hasTouch:true});
  await context.grantPermissions(['clipboard-read','clipboard-write'],{origin});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  const source=instrument(fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8'));
  await page.route(origin+'/**',route=>route.fulfill({status:200,contentType:'text/html; charset=utf-8',body:source}));
  await page.goto(origin+'/editor');await page.evaluate(()=>window.vscodeCppHighlighter);
  await page.evaluate(()=>{
   window.__realClipboard=navigator.clipboard;window.__realWrite=navigator.clipboard.writeText;
   window.__realExec=document.execCommand;window.__fallbackAttempts=0;
   document.execCommand=function(...args){if(args[0]==='copy')window.__fallbackAttempts++;return window.__realExec.apply(this,args)};
  });
  const reset=(...args)=>page.evaluate(args=>window.__copyTest.reset(...args),args);
  const state=()=>page.evaluate(()=>window.__copyTest.state());
  const clipboard=()=>page.evaluate(()=>window.__realClipboard.readText().then(t=>t.replace(/\r\n/g,'\n')));
  async function mode(value){await page.evaluate(value=>{
   Object.defineProperty(navigator,'clipboard',{configurable:true,value:value==='missing'?undefined:window.__realClipboard});
   Object.defineProperty(window.__realClipboard,'writeText',{configurable:true,value:value==='denied'?()=>Promise.reject(new DOMException('expected denial','NotAllowedError')):value==='throws'?()=>{throw Error('expected failure')}:window.__realWrite});
   document.execCommand=function(...args){if(args[0]==='copy')window.__fallbackAttempts++;return window.__realExec.apply(this,args)};
  },value)}
  async function clickCopy(){await page.locator('#copy').click();await page.waitForFunction(()=>document.getElementById('toast').textContent.includes('コピー'));}
  let count=0;
  await mode('normal');await reset(sample,1,8);await clickCopy();assert.equal(await clipboard(),sample);assert.equal((await state()).head,8);assert.equal((await state()).anchor,8);assert.equal((await state()).code,sample);assert.equal(await page.evaluate(()=>window.__fallbackAttempts),1);count++;
  for(const value of ['denied','missing','throws']){
   await mode(value);await reset(sample,1,8);await clickCopy();await page.waitForFunction(()=>window.__copyTest.state().anchor===window.__copyTest.state().head);
   assert.equal(await clipboard(),sample);assert.equal((await state()).head,8);assert.equal((await state()).code,sample);assert.equal(await page.locator('textarea[aria-hidden="true"]').count(),0);assert.equal((await state()).undo,0);count++;
  }
  await mode('denied');await reset(sample,1,8);await page.evaluate(()=>{document.execCommand=()=>false;document.getElementById('toast').textContent=''});await clickCopy();await page.waitForFunction(()=>document.getElementById('toast').textContent.includes('使えません'));
  assert.deepEqual(await state(),{code:sample,anchor:1,head:8,undo:0});count++;
  await mode('denied');await reset(sample,1,8);await page.evaluate(()=>{document.execCommand=()=>{throw Error('expected fallback failure')};document.getElementById('toast').textContent=''});await clickCopy();await page.waitForFunction(()=>document.getElementById('toast').textContent.includes('使えません'));
  assert.deepEqual(await state(),{code:sample,anchor:1,head:8,undo:0});assert.equal(await page.locator('textarea[aria-hidden="true"]').count(),0);count++;
  await mode('normal');await reset('');await clickCopy();assert.equal(await clipboard(),'');count++;
  await mode('denied');await reset('abcdef',1,4);await page.locator('#keyboard-main [data-op="ctrl"]').click();await page.locator('#keyboard-main [data-value="c"]').click();await page.waitForFunction(()=>!document.querySelector('#keyboard-main [data-op="ctrl"]').classList.contains('pressed'));assert.equal(await clipboard(),'bcd');assert.equal((await state()).code,'abcdef');count++;
  await reset('abcdef',1,4);await page.locator('#keyboard-main [data-op="ctrl"]').click();await page.locator('#keyboard-main [data-value="x"]').click();await page.waitForFunction(()=>window.__copyTest.state().code==='aef');assert.equal(await clipboard(),'bcd');count++;
  await reset('abcdef',1,4);await page.locator('#editor').dispatchEvent('keydown',{key:'c',code:'KeyC',ctrlKey:true});await page.waitForFunction(()=>window.__copyTest.state().anchor===window.__copyTest.state().head);assert.equal(await clipboard(),'bcd');count++;
  await mode('normal');await reset(sample,1,8);
  await page.evaluate(()=>{Object.defineProperty(window.__realClipboard,'writeText',{configurable:true,value:()=>new Promise(resolve=>{window.__resolveCopy=resolve})});window.__pendingCopy=window.__copyTest.copy()});
  await reset('new code',2,5);await page.evaluate(async()=>{window.__resolveCopy();await window.__pendingCopy});assert.deepEqual(await state(),{code:'new code',anchor:2,head:5,undo:0});count++;
  const views=[];
  for(const viewport of [{width:1280,height:846},{width:1024,height:650},{width:390,height:700},{width:844,height:390}]){
   await page.setViewportSize(viewport);await mode('denied');await reset(sample,1,8);await page.locator('#copy').click();
   await page.waitForFunction(()=>window.__copyTest.state().anchor===window.__copyTest.state().head);
   const g=await page.evaluate(()=>{const toast=document.getElementById('toast'),dock=document.getElementById('keyboard-dock'),a=toast.getBoundingClientRect(),b=dock.getBoundingClientRect();return {top:a.top,bottom:a.bottom,dockTop:b.top,z:+getComputedStyle(toast).zIndex,dockZ:+getComputedStyle(dock).zIndex}});
   assert(g.top>=0&&g.bottom<g.dockTop&&g.z>g.dockZ);assert.equal(await clipboard(),sample);views.push(viewport);count++;
  }
  assert.deepEqual(errors,[]);console.log(JSON.stringify({clipboardChecks:count,feedbackViewports:views,pageErrors:errors}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
