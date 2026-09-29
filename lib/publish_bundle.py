"""Stamp asset_urls into every template, write bundle/manifest.json, mirror bundle to docs/bundle (public)."""
import json,glob,os,shutil
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
BASE="https://farooqchisty-hub.github.io/magicfit-video-templates/bundle"
man=[]
for f in sorted(glob.glob(f"{ROOT}/bundle/templates/*/template.json")):
    d=os.path.dirname(f); tid=os.path.basename(d); t=json.load(open(f))
    urls={}
    for grp in [t.get("cast",[]),t.get("locations",[]),t.get("world_bible",{}).get("signature_objects",[])]:
        for x in grp:
            if x.get("asset"): urls[x["id"]]=f"{BASE}/templates/{tid}/{x['asset']}"
    t["asset_urls"]=urls; json.dump(t,open(f,"w"),indent=2)
    st=json.load(open(f"{d}/style.json"))
    man.append({"id":tid,"style":t["style"],"style_name":st.get("name"),"title":t["title"],"logline":t["logline"],"fit":{k:v[0] if isinstance(v,list) else v for k,v in t.get("fit",{}).get("archetypes",{}).items()},"avoid":t.get("fit",{}).get("avoid",[])})
json.dump({"version":"1.0","templates":man},open(f"{ROOT}/bundle/manifest.json","w"),indent=2)
dst=f"{ROOT}/docs/bundle"
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(f"{ROOT}/bundle",dst)
open(f"{dst}/.nojekyll","w").write("")
print(len(man),"templates published")
