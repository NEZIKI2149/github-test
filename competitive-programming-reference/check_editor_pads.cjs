const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const pw=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const engine=process.env.PADS_BROWSER||'chromium';
 const browser=await pw[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:390,height:850}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
  source=source.replace('\nrender();\n})();',`\nwindow.__padTest={reset:(s,a,h=a)=>{stopPad();stopRepeat();code=s;anchor=a;head=h;shift=0;ctrl=false;undo.length=redo.length=0;render();},state:()=>({code,anchor,head,active:!!activePad,pointer:activePad&&!activePad.extend?{x:activePad.pointerX,y:activePad.pointerY,target:positionFromEditorPoint(activePad.pointerX,activePad.pointerY)}:null})};\nrender();\n})();`);
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
  // Free pointer moves continuously on both axes; the caret commits on release only.
  await reset('abcdefghijklmnopqrstuvwxyz\nxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ',5);
  const box=await page.locator('#cursor-pad').boundingBox(),x=box.x+box.width/2,y=box.y+box.height/2;
  await page.mouse.move(x,y);await page.mouse.down();
  const initial=(await state()).pointer;
  await page.mouse.move(x+3,y+2);
  let preview=await state();assert.equal(preview.head,5);assert.equal(preview.anchor,5);
  assert(Math.abs(preview.pointer.x-initial.x-3)<1);assert(Math.abs(preview.pointer.y-initial.y-2)<1);
  await page.mouse.move(x+36,y+20,{steps:3});
  preview=await state();assert.equal(preview.head,5);assert.equal(preview.anchor,5);
  assert(Math.abs(preview.pointer.x-initial.x-36)<1);assert(Math.abs(preview.pointer.y-initial.y-20)<1);
  // A short line does not pull the pointer back toward its end.
  assert(preview.pointer.x>initial.x);
  const target=preview.pointer.target;
  await page.mouse.up();assert.equal((await state()).head,target);assert.equal((await state()).anchor,target);assert.equal((await state()).active,false);
  assert.equal(await page.locator('#cursor-pointer').isVisible(),false);
  assert.equal((await state()).code,'abcdefghijklmnopqrstuvwxyz\nxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ');
  const original=(await state()).code;
  await page.locator('.keyboard-main button[data-value="a"]').click();
  assert.equal((await state()).code,original.slice(0,target)+'a'+original.slice(target));
  await page.locator('#undo').click();assert.equal((await state()).code,original);
  // Cancellation must not collapse or alter an existing selection.
  for(const event of ['pointercancel','lostpointercapture']){
   await reset('abcdefghijklmnop',3,7);
   await page.locator('#cursor-pad').dispatchEvent('pointerdown',{pointerId:9,pointerType:'touch',isPrimary:true,button:0,clientX:50,clientY:50});
   await page.locator('#cursor-pad').dispatchEvent('pointermove',{pointerId:9,pointerType:'touch',isPrimary:true,buttons:1,clientX:80,clientY:65});
   assert.equal((await state()).head,7);assert.equal((await state()).anchor,3);
   await page.locator('#cursor-pad').dispatchEvent(event,{pointerId:9,pointerType:'touch'});
   assert.equal((await state()).head,7);assert.equal((await state()).anchor,3);assert.equal((await state()).active,false);
   assert.equal(await page.locator('#cursor-pointer').isVisible(),false);
  }
  for(const width of [320,390,844,1024,1194]){
   await page.setViewportSize({width,height:width===844?390:850});
   const ids=['selection-pad','cursor-pad','undo','redo','nav-arrow-left','nav-arrow-right'];
   const boxes=await Promise.all(ids.map(id=>page.locator('#'+id).boundingBox()));
   for(let i=0;i<boxes.length;i++){assert(boxes[i].x>=0);assert(boxes[i].x+boxes[i].width<=width);if(i)assert(boxes[i-1].x+boxes[i-1].width<=boxes[i].x);}
  }
  assert.deepEqual(errors,[]);
  console.log('PASS '+engine+': keyboard and swipe selection, free diagonal pointer, release-only commit, short lines, cancellation, Unicode, unchanged code, 5 layouts');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
