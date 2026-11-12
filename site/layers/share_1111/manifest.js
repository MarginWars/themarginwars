// Build the Pages direct-upload manifest the way wrangler does (blake3(base64 + ext) hex, first 32 chars).
const fs=require('fs'),path=require('path');const {hash}=require('/tmp/axe/node_modules/blake3-wasm/dist/node');
const root=process.argv[2],out={},meta={};const IGN=new Set(['_headers','_redirects','_routes.json','_worker.js','functions','.DS_Store','node_modules','.git']);
function walk(d){for(const f of fs.readdirSync(d)){const p=path.join(d,f),rel='/'+path.relative(root,p).split(path.sep).join('/');if(d===root&&IGN.has(f))continue;const s=fs.statSync(p);if(s.isDirectory())walk(p);else{const c=fs.readFileSync(p);const h=hash(c.toString('base64')+path.extname(p).substring(1)).toString('hex').slice(0,32);out[rel]=h;meta[h]={file:p,size:c.length}}}}
walk(root);fs.writeFileSync(process.argv[3],JSON.stringify({manifest:out,meta},null,0));console.log(Object.keys(out).length,'files',Object.keys(meta).length,'unique');
