const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const pw=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const engine=process.env.PADS_BROWSER||'chromium';
 const browser=await pw[engine].launch({headless:true,...(engine==='chromium'&&process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:390,height:850}}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  let source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
  source=source.replace('\nrender();\n})();',`\nwindow.__padTest={reset:(s,a,h=a)=>{stopPad();stopRepeat();code=s;anchor=a;head=h;shift=0;ctrl=false;undo.length=redo.length=0;render();},state:()=>({code,anchor,head,active:!!activePad,pointer:activePad?{x:activePad.pointerX,y:activePad.pointerY,target:positionFromEditorPoint(activePad.pointerX,activePad.pointerY)}:null})};\nrender();\n})();`);
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
  const text='abcdefghijklmnopqrstuvwxyz\nxy\nABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const traces=[];
  // Identical gestures must follow identical free coordinates, visible or hidden.
  for(const id of ['cursor-pad','selection-pad']){
   await reset(text,5);
   const box=await page.locator('#'+id).boundingBox(),x=box.x+box.width/2,y=box.y+box.height/2;
   await page.mouse.move(x,y);await page.mouse.down();
   assert.equal(await page.locator('#cursor-pointer').isVisible(),id==='cursor-pad');
   const initial=(await state()).pointer,trace=[];
   for(const [dx,dy] of [[3,2],[36,20],[36,40],[-12,20]]){
    await page.mouse.move(x+dx,y+dy,{steps:3});
    const preview=await state();assert.equal(preview.head,5);assert.equal(preview.anchor,5);
    assert(Math.abs(preview.pointer.x-initial.x-dx)<1);assert(Math.abs(preview.pointer.y-initial.y-dy)<1);
    trace.push(preview.pointer);
   }
   traces.push(trace);
   const target=(await state()).pointer.target;
   await page.mouse.up();assert.equal((await state()).head,target);
   assert.equal((await state()).anchor,id==='selection-pad'?5:target);
   assert.equal((await state()).active,false);assert.equal(await page.locator('#cursor-pointer').isVisible(),false);
   assert.equal((await state()).code,text);
   if(id==='cursor-pad'){
    await page.locator('.keyboard-main button[data-value="a"]').click();
    assert.equal((await state()).code,text.slice(0,target)+'a'+text.slice(target));
    await page.locator('#undo').click();assert.equal((await state()).code,text);
   }
  }
  assert.deepEqual(traces[0],traces[1]);
  // Cancel preserves both ends of an existing selection for either pad.
  for(const id of ['cursor-pad','selection-pad'])for(const event of ['pointercancel','lostpointercapture']){
   await reset('abcdefghijklmnop',3,7);
   await page.locator('#'+id).dispatchEvent('pointerdown',{pointerId:9,pointerType:'touch',isPrimary:true,button:0,clientX:50,clientY:50});
   await page.locator('#'+id).dispatchEvent('pointermove',{pointerId:9,pointerType:'touch',isPrimary:true,buttons:1,clientX:80,clientY:65});
   assert.equal((await state()).head,7);assert.equal((await state()).anchor,3);
   await page.locator('#'+id).dispatchEvent(event,{pointerId:9,pointerType:'touch'});
   assert.equal((await state()).head,7);assert.equal((await state()).anchor,3);assert.equal((await state()).active,false);
   assert.equal(await page.locator('#cursor-pointer').isVisible(),false);
  }
  // A release creates a reverse selection when dragged left of the fixed start.
  await reset('abcdefghijklmnop',9);
  const fire=(type,x)=>page.locator('#selection-pad').dispatchEvent(type,{pointerId:12,pointerType:'touch',isPrimary:true,button:0,buttons:type==='pointerup'?0:1,clientX:x,clientY:50});
  await fire('pointerdown',100);await fire('pointermove',64);
  const reverseTarget=(await state()).pointer.target;assert(reverseTarget<9);
  assert.equal((await state()).head,9);await fire('pointerup',64);
  assert.equal((await state()).anchor,9);assert.equal((await state()).head,reverseTarget);
  await fire('pointermove',20);assert.equal((await state()).head,reverseTarget);
  for(const width of [320,390,844,1024,1194]){
   await page.setViewportSize({width,height:width===844?390:850});
   const ids=['selection-pad','cursor-pad','undo','redo','nav-arrow-left','nav-arrow-right'];
   const boxes=await Promise.all(ids.map(id=>page.locator('#'+id).boundingBox()));
   for(let i=0;i<boxes.length;i++){assert(boxes[i].x>=0);assert(boxes[i].x+boxes[i].width<=width);if(i)assert(boxes[i-1].x+boxes[i-1].width<=boxes[i].x);}
  }
  assert.deepEqual(errors,[]);
  console.log('PASS '+engine+': identical free trajectories for both pads, hidden selection pointer, release-only commit, reverse selection, cancellation, Unicode, unchanged code, 5 layouts');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
