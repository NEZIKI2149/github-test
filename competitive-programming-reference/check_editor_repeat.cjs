const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
const os=require('node:os');
const sample='abcdefghijklmnopqrstuvwxyz'.repeat(20);
const selector='#keyboard-main [data-op="backspace"]';
function prepare(source,destination){
 const s=fs.readFileSync(source,'utf8').replace(/\r\n/g,'\n');
 const hook='\nwindow.__repeatTest={reset:()=>{stopRepeat();code='+JSON.stringify(sample)+';anchor=head=code.length;ctrl=false;shift=0;render();},value:()=>code};\nrender();\n})();';
 fs.writeFileSync(destination,require('./security_test_utils.cjs').refreshScriptHashes(s.replace('\nrender();\n})();',hook)));
}
async function pointer(page,type,{target=selector,pointerId=11,pointerType='touch',x,y,isPrimary=true,buttons}={}){
 const point=await page.locator(target).evaluate(e=>{const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2}});
 await page.evaluate(({type,target,pointerId,pointerType,x,y,isPrimary,buttons})=>{
  const e=new PointerEvent(type,{bubbles:true,cancelable:true,pointerId,pointerType,clientX:x,clientY:y,button:0,buttons,isPrimary});
  (target==='document'?document:document.querySelector(target)).dispatchEvent(e);
 },{type,target,pointerId,pointerType,x:x??point.x,y:y??point.y,isPrimary,buttons:buttons??(type==='pointerup'?0:1)});
}
(async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'neziki-repeat-test-'));
 const after=path.join(tmp,'editor.html');
 prepare(path.join(__dirname,'mobile-editor.html'),after);
 process.on('exit',()=>{fs.unlinkSync(after);fs.rmdirSync(tmp);});
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 const context=await browser.newContext({viewport:{width:1280,height:846},hasTouch:true});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 async function load(file){await page.goto(pathToFileURL(file).href);await page.evaluate(()=>window.vscodeCppHighlighter);await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));}
 async function reset(){await page.evaluate(()=>window.__repeatTest.reset());}
 async function value(){return page.evaluate(()=>window.__repeatTest.value());}
 async function outside(type,options={}){
  await page.evaluate(({type,options})=>document.dispatchEvent(new PointerEvent(type,{bubbles:true,cancelable:true,pointerId:11,pointerType:'touch',isPrimary:true,clientX:1,clientY:1,button:0,buttons:0,...options})),{type,options});
 }
 await load(after);await page.clock.install();await reset();
 const tests=[];
 async function stable(name,interrupt,options={}){
  await reset();await pointer(page,'pointerdown',options);await page.clock.runFor(675);
  assert((await value()).length<sample.length,'long press did not repeat');
  await interrupt();const stopped=await value();await page.clock.runFor(1500);assert.equal(await value(),stopped,name+' kept deleting');tests.push(name);
 }
 await reset();await pointer(page,'pointerdown',{pointerType:'mouse'});await outside('pointerup',{pointerType:'mouse'});await page.clock.runFor(1500);assert.equal((await value()).length,sample.length-1);tests.push('mouse release outside before delay');
 await reset();await pointer(page,'pointerdown');await pointer(page,'pointerup');await page.clock.runFor(1500);assert.equal((await value()).length,sample.length-1);tests.push('touch tap exactly once');
 await stable('touch release outside',()=>outside('pointerup'));
 await stable('pen release outside',()=>outside('pointerup',{pointerType:'pen'}),{pointerType:'pen'});
 await stable('pointer cancellation',()=>outside('pointercancel'));
 await stable('lost pointer capture',()=>outside('lostpointercapture'));
 for(const event of ['blur','pagehide','resize','orientationchange','contextmenu'])await stable(event,()=>page.evaluate(event=>window.dispatchEvent(new Event(event)),event));
 for(const event of ['visibilitychange','scroll'])await stable(event,()=>page.evaluate(event=>document.dispatchEvent(new Event(event)),event));
 await stable('another finger',()=>outside('pointerdown',{pointerId:22,isPrimary:false,buttons:1}));
 await stable('another control click',()=>page.locator('#undo').evaluate(e=>e.click()));
 await stable('physical key',()=>page.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'Shift',bubbles:true}))));
 await stable('drag off key',()=>outside('pointermove',{buttons:1}));
 await reset();await pointer(page,'pointerdown');await page.clock.runFor(675);await pointer(page,'pointerup');const held=await value();await page.locator(selector).evaluate(e=>e.click());assert.equal(await value(),held);tests.push('no duplicate iOS zero-detail click');
 await reset();await pointer(page,'pointerdown');await outside('pointercancel');await page.clock.runFor(1500);assert.equal(await value(),sample);tests.push('cancelled tap edits nothing');
 await reset();await pointer(page,'pointerdown');await page.clock.runFor(200);await pointer(page,'pointerdown',{target:'#keyboard-main [data-value="a"]',pointerId:22});await pointer(page,'pointerup',{target:'#keyboard-main [data-value="a"]',pointerId:22});const replaced=await value();await page.clock.runFor(1500);assert.equal(await value(),replaced);assert.equal(replaced,sample+'a');tests.push('new key cancels previous delayed delete');
 await reset();await pointer(page,'pointerdown',{target:'#keyboard-main [data-op="ctrl"]'});await pointer(page,'pointerup',{target:'#keyboard-main [data-op="ctrl"]'});await pointer(page,'pointerdown');await page.clock.runFor(1000);assert.equal(await value(),sample);await pointer(page,'pointerup');const wordDeleted=await value();await page.clock.runFor(1500);assert.equal(await value(),wordDeleted);assert.equal(wordDeleted,'');tests.push('Ctrl+Backspace stays one-shot');
 await reset();
 const bounds=await page.locator(selector).boundingBox();const point={x:bounds.x+bounds.width/2,y:bounds.y+bounds.height/2};
 await page.mouse.move(point.x,point.y);await page.mouse.down();await page.clock.runFor(675);
 assert((await value()).length<sample.length-1);await page.mouse.up();const mouseStopped=await value();await page.clock.runFor(1500);assert.equal(await value(),mouseStopped);tests.push('native mouse capture and release');
 await reset();const cdp=await context.newCDPSession(page);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{...point,id:0}]});await page.clock.runFor(675);
 assert((await value()).length<sample.length);await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});const touchStopped=await value();await page.clock.runFor(1500);assert.equal(await value(),touchStopped);tests.push('native touch capture and release');await cdp.detach();
 assert.deepEqual(errors,[]);console.log(JSON.stringify({regressions:tests,pageErrors:errors}));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
