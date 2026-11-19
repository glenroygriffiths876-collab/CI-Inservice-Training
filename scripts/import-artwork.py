#!/usr/bin/env python3
"""One-time import of original user-generated CI/DIO illustrations from signed Canva delivery URLs.
These signed preview URLs are temporary. The workflow commits permanent optimised copies locally.
The module tiles use these assets; full-resolution hero imagery remains in the repository until confirmed.
"""
from PIL import Image,ImageEnhance,ImageFilter
from pathlib import Path
import json, requests, re, io, os, sys
items=[{"name":"clinic-interview","canva_id":"MAHbZ_6TnZs","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fd8114177-00ab-49d8-b9ad-60b6dbcb3c33/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAJhHEfyhrkIYUvWsB8DDK03BvXe6yO3iM3vTFLQ2moH8&exp=1795146127&osig=AAAAAAAAAAAAAAAAAAAAABssrUJ6zTDlml3dC3UhWlAaqjM_pB8Zg49pijrM_CMe&signer=media-rpc&token=AAIAAU0AJGQ4MTE0MTc3LTAwYWItNDlkOC1iOWFkLTYwYjZkYmNiM2MzMwAAAAABofcMFpgm2ET33Au05IxQvXoBIRhL-WMlkhxA9qXo6P1VBLjfdQ&x-canva-quality=thumbnail"},{"name":"clinic-records","canva_id":"MAHbZ_FM0es","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2F1075f31a-bcd2-41b7-8969-11a7f6a3ecc9/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAFHpz41LIJVtPpbbY5gnsCWwD_QXKjhfogOLZ4XhMRXP&exp=1795145293&osig=AAAAAAAAAAAAAAAAAAAAAAbfsGCtyW4kCVU8CY3ByaL6F2AZXmVbpZIfA5iRKE-i&signer=media-rpc&token=AAIAAU0AJDEwNzVmMzFhLWJjZDItNDFiNy04OTY5LTExYTdmNmEzZWNjOQAAAAABofb_XMgwcyXFvJm-x_P8r_7oU19KIGVPyUUY8w0U03mbVCsIug&x-canva-quality=thumbnail"},{"name":"team-surveillance","canva_id":"MAHbZ3Q6AL4","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fa9308a86-6c03-407b-99ae-6721303d0683/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAArmcQHtACSdlur3Dr0wx7G-ZaW7Vz7eZpsWyE57t9um&exp=1795146705&osig=AAAAAAAAAAAAAAAAAAAAADe0621H_gJzsDymhdZTpiLmJGeMbAHezqsVikTsx29_&signer=media-rpc&token=AAIAAU0AJGE5MzA4YTg2LTZjMDMtNDA3Yi05OWFlLTY3MjEzMDNkMDY4MwAAAAABofcU6Gi10g987MSCG5yD8CA9DEtOre2eNWWjNa9NUyrPGFxCtA&x-canva-quality=thumbnail"},{"name":"community-fieldwork","canva_id":"MAHbZ3d1vjQ","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fa7f3f321-8b5c-49df-a2a5-729aa8d77849/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAFYibpb6ZDx_PzOZ7vXbIPOa8p0K_eYpKS0Kp8chmpvd&exp=1795146961&osig=AAAAAAAAAAAAAAAAAAAAACl9LrYry7iP-XS4S5NuwRQkcVmJRGmcxpmonCd9l_CO&signer=media-rpc&token=AAIAAU0AJGE3ZjNmMzIxLThiNWMtNDlkZi1hMmE1LTcyOWFhOGQ3Nzg0OQAAAAABofcY0GgGt-i4Jnyjzkl9nEMfOuxKafjQ87wP5cSrCaPGCizhnw&x-canva-quality=thumbnail"},{"name":"outbreak-review","canva_id":"MAHbZ_yWNuw","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2F64f6751e-1c77-423a-b835-4606b5bfd640/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAADwqU4J0kn9hZxmEIbkSFxqkZ6A2cdRGuXSlUpP_cTCf&exp=1795145556&osig=AAAAAAAAAAAAAAAAAAAAAFVeUalJFc_b_QAjfgXr0JHUQ4bmTjDBIS3iFaIf3Bsk&signer=media-rpc&token=AAIAAU0AJDY0ZjY3NTFlLTFjNzctNDIzYS1iODM1LTQ2MDZiNWJmZDY0MAAAAAABofcDYCDADFob0qZkwu3oJ1A0otWy33aOa9BmZKY309PF8ZJhuw&x-canva-quality=thumbnail"},{"name":"family-support","canva_id":"MAHbZ3YfZ88","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fab01b98b-5cb5-4c22-a806-e956bb85ef18/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAMnAq_2waNtDPdCgjC6JozOxP3ZMfYsYuKXh38ItlOPH&exp=1795145677&osig=AAAAAAAAAAAAAAAAAAAAAI9UPNnXdaNiod19rTRzGjcEBSRwDTKJf-dczaT1TcJ-&signer=media-rpc&token=AAIAAU0AJGFiMDFiOThiLTVjYjUtNGMyMi1hODA2LWU5NTZiYjg1ZWYxOAAAAAABofcFOMjdJ-lfHJ6mJYRZa-Ws4XTSulp2XhNKEd_ECqCwd8vyOg&x-canva-quality=thumbnail"},{"name":"confidential-counselling","canva_id":"MAHbZwW6abk","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fb196c3dc-8398-402d-afe4-41987d143903/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAIFKa-UG4T4NkL1wd3Y3HHANlpMn-6LcrqV2N58ycIcN&exp=1795146868&osig=AAAAAAAAAAAAAAAAAAAAAEGj4CbT_eD_SQLftyVLA7-TFZ5OKL9UxRg0XwGYj_xF&signer=media-rpc&token=AAIAAU0AJGIxOTZjM2RjLTgzOTgtNDAyZC1hZmU0LTQxOTg3ZDE0MzkwMwAAAAABofcXZSAMvLuZxxAYFsfGsxwjwv66MHlMSEOPdc7ykPX2yICxfg&x-canva-quality=thumbnail"},{"name":"supervision","canva_id":"MAHbZ4MgSWs","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fcf0ce693-2aa9-4577-b095-65c19128ce0d/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAABDefikZ3Pm3v83vNkGPCiagTBhL68RkIRYeo1l5Ldyc&exp=1795145624&osig=AAAAAAAAAAAAAAAAAAAAAGBbAhdAvyTySGG_dKwoQVLZpaWiGR1J49QNn6UmhhLQ&signer=media-rpc&token=AAIAAU0AJGNmMGNlNjkzLTJhYTktNDU3Ny1iMDk1LTY1YzE5MTI4Y2UwZAAAAAABofcEacC4Okid8nAloGPqH8PZLw-lL7dpBmCuQXpLH3foW8xhKw&x-canva-quality=thumbnail"},{"name":"e-learning","canva_id":"MAHbZ1-X_jM","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2F428be86f-a6ae-49eb-8bce-f0270a42fff0/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAGOHRDCyHdC27HAJU0vCVWqz45DM7si128Nl4GyQXt0I&exp=1795145695&osig=AAAAAAAAAAAAAAAAAAAAANnAM4gVCilp15gZIgctpJG_03Hcz_Tbn3NRuDogx8Po&signer=media-rpc&token=AAIAAU0AJDQyOGJlODZmLWE2YWUtNDllYi04YmNlLWYwMjcwYTQyZmZmMAAAAAABofcFfxhma8GOlz6DVHH6_corMxSBizoH5Jm0ZWm2EKGyzmlmjg&x-canva-quality=thumbnail"},{"name":"professional-team","canva_id":"MAHbZ_rlRmQ","url":"https://media.canva.com/v2/image-resize/format:PNG/height:112/quality:100/uri:ifs%3A%2F%2FM%2Fa527cb73-4f29-4b5d-b000-cd5643bda5e3/watermark:F/width:200?csig=AAAAAAAAAAAAAAAAAAAAAGiGFSHLGzMxGbpZlNQHXhzuOt4bUfhM6Oe_Qu3in7cR&exp=1795147572&osig=AAAAAAAAAAAAAAAAAAAAANJs-4liY0zziFC9nTCqonBV8cYzZb9qojfYDiGRQ9fp&signer=media-rpc&token=AAIAAU0AJGE1MjdjYjczLTRmMjktNGI1ZC1iMDAwLWNkNTY0M2JkYTVlMwAAAAABofciIyBKxSj6o-fXdeuMXtim_UwrZboMPTOgZEtVzdwCJh5Hvw&x-canva-quality=thumbnail"}]
root=Path(__file__).resolve().parents[1]
out=root/"assets"/"original-art"
out.mkdir(parents=True,exist_ok=True)
log=[]
names={}
for item in items:
    name,url=item["name"],item["url"]
    candidates=[re.sub(r"width:200", "width:1280", re.sub(r"height:112","height:720",url)),url]
    images=[]
    for variant in candidates:
        try:
            r=requests.get(variant,timeout=25,headers={"User-Agent":"Mozilla/5.0","Accept":"image/*"})
            r.raise_for_status()
            im=Image.open(io.BytesIO(r.content)).convert("RGB")
            if im.width>=150 and im.height>=80:images.append(im)
        except Exception:pass
    if images:
        im=max(images,key=lambda x:x.width*x.height)
        if im.width<720:
            # Preview-quality source: preserve a sensible ~400px module-card presentation.
            im=im.resize((800,450),Image.Resampling.LANCZOS)
            im=im.filter(ImageFilter.UnsharpMask(radius=1.1,percent=105,threshold=2))
        im.save(out/(name+".webp"),"WEBP",quality=86,method=6)
        names[name]={"image":"assets/original-art/"+name+".webp","sourceSize":(im.width,im.height)}
        log.append({"name":name,"status":"imported","size":list(im.size),"source":"user-generated Canva asset"})
    else:log.append({"name":name,"status":"unavailable"})
module_images={1:"clinic-interview",2:"outbreak-review",3:"confidential-counselling",4:"family-support",5:"clinic-records",6:"community-fieldwork",7:"professional-team",8:"team-surveillance",9:"e-learning",10:"community-fieldwork",11:"supervision"}
thumb={str(m):names[name]["image"] for m,name in module_images.items() if name in names}
(root/"artwork-thumbnails.js").write_text("window.CI_ART_THUMBNAILS="+json.dumps(thumb,sort_keys=True)+";\n")
(root/"reports").mkdir(exist_ok=True)
(root/"reports"/"illustration-import.json").write_text(json.dumps(log,indent=2))
print(json.dumps({"imported":len(names),"mapped":len(thumb),"source":"original generated Canva artwork","note":"some assets may be 200px previews upscaled; source resolution recorded in report"},indent=2))
if len(names)==0:sys.exit(1)
