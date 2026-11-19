import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const context={window:{}};vm.createContext(context);
vm.runInContext(fs.readFileSync('course-data.js','utf8'),context);
vm.runInContext(fs.readFileSync('resources.js','utf8'),context);
vm.runInContext(fs.readFileSync('document-library-manifest.js','utf8'),context);
const {CI_MODULES:m,CI_RESOURCES:d,CI_FORMS:f,CI_LOCAL_MANIFEST:man,CI_VIDEOS:v}=context.window;
assert.equal(m.length,11);assert.equal(m.reduce((x,y)=>x+y.hours,0),67);assert.equal(m.flatMap(x=>x.lessons).length,66);
assert.equal(new Set(m.flatMap(x=>x.lessons.map(l=>l.id))).size,66);
for(const x of m)for(const l of x.lessons){assert.ok(l.body.length>100);assert.equal(new Set([l.correct,...l.incorrect]).size,3);assert.ok(l.question)}
assert.equal(new Set(d.map(x=>x.id)).size,d.length);assert.equal(f.length,11);
for(const x of d)if(man[x.id]){assert.ok(fs.existsSync(x.local));assert.ok(fs.existsSync(x.cover));const h=(await import('node:crypto')).createHash('sha256').update(fs.readFileSync(x.local)).digest('hex');assert.equal(h,man[x.id].sha256)}
for(const x of Object.values(v))assert.match(x.id,/^[A-Za-z0-9_-]{11}$/);
for(const x of ['app.js','viewer.js','reader-adapter.js','service-worker.js'])new vm.Script(fs.readFileSync(x,'utf8'),{filename:x});
console.log(JSON.stringify({modules:m.length,lessons:66,formReferences:f.length,resources:d.length,prepared:Object.keys(man).length,videoCandidates:Object.keys(v).length,syntax:'PASS'}));
