// Test hooks change inline scripts, so refresh their hashes in test fixtures only.
const {createHash}=require('node:crypto');
exports.refreshScriptHashes=function(source){
 source=source.replace(/\r\n?/g,'\n');
 const hashes=[...source.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)]
  .filter(m=>! /type=["']application\/json["']/.test(m[1]))
  .map(m=>"'sha256-"+createHash('sha256').update(m[2]).digest('base64')+"'");
 return source.replace(/(script-src )[^;]+;/,(_,prefix)=>prefix+hashes.join(' ')+" 'wasm-unsafe-eval';");
};
