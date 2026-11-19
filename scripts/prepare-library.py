#!/usr/bin/env python3
"""Prepare exact existing published HSTU reading copies, covers and hashes.
Only explicitly listed resources from the owner's existing public library are eligible.
No private curriculum, facilitator answer keys, or unapproved new sources are imported.
An institutional publication-rights/edition review remains required before formal rollout.
"""
import hashlib, json, pathlib, re, urllib.request, time
import fitz
ROOT=pathlib.Path(__file__).resolve().parents[1]
src=ROOT/"resources.js"
text=src.read_text()
rows=re.findall(r'\["([^"]+)","([^"]+)","([^"]+)","([^"]+)","([^"]+\.pdf)",true\]',text)
base="https://raw.githubusercontent.com/glenroygriffiths876-collab/HSTU-SI/main/documents/pdf-library/"
manifest={}
errors=[]
def fetch(url, path):
    path.parent.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(url,headers={"User-Agent":"CI-Academy-Document-Preparation"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=90) as r:
                content=r.read(150*1024*1024+1)
                if len(content)>150*1024*1024: raise ValueError("oversize")
            path.write_bytes(content)
            return
        except Exception:
            if attempt==2: raise
            time.sleep(2)
for key,title,year,category,filename in rows:
    target=ROOT/"documents/library"/filename
    try:
        if not target.exists(): fetch(base+filename,target)
        raw=target.read_bytes()
        if not raw.startswith(b"%PDF-"): raise ValueError("invalid PDF signature")
        with fitz.open(target) as doc:
            if not doc.page_count or doc.needs_pass: raise ValueError("empty or encrypted PDF")
            for i in sorted({0,doc.page_count//2,doc.page_count-1}):
                pix=doc[i].get_pixmap(matrix=fitz.Matrix(.25,.25),alpha=False)
                if not pix.width or not pix.height: raise ValueError("page render failed")
            cover=ROOT/"covers"/(key+".webp")
            cover.parent.mkdir(exist_ok=True)
            doc[0].get_pixmap(matrix=fitz.Matrix(.75,.75),alpha=False).pil_save(str(cover),format="WEBP",quality=88)
            manifest[key]={"sha256":hashlib.sha256(raw).hexdigest(),"bytes":len(raw),"pages":doc.page_count,"cover":True,"source":base+filename,"firstMiddleLastRasterized":True,"status":"Prepared exact existing published copy; institutional review pending"}
    except Exception as err:
        errors.append({"id":key,"title":title,"error":str(err)})
        if target.exists() and not target.read_bytes().startswith(b"%PDF-"):target.unlink()
for name in ["pdf.min.mjs","pdf.worker.min.mjs"]:
    try:
        fetch("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/"+name,ROOT/"vendor/pdfjs"/name)
    except Exception as err: errors.append({"id":name,"error":str(err)})
(ROOT/"document-library-manifest.js").write_text("window.CI_LOCAL_MANIFEST="+json.dumps(manifest,indent=2)+";\n")
(ROOT/"reports").mkdir(exist_ok=True)
(ROOT/"reports/library-preparation.json").write_text(json.dumps({"selected":len(rows),"prepared":len(manifest),"errors":errors,"scope":"PDF signatures, first/middle/last rasterization, hashes, original cover generation; not live-browser verification or publication clearance"},indent=2))
print(f"{len(manifest)} / {len(rows)} documents prepared; {len(errors)} issues")
if errors: print(json.dumps(errors,indent=2))
