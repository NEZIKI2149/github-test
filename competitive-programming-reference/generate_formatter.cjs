// Build a self-contained browser formatter from the pinned upstream distribution.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const root=__dirname,vendor=path.join(root,'vendor','clang-format');
const provenance=JSON.parse(fs.readFileSync(path.join(vendor,'provenance.json'),'utf8'));
for(const [name,expected] of Object.entries(provenance.files)){
 const actual=crypto.createHash('sha256').update(fs.readFileSync(path.join(vendor,name))).digest('hex');
 if(actual!==expected)throw Error('Vendor hash mismatch: '+name);
}
const moduleSource=fs.readFileSync(path.join(vendor,'clang-format.js'),'utf8').replace(/^export /gm,'');
const binding=fs.readFileSync(path.join(vendor,'clang-format-binding.js'),'utf8').replace(/^export /gm,'');
const binary=fs.readFileSync(path.join(vendor,'clang-format.wasm')).toString('base64');
const runtime=`// @wasm-fmt/clang-format ${provenance.version}; licenses: vendor/clang-format/\n`+
`(()=>{'use strict';\n${moduleSource}\n${binding}\n`+
`let initializing;window.loadCppFormatter=function(){\n`+
`if(!initializing)initializing=(async()=>{const binary=atob(${JSON.stringify(binary)});\n`+
`const module=await WebAssembly.compile(Uint8Array.from(binary,c=>c.charCodeAt(0)).buffer);\n`+
`set_wasm(createModule({wasm:module}));return {format,version};\n`+
`})().catch(error=>{initializing=null;throw error;});return initializing;};})();\n`;
if(/<\/script/i.test(runtime))throw Error('Unexpected script close');
const file=path.join(root,'mobile-editor.html');
let page=fs.readFileSync(file,'utf8').replace(/\r\n/g,'\n').replace(/<script id="cpp-formatter-engine">[\s\S]*?<\/script>\n/,'');
page=page.replace('<script>\n',()=>'<script id="cpp-formatter-engine">\n'+runtime+'</script>\n<script>\n');
fs.writeFileSync(file,page);
console.log('Embedded offline clang-format '+provenance.version);
