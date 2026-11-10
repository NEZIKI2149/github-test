const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'neziki-commands-test-')),file=path.join(tmp,'editor.html');
 const source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
 const hook=`
 window.__commands={reset:(text,a=text.length,h=a)=>{stopRepeat();code=text;anchor=a;head=h;autoPairs=[];undo.length=redo.length=0;stopUndoGroup();ctrl=false;shift=0;render();},
 select:(a,h=a)=>{stopUndoGroup();anchor=a;head=h;render();},comment:toggleLineComment,tab:handleTab,format:formatCode,history,backspace,type:t=>insert(t,'type'),
 state:()=>({code,anchor,head,pairs:autoPairs.map(p=>({...p})),undo:undo.length,redo:redo.length}),style:FORMAT_STYLE};
 render();
 })();`;
 fs.writeFileSync(file,source.replace('\nrender();\n})();',hook));
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:846},hasTouch:true}),errors=[],requests=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
  await page.goto(pathToFileURL(file).href);await page.evaluate(()=>window.vscodeCppHighlighter);
  const call=(name,...args)=>page.evaluate(({name,args})=>window.__commands[name](...args),{name,args});
  const state=()=>call('state'),reset=(...args)=>call('reset',...args);
  let count=0;
  async function expect(text){assert.equal((await state()).code,text);count++;}
  const text='int a;\n    int b;\nint c;',end=text.indexOf('int c;');
  await reset(text,0,end);await call('comment');await expect('// int a;\n    // int b;\nint c;');
  await call('comment');await expect(text);await call('history',false);await expect('// int a;\n    // int b;\nint c;');
  await reset('// old\nint b;',0,13);await call('comment');await expect('// // old\n// int b;');await call('comment');await expect('// old\nint b;');
  await reset('a\nb\n',0,4);await call('comment');await expect('// a\n// b\n');
  await reset('a\nb',3,0);await call('comment');await expect('// a\n// b');assert((await state()).anchor>(await state()).head);
  await reset('a\nb',3);await call('comment');await expect('a\n// b');
  await reset('');await call('comment');await expect('// ');await call('comment');await expect('');
  await reset('int a;',0,6);await page.locator('#editor').dispatchEvent('keydown',{key:'/',code:'Slash',ctrlKey:true});await expect('// int a;');
  await reset('a\nb',0,3);await page.locator('#keyboard-main [data-op="ctrl"]').click();await page.locator('#keyboard-main [data-value="/"]').click();await expect('// a\n// b');
  await reset('a\n  b\nc',0,6);await call('tab',false);await expect('    a\n      b\nc');await call('tab',true);await expect('a\n  b\nc');
  await reset('a\nb',3,0);await call('tab',false);await expect('    a\n    b');assert((await state()).anchor>(await state()).head);await call('history',false);await expect('a\nb');
  await reset('a\nb',0,2);await page.locator('#editor').dispatchEvent('keydown',{key:'Tab',code:'Tab'});await expect('    a\nb');
  await page.locator('#editor').dispatchEvent('keydown',{key:'Tab',code:'Tab',shiftKey:true});await expect('a\nb');
  await reset('a',1);await call('tab',false);await expect('a    ');
  await reset('\tfoo\n  bar\nplain',0,16);await call('tab',true);await expect('foo\nbar\nplain');
  await reset('a\r\nb\r\n',0,6);await call('tab',false);await expect('    a\r\n    b\r\n');
  await reset('');await call('type','(');await call('select',0,2);await call('tab',false);await call('select',5);await call('backspace');await expect('    ');
  await reset('');await call('type','(');await call('comment');const commented=await state();assert.equal(commented.pairs.length,1);await call('backspace');await expect('// ');
  const ugly='#include <z>\n#include <a>\nusing namespace std;\nint main(){int x=1;if(x){x++;}return 0;}';
  await reset(ugly,ugly.indexOf('x++'));await call('format');const formatted=await state();
  assert(formatted.code.includes('\n    int x = 1;\n'));assert(formatted.code.includes('if(x) {\n        x++;\n    }'));
  assert(formatted.code.indexOf('<z>')<formatted.code.indexOf('<a>'));assert.equal(formatted.undo,1);count++;
  await call('history',false);await expect(ugly);await call('history',true);await expect(formatted.code);
  await call('format');assert.equal((await state()).undo,1);count++;
  const literals=String.raw`#define STEP(x) do { x++; } while(0)
int main(){const char* s="a  //  b { }"; const char* raw=R"tag(a   b
{ // raw })tag"; // comment   spacing
return 0;}`;
  await reset(literals);await call('format');const literalOutput=(await state()).code;
  assert(literalOutput.includes('"a  //  b { }"'));assert(literalOutput.includes('R"tag(a   b\n{ // raw })tag"'));assert(literalOutput.includes('comment   spacing'));count++;
  await reset('int main()');await call('type','{');await call('format');const pair=await state();assert.equal(pair.pairs.length,1);assert.equal(pair.code[pair.pairs[0].end],'}');await call('backspace');assert(!(await state()).code.includes('{'));count++;
  await page.evaluate(()=>{window.__realFormatter=loadCppFormatter;window.loadCppFormatter=async()=>({format:()=>{throw Error('expected test failure')}})});
  await reset('int x=1;');await call('format');await expect('int x=1;');assert.equal((await state()).undo,0);
  await page.evaluate(()=>{window.loadCppFormatter=()=>new Promise(resolve=>{window.__resolveFormatter=resolve})});
  await reset('int x=1;');await page.evaluate(()=>{window.__formatPending=window.__commands.format()});await reset('int y=2;');
  await page.evaluate(async()=>{window.__resolveFormatter(await window.__realFormatter());await window.__formatPending});await expect('int y=2;');
  await page.evaluate(()=>{window.loadCppFormatter=window.__realFormatter});
  const geometries=[];
  for(const viewport of [{width:1280,height:846},{width:1024,height:650},{width:834,height:1000},{width:390,height:700},{width:844,height:390}]){
   await page.setViewportSize(viewport);
   const g=await page.evaluate(()=>{const f=document.getElementById('format-code'),one=document.querySelector('#keyboard-main [data-value="1"]'),a=f.getBoundingClientRect(),b=one.getBoundingClientRect();return {left:a.left,right:a.right,oneLeft:b.left,top:a.top,oneTop:b.top,hit:document.elementFromPoint(a.x+a.width/2,a.y+a.height/2)?.closest('button')===f}});
   assert(g.left>=0&&g.right<=g.oneLeft&&Math.abs(g.top-g.oneTop)<1&&g.hit);geometries.push(viewport);count++;
  }
  await reset(ugly);await page.locator('#format-code').click();await page.waitForFunction(()=>!document.getElementById('format-code').disabled);assert.equal((await state()).code,formatted.code);count++;
  await page.screenshot({path:process.env.EDITOR_COMMAND_SCREENSHOT||path.join(tmp,'preview.png'),fullPage:false});
  if(!process.env.EDITOR_COMMAND_SCREENSHOT)fs.unlinkSync(path.join(tmp,'preview.png'));
  assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);console.log(JSON.stringify({commandChecks:count,buttonViewports:geometries,pageErrors:errors,externalRequests:requests}));
 }finally{await browser.close();fs.unlinkSync(file);fs.rmdirSync(tmp);}
})().catch(e=>{console.error(e);process.exit(1)});
