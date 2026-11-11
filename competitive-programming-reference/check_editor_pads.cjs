const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const pw=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const engine=process.env.PADS_BROWSER||'chromium';
 const browser=await pw[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:390,height:850}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
  source=source.replace('\nrender();\n})();',`\nwindow.__padTest={reset:(s,a,h=a)=>{stopPad();stopRepeat();code=s;anchor=a;head=h;shift=0;ctrl=false;undo.length=redo.length=0;render();},state:()=>({code,anchor,head,active:!!activePad})};\nrender();\n})();`);
  source=require('./security_test_utils.cjs').refreshScriptHashes(source);
  await page.route('https://pads.test/**',r=>r.fulfill({contentType:'text/html; charset=utf-8',body:source}));
  await page.goto('https://pads.test/');await page.evaluate(()=>window.vscodeCppHighlighter);
  const reset=(...args)=>page.evaluate(args=>window.__padTest.reset(...args),args);
  const state=()=>page.evaluate(()=>window.__padTest.state());
  const press=(id,key)=>page.locator('#'+id).press(key);
  await reset('abcdef\nxy\n12345',2);
  await press('selection-pad','ArrowRight');assert.equal((await state()).head,3);assert.equal((await state()).anchor,2);
  await press('selection-pad','ArrowDown');assert.equal((await state()).head,9);assert.equal((await state()).anchor,2);
  await press('cursor-pad','ArrowLeft');assert.equal((await state()).head,2);assert.equal((await state()).anchor,2);
  await reset('a😀b',1);await press('selection-pad','ArrowRight');assert.equal((await state()).head,3);
  await press('selection-pad','ArrowLeft');assert.equal((await state()).head,1);
  await reset('abcdef',2);
  const pointer=(type,x,y)=>page.evaluate(({type,x,y})=>{
   const pad=document.getElementById('selection-pad');
   pad.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,pointerId:7,pointerType:'touch',isPrimary:true,button:0,buttons:type==='pointerup'?0:1,clientX:x,clientY:y}));
  },{type,x,y});
  await pointer('pointerdown',50,50);await pointer('pointermove',74,50);
  assert.equal((await state()).head,4);assert.equal((await state()).anchor,2);
  await pointer('pointermove',38,50);assert.equal((await state()).head,1);assert.equal((await state()).anchor,2);
  await pointer('pointerup',38,50);await pointer('pointermove',100,50);assert.equal((await state()).head,1);assert.equal((await state()).active,false);
  for(const cancel of ['pointercancel','lostpointercapture']){
   await pointer('pointerdown',50,50);await pointer(cancel,50,50);await pointer('pointermove',100,50);assert.equal((await state()).active,false);assert.equal((await state()).head,1);
  }
  // Real mouse capture continues outside the pad, then stops on release.
  await reset('abcdefghijklmnopqrstuvwxyz',5);
  const box=await page.locator('#cursor-pad').boundingBox(),x=box.x+box.width/2,y=box.y+box.height/2;
  await page.mouse.move(x,y);await page.mouse.down();await page.mouse.move(x+36,y,{steps:3});await page.mouse.up();
  assert.equal((await state()).head,8);assert.equal((await state()).anchor,8);assert.equal((await state()).active,false);
  assert.equal((await state()).code,'abcdefghijklmnopqrstuvwxyz');
  for(const width of [320,390,844,1024,1194]){
   await page.setViewportSize({width,height:width===844?390:850});
   const ids=['selection-pad','cursor-pad','undo','redo','nav-arrow-left','nav-arrow-right'];
   const boxes=await Promise.all(ids.map(id=>page.locator('#'+id).boundingBox()));
   for(let i=0;i<boxes.length;i++){assert(boxes[i].x>=0);assert(boxes[i].x+boxes[i].width<=width);if(i)assert(boxes[i-1].x+boxes[i-1].width<=boxes[i].x);}
  }
  assert.deepEqual(errors,[]);
  console.log('PASS '+engine+': keyboard and swipe selection, reverse selection, Unicode, pointer capture/cancellation, release, unchanged code, 5 layouts');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
