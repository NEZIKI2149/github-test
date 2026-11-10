const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const playwright=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const engine=process.env.KEYS_BROWSER||'webkit';
 const browser=await playwright[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const context=await browser.newContext({viewport:{width:1194,height:700},isMobile:true,hasTouch:true});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  let source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
  source=source.replace('\nrender();\n})();',`\nwindow.__keysTest={reset:(text='',cursor=text.length)=>{stopRepeat();code=text;anchor=head=cursor;autoPairs=[];ctrl=false;shift=0;lastShift=0;undo.length=redo.length=0;render();},state:()=>({code,anchor,head,shift,scroll:kbViewport.scrollLeft})};\nrender();\n})();`);
  await page.route('https://editor.test/**',r=>r.fulfill({status:200,contentType:'text/html; charset=utf-8',body:source}));
  await page.goto('https://editor.test/keys');await page.evaluate(()=>window.vscodeCppHighlighter);
  const reset=(...args)=>page.evaluate(args=>window.__keysTest.reset(...args),args),state=()=>page.evaluate(()=>window.__keysTest.state());
  async function geometry(){return page.evaluate(()=>{
   const enter=document.getElementById('right-enter'),shift=document.getElementById('right-shift');
   const points=(key)=>{const r=key.getBoundingClientRect();return {upper:[r.x+r.width*.08,r.y+r.height*.25],lower:[r.x+r.width*.8,r.y+r.height*.75],cutout:[r.x+r.width*.03,r.y+r.height*.75]}};
   function hit(point){return document.elementFromPoint(...point)?.closest('button')?.id||'';}
   const a=points(enter),b=points(shift);
   return {enterUpper:hit(a.upper),enterLower:hit(a.lower),enterCutout:hit(a.cutout),shiftUpper:hit(b.upper),shiftLower:hit(b.lower),shiftCutout:hit(b.cutout),
    enterCount:document.querySelectorAll('#keyboard-main [data-op="enter"]').length,shiftCount:document.querySelectorAll('#keyboard-main [data-op="shift"]').length};
  });}
  let count=0;const views=[];
  for(const viewport of [{width:1194,height:700},{width:1024,height:650},{width:834,height:1000},{width:390,height:700},{width:844,height:390}]){
   await page.setViewportSize(viewport);const g=await geometry();
   assert.equal(g.enterUpper,'right-enter');assert.equal(g.enterLower,'right-enter');assert.notEqual(g.enterCutout,'right-enter');
   assert.equal(g.shiftUpper,'right-shift');assert.equal(g.shiftLower,'right-shift');assert.notEqual(g.shiftCutout,'right-shift');
   assert.equal(g.enterCount,1);assert.equal(g.shiftCount,2);views.push(viewport);count++;
  }
  await page.setViewportSize({width:390,height:700});await page.locator('#fit-keys').tap();
  await page.locator('#keyboard-viewport').evaluate(e=>{e.scrollLeft=e.scrollWidth-e.clientWidth});
  const g=await geometry();assert.equal(g.enterUpper,'right-enter');assert.equal(g.shiftUpper,'right-shift');count++;
  await reset();const startScroll=(await state()).scroll;
  await page.locator('#right-shift').tap();
  assert.equal(await page.locator('#left-shift').getAttribute('aria-pressed'),'true');assert.equal(await page.locator('#right-shift').getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('#keyboard-main [data-value="."] .key-legend').textContent(),'>');count++;
  await page.locator('#keyboard-main [data-value="."]').tap();assert.equal((await state()).code,'>');assert.equal((await state()).shift,0);assert(Math.abs((await state()).scroll-startScroll)<1);count++;
  assert.equal(await page.locator('#left-shift').getAttribute('aria-pressed'),'false');assert.equal(await page.locator('#right-shift').getAttribute('aria-pressed'),'false');count++;
  await reset();await page.locator('#right-shift').tap();await page.locator('#keyboard-main [data-value="["]').tap();assert.equal((await state()).code,'{}');assert.equal((await state()).head,1);count++;
  const bounds=await page.locator('#right-enter').boundingBox();
  for(const position of [{x:bounds.width*.08,y:bounds.height*.25},{x:bounds.width*.8,y:bounds.height*.75}]){
   await reset('{}',1);await page.locator('#right-enter').tap({position});assert.equal((await state()).code,'{\n    \n}');assert.equal((await state()).head,6);count++;
  }
  const shiftBounds=await page.locator('#right-shift').boundingBox();
  for(const position of [{x:shiftBounds.width*.08,y:shiftBounds.height*.25},{x:shiftBounds.width*.8,y:shiftBounds.height*.75}]){
   await reset();await page.locator('#right-shift').tap({position});assert.equal((await state()).shift,1);count++;
  }
  await reset();await page.locator('#right-shift').tap();await page.locator('#right-shift').tap();assert.equal((await state()).shift,2);
  await page.locator('#keyboard-main [data-value="p"]').tap();assert.equal((await state()).code,'P');assert.equal((await state()).shift,2);
  await page.locator('#right-shift').tap();await page.locator('#keyboard-main [data-value="p"]').tap();assert.equal((await state()).code,'Pp');count++;
  await reset();
  if(process.env.EDITOR_KEYS_SCREENSHOT)await page.screenshot({path:process.env.EDITOR_KEYS_SCREENSHOT,fullPage:false});
  assert.deepEqual(errors,[]);console.log(JSON.stringify({engine,rightKeyChecks:count,viewports:views,pageErrors:errors}));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
