// Build-time only: use the installed VS Code C++ grammar and TextMate engine.
// Set VSCODE_APP to a VS Code resources/app directory on other installations.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

function vscodeApp() {
    if (process.env.VSCODE_APP) return process.env.VSCODE_APP;
    const base = path.join(process.env.LOCALAPPDATA || '', 'Programs', 'Microsoft VS Code');
    const candidates = [path.join(base, 'resources', 'app')];
    if (fs.existsSync(base)) {
        for (const dir of fs.readdirSync(base)) candidates.push(path.join(base, dir, 'resources', 'app'));
    }
    const found = candidates.find(p => fs.existsSync(path.join(p, 'extensions', 'cpp', 'syntaxes', 'cpp.tmLanguage.json')));
    if (!found) throw new Error('Set VSCODE_APP to the installed VS Code resources/app directory.');
    return found;
}

const app = vscodeApp();
let archive;
let header;
let contentOffset;
function bundledSource(name) {
    const normal = path.join(app, 'node_modules', name, 'release', 'main.js');
    if (fs.existsSync(normal)) return fs.readFileSync(normal, 'utf8');
    if (!archive) {
        archive = fs.readFileSync(path.join(app, 'node_modules.asar'));
        header = JSON.parse(archive.subarray(16, 16 + archive.readUInt32LE(12)).toString());
        contentOffset = 8 + archive.readUInt32LE(4);
    }
    let entry = header;
    for (const part of [name, 'release', 'main.js']) entry = entry.files[part];
    const start = contentOffset + Number(entry.offset);
    return archive.subarray(start, start + entry.size).toString();
}
function bundledModule(name) {
    const module = {exports: {}};
    new Function('module', 'exports', 'require', bundledSource(name))(module, module.exports, require);
    return module.exports;
}

async function main() {
    const textmate = bundledModule('vscode-textmate');
    const oniguruma = bundledModule('vscode-oniguruma');
    const wasmPaths = ['node_modules', 'node_modules.asar.unpacked'].map(p => path.join(app, p, 'vscode-oniguruma', 'release', 'onig.wasm'));
    await oniguruma.loadWASM(fs.readFileSync(wasmPaths.find(p => fs.existsSync(p))));
    const theme = JSON.parse(fs.readFileSync(path.join(__dirname, 'vscode-code-theme.json'), 'utf8'));
    const grammars = new Map();
    const syntax = path.join(app, 'extensions', 'cpp', 'syntaxes');
    for (const name of fs.readdirSync(syntax).filter(n => n.endsWith('.json'))) {
        const grammar = textmate.parseRawGrammar(fs.readFileSync(path.join(syntax, name), 'utf8'), name);
        grammars.set(grammar.scopeName, grammar);
    }
    const registry = new textmate.Registry({
        theme,
        onigLib: Promise.resolve({createOnigScanner: patterns => new oniguruma.OnigScanner(patterns), createOnigString: s => new oniguruma.OnigString(s)}),
        loadGrammar: async scope => grammars.get(scope) || null
    });
    const grammar = await registry.loadGrammar('source.cpp');
    const colors = registry.getColorMap();
    const escape = s => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
    function highlight(source) {
        let state = textmate.INITIAL;
        const html = source.split('\n').map(line => {
            const result = grammar.tokenizeLine2(line, state);
            state = result.ruleStack;
            let out = '';
            for (let i = 0; i < result.tokens.length; i += 2) {
                const start = result.tokens[i], end = Math.min(line.length, result.tokens[i + 2] ?? line.length);
                if (start >= end) continue;
                const metadata = result.tokens[i + 1];
                const color = colors[(metadata >>> 15) & 511];
                const font = (metadata >>> 11) & 15;
                const style = `color:${color}` + ((font & 1) ? ';font-style:italic' : '') + ((font & 2) ? ';font-weight:bold' : '') + ((font & 4) ? ';text-decoration:underline' : '');
                out += '<span style="' + style + '">' + escape(line.slice(start, end)) + '</span>';
            }
            return out;
        }).join('\n');
        return {sha256: crypto.createHash('sha256').update(source).digest('hex'), html};
    }
    const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'reference-data.json'), 'utf8'));
    const items = {};
    for (const group of data.groups) for (const item of group.items) {
        items[item.id] = {full: highlight(item.full), code: highlight(item.code)};
    }
    fs.writeFileSync(path.join(__dirname, 'syntax-highlighting.json'), JSON.stringify({theme: theme.name, background: theme.colors['editor.background'], foreground: theme.colors['editor.foreground'], items}) + '\n');
    // Embed the same engine for arbitrary text typed in the offline mobile editor.
    const runtime = `"use strict";\n// Bundled VS Code TextMate/Oniguruma: see syntax-NOTICES.txt.\n` +
        `const vscodeTextmate=(()=>{const module={exports:{}};const exports=module.exports;${bundledSource('vscode-textmate')}\nreturn module.exports;})();\n` +
        `const vscodeOniguruma=(()=>{const module={exports:{}};const exports=module.exports;${bundledSource('vscode-oniguruma')}\nreturn module.exports;})();\n` +
        `window.vscodeCppHighlighter=(async()=>{\n` +
        `const binary=atob(${JSON.stringify(fs.readFileSync(wasmPaths.find(p => fs.existsSync(p))).toString('base64'))});\n` +
        `await vscodeOniguruma.loadWASM(Uint8Array.from(binary,c=>c.charCodeAt(0)).buffer);\n` +
        `const grammars=${JSON.stringify(Object.fromEntries(grammars))};\n` +
        `const registry=new vscodeTextmate.Registry({theme:${JSON.stringify(theme)},onigLib:Promise.resolve({createOnigScanner:p=>new vscodeOniguruma.OnigScanner(p),createOnigString:s=>new vscodeOniguruma.OnigString(s)}),loadGrammar:async s=>grammars[s]||null});\n` +
        `const grammar=await registry.loadGrammar('source.cpp'),colors=registry.getColorMap();\n` +
        `return source=>{const tokens=[];let state=vscodeTextmate.INITIAL;const lines=source.split('\\n');\n` +
        `for(let n=0;n<lines.length;n++){const line=lines[n],result=grammar.tokenizeLine2(line,state);state=result.ruleStack;\n` +
        `for(let i=0;i<result.tokens.length;i+=2){const start=result.tokens[i],end=Math.min(line.length,result.tokens[i+2]??line.length),m=result.tokens[i+1];if(start<end)tokens.push({value:line.slice(start,end),color:colors[(m>>>15)&511],font:(m>>>11)&15});}\n` +
        `if(n<lines.length-1)tokens.push({value:'\\n'});}return tokens;};})();\n`;
    if (/<\/script/i.test(runtime)) throw new Error('Unexpected script close in bundled runtime');
    const mobile = path.join(__dirname, 'mobile-editor.html');
    let editor = fs.readFileSync(mobile, 'utf8').replace(/\r\n/g, '\n').replace(/<script id="vscode-cpp-engine">[\s\S]*?<\/script>\n/, '');
    editor = editor.replace('<script>\n', () => '<script id="vscode-cpp-engine">\n' + runtime + '</script>\n<script>\n');
    fs.writeFileSync(mobile, editor);
    console.log(`Highlighted ${Object.keys(items).length} examples with VS Code ${theme.name} and its C++ TextMate grammar.`);
}
main().catch(error => {console.error(error); process.exitCode = 1;});
