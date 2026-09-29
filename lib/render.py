"""Render assets + keyframes for one style board. python3 lib/render.py <style_key> [--only S03,S05] [--force]"""
import json,sys,os,concurrent.futures as cf
sys.path.insert(0,os.path.dirname(__file__)); from gen import gen
ROOT=os.path.join(os.path.dirname(__file__),"..")
CAN=json.load(open(f"{ROOT}/product/red-bull-sugarfree.json"))["image"]
def run(key,only=None,force=False):
    d=f"{ROOT}/styles/{key}"; st=json.load(open(f"{d}/style.json")); b=json.load(open(f"{d}/board.json"))
    os.makedirs(f"{d}/img",exist_ok=True)
    def g(prompt,refs,name,size="9:16",asset=False):
        out=f"{d}/img/{name}.png"
        if os.path.exists(out+".url") and not (force and (not only or name in only)): return name,open(out+".url").read()
        try: return name,gen(prompt,refs,out,size=size,tag=f"{key}/{name}")
        except Exception as e: return name,"ERR "+str(e)[:200]
    urls={}
    assets=[(c["card_prompt"]+" "+st.get("asset_style",""),[],c["id"],"16:9",True) for c in b.get("cast",[])]
    wb=b.get("world_bible",{})
    def dress(loc):
        L=wb.get("locations",{}).get(loc)
        if not L: return ""
        return " Set dressing, foreground: "+"; ".join(L.get("foreground",[]))+". Midground: "+"; ".join(L.get("midground",[]))+". Background: "+"; ".join(L.get("background",[]))+"."
    mat=(" "+wb["materials_rule"]) if wb.get("materials_rule") else ""
    assets+=[(l["plate_prompt"]+dress(l["id"])+mat,[],l["id"],"9:16",True) for l in b.get("locations",[])]
    assets+=[(o["prop_prompt"]+mat,[],o["id"],"16:9",True) for o in wb.get("signature_objects",[])]
    with cf.ThreadPoolExecutor(4) as ex:
        for n,u in ex.map(lambda a:g(*a),assets): urls[n]=u; print(n,u[:60])
    neg="Avoid: "+"; ".join(st.get("negatives",[]))
    def kf(s):
        refs=[];roles=[]
        for r in s.get("refs",[]):
            if r=="product": refs.append(CAN); roles.append(f"Image {len(refs)} is the product: reproduce this exact product, its shape, colours, label and logo, undistorted.")
            elif r in urls and not urls[r].startswith("ERR"):
                refs.append(urls[r]); kind="character sheet" if any(c["id"]==r for c in b.get("cast",[])) else ("prop reference" if any(o["id"]==r for o in wb.get("signature_objects",[])) else "location reference")
                roles.append(f"Image {len(refs)} is the {kind} for {r}: keep identity and design consistent.")
        det=""
        if s.get("dressing"): det=" Specific details in this shot, spread across foreground, midground and background so the world feels lived in: "+"; ".join(s["dressing"])+"."
        p=f"{st['prompt_prefix']} {s['keyframe_prompt']}{det}{mat} {' '.join(roles)} {neg}"
        return g(p,refs,s["id"])
    shots=[s for s in b["shots"] if not only or s["id"] in only]
    with cf.ThreadPoolExecutor(5) as ex:
        for n,u in ex.map(kf,shots): print(n,u[:60])
if __name__=="__main__":
    only=None;force="--force" in sys.argv
    if "--only" in sys.argv: only=sys.argv[sys.argv.index("--only")+1].split(",")
    run(sys.argv[1],only,force)
