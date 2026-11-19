import {chromium} from 'playwright';
import fs from 'node:fs';
const start=process.env.CI_BASE||'http://127.0.0.1:8080/';
const browser=await chromium.launch({headless:true});
const out=[];
for(const width of [390,768,1440]){
 const ctx=await browser.newContext({viewport:{width,height:900},serviceWorkers:'block'});const p=await ctx.newPage();const err=[];p.on('pageerror',e=>err.push(e.message));
 try{
 await p.goto(start,{waitUntil:'domcontentloaded'});await p.getByText('Investigate.',{exact:false}).first().waitFor();await p.locator('button[data-go="lesson:1.1"]').first().click();await p.locator('#lesson-question button').first().click();await p.locator('#complete').click();await p.reload();await p.getByRole('button',{name:'✓ Completed'}).waitFor();
 await p.goto(start+'#forms');await p.locator('#form-choice').waitFor();await p.goto(start+'#practice');await p.locator('#cascade-result').waitFor();await p.goto(start+'#certificate');await p.locator('#cert-display').waitFor();
 const overflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);if(overflow)throw Error('Horizontal overflow');if(err.length)throw Error(err.join('; '));out.push({width,status:'pass'})
 }catch(e){out.push({width,status:'fail',error:e.message,errors:err})}await ctx.close();
}
const ctx=await browser.newContext({viewport:{width:1280,height:900},serviceWorkers:'block'}),p=await ctx.newPage();
await p.goto(start+'#library');await p.locator('#books').waitFor();
const docs=await p.evaluate(()=>window.CI_RESOURCES.filter(x=>window.CI_LOCAL_MANIFEST[x.id]).map(x=>({id:x.id,title:x.title})));
for(const d of docs){try{await p.locator('[data-doc="'+d.id+'"]').first().click();await p.locator('#pdfPageSurface canvas').first().waitFor({timeout:35000});out.push({id:d.id,status:'first-page-rendered'});await p.locator('#closePdf').click();await p.locator('#pdfDialog').waitFor({state:'hidden'})}catch(e){out.push({id:d.id,status:'fail',error:e.message});if(await p.locator('#pdfDialog').isVisible())await p.locator('#closePdf').click().catch(()=>{})}}
await browser.close();fs.mkdirSync('reports',{recursive:true});fs.writeFileSync('reports/browser-checks.json',JSON.stringify(out,null,2));console.log(out);if(out.some(x=>x.status==='fail'))process.exitCode=1;
