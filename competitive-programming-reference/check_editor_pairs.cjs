const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),assert=require('node:assert/strict');
const {pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_PATH||'playwright');
(async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'neziki-pairs-test-')),file=path.join(tmp,'editor.html');
 const source=fs.readFileSync(path.join(__dirname,'mobile-editor.html'),'utf8').replace(/\r\n/g,'\n');
 const hook=`
 window.__pairsTest={reset:(text,a=text.length,h=a)=>{stopRepeat();code=text;anchor=a;head=h;autoPairs=[];undo.length=redo.length=0;stopUndoGroup();ctrl=false;shift=0;render();},
 type:t=>insert(t,'type'),enter,backspace,history,paste:t=>replace(t,undefined,undefined,'paste'),
 caret:p=>{stopUndoGroup();anchor=head=p;render();},state:()=>({code,anchor,head,pairs:autoPairs.map(p=>({...p}))})};
 render();
 })();`;
 assert(source.includes('\nrender();\n})();'));
 fs.writeFileSync(file,source.replace('\nrender();\n})();',hook));
 const browser=await chromium.launch({headless:true,...(process.env.BROWSER_CHANNEL?{channel:process.env.BROWSER_CHANNEL}:{})});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:846}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(file).href);await page.evaluate(()=>window.vscodeCppHighlighter);
  const call=(name,...args)=>page.evaluate(({name,args})=>window.__pairsTest[name](...args),{name,args});
  const state=()=>call('state'),reset=(...args)=>call('reset',...args),type=t=>call('type',t);
  let count=0;
  async function expect(text,anchor,head=anchor){const actual=await state();assert.equal(actual.code,text);assert.equal(actual.anchor,anchor);assert.equal(actual.head,head);count++;}
  for(const [open,close] of [['(',')'],['[',']'],['{','}'],['"','"'],["'","'"]]){
   await reset('');await type(open);await expect(open+close,1);assert.equal((await state()).pairs.length,1);
   await type(close);await expect(open+close,2);assert.equal((await state()).pairs.length,0);
   await reset('');await type(open);await call('backspace');await expect('',0);
   await call('history',false);await expect(open+close,1);await call('backspace');await expect('',0);
  }
  await reset('f');for(const c of ['(','[','1',']',')'])await type(c);await expect('f([1])',6);
  await reset('foo',0);await type('(');await expect('(foo',1);
  await reset('1');await type("'");await expect("1'",2);assert.equal((await state()).pairs.length,0);
  await reset('// comment ');await type("'");await expect("// comment '",12);
  await reset('// ');await type('"');await expect('// ""',4);
  await reset('"abc"',2);await type('"');await expect('"a"bc"',3);
  await reset('');await type('"');await type('\\');await type('"');await expect(String.raw`"\""`,3);await type('"');await expect(String.raw`"\""`,4);
  const prefix='    if (ok) ';
  await reset(prefix);await type('{');await call('enter');await expect(prefix+'{\n        \n    }',prefix.length+10);
  await call('history',false);await expect(prefix+'{}',prefix.length+1);
  await call('history',true);await expect(prefix+'{\n        \n    }',prefix.length+10);
  await type('x');await expect(prefix+'{\n        x\n    }',prefix.length+11);
  await reset('{}',1);await call('enter');await expect('{\n    \n}',6);
  await reset('call()',5);await call('enter');await expect('call(\n    \n)',10);
  await reset('    x');await call('enter');await expect('    x\n    ',10);
  await reset('"{"',2);await call('enter');await expect('"{\n"',3);
  await reset('// {');await call('enter');await expect('// {\n',5);
  await reset('() ',1);await call('backspace');await expect(') ',0);
  await reset('');await call('paste','()');await call('backspace');await expect('(',1);
  await reset('foo',0,3);await type('(');await expect('(foo)',1,4);
  await call('history',false);await expect('foo',0,3);await call('history',true);await expect('(foo)',1,4);
  await reset('foo',3,0);await type('[');await expect('[foo]',4,1);
  await reset('');await type('(');await call('caret',0);await type('x');await call('caret',2);await call('backspace');await expect('x',1);
  await reset('');await type('{');await call('enter');await type('(');await type('x');await type(')');await expect('{\n    (x)\n}',9);
  await reset('');await type('(');await page.reload();await page.evaluate(()=>window.vscodeCppHighlighter);await call('backspace');await expect('',0);
  // Exercise the actual JIS Shift+8/9 buttons as well as the editing functions.
  await reset('');await page.locator('#keyboard-main [data-op="shift"]').click();await page.locator('#keyboard-main [data-value="8"]').click();await expect('()',1);
  await page.locator('#keyboard-main [data-op="shift"]').click();await page.locator('#keyboard-main [data-value="9"]').click();await expect('()',2);
  assert.deepEqual(errors,[]);console.log(JSON.stringify({pairAndIndentChecks:count,pageErrors:errors}));
 }finally{await browser.close();fs.unlinkSync(file);fs.rmdirSync(tmp);}
})().catch(e=>{console.error(e);process.exit(1)});
