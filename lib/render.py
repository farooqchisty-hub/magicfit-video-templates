"""Render assets + keyframes for one style board. python3 lib/render.py <style_key> [--only S03,S05] [--force]"""
import json,sys,os,concurrent.futures as cf
sys.path.insert(0,os.path.dirname(__file__)); from gen import gen
ROOT=os.path.join(os.path.dirname(__file__),"..")
CAN=json.load(open(f"{ROOT}/product/red-bull-sugarfree.json"))["image"]
def run(key,only=None,force=False):
    d=f"{ROOT}/styles/{key}"; st=json.load(open(f"{d}/style.json")); b=json.load(open(f"{d}/board.json"))
    os.makedirs(f"{d}/img",exist_ok=True)
    def g(prompt,refs,name,size="9:16"):
        out=f"{d}/img/{name}.png"
        if os.path.exists(out+".url") and not force: return name,open(out+".url").read()
        try: return name,gen(prompt,refs,out,size=size,tag=f"{key}/{name}")
        except Exception as e: return name,"ERR "+str(e)[:200]
    urls={}
    assets=[(c["card_prompt"]+" "+st.get("asset_style",""),[],c["id"],"16:9") for c in b.get("cast",[])]
    assets+=[(l["plate_prompt"],[],l["id"],"9:16") for l in b.get("locations",[])]
    with cf.ThreadPoolExecutor(8) as ex:
        for n,u in ex.map(lambda a:g(*a),assets): urls[n]=u; print(n,u[:60])
    neg="Avoid: "+"; ".join(st.get("negatives",[]))
    def kf(s):
        refs=[];roles=[]
        for r in s.get("refs",[]):
            if r=="product": refs.append(CAN); roles.append(f"Image {len(refs)} is the product: reproduce this exact product, its shape, colours, label and logo, undistorted.")
            elif r in urls and not urls[r].startswith("ERR"):
                refs.append(urls[r]); kind="character sheet" if any(c["id"]==r for c in b.get("cast",[])) else "location or prop reference"
                roles.append(f"Image {len(refs)} is the {kind} for {r}: keep identity and design consistent.")
        p=f"{st['prompt_prefix']} {s['keyframe_prompt']} {' '.join(roles)} {neg}"
        return g(p,refs,s["id"])
    shots=[s for s in b["shots"] if not only or s["id"] in only]
    with cf.ThreadPoolExecutor(10) as ex:
        for n,u in ex.map(kf,shots): print(n,u[:60])
if __name__=="__main__":
    only=None;force="--force" in sys.argv
    if "--only" in sys.argv: only=sys.argv[sys.argv.index("--only")+1].split(",")
    run(sys.argv[1],only,force)
