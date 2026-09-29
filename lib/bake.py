import json,os,sys,concurrent.futures as cf
sys.path.insert(0,os.path.dirname(__file__)); from gen import gen
ROOT=os.path.join(os.path.dirname(__file__),".."); CAN=json.load(open(f"{ROOT}/product/red-bull-sugarfree.json"))["image"]
def build(key,sid):
    d=f"{ROOT}/styles/{key}"; st=json.load(open(f"{d}/style.json")); b=json.load(open(f"{d}/board.json")); wb=b.get("world_bible",{})
    s=[x for x in b["shots"] if x["id"]==sid][0]; refs=[];roles=[]
    for r in s.get("refs",[]):
        if r=="product": refs.append(CAN); roles.append(f"Image {len(refs)} is the product: reproduce this exact product, its shape, colours, label and logo, undistorted.")
        elif os.path.exists(f"{d}/img/{r}.png.url"):
            refs.append(open(f"{d}/img/{r}.png.url").read()); kind="character sheet" if any(c["id"]==r for c in b.get("cast",[])) else ("prop reference" if any(o["id"]==r for o in wb.get("signature_objects",[])) else "location reference")
            roles.append(f"Image {len(refs)} is the {kind} for {r}: keep identity and design consistent.")
    det=(" Specific details in this shot, spread across foreground, midground and background so the world feels lived in: "+"; ".join(s["dressing"])+".") if s.get("dressing") else ""
    mat=(" "+wb["materials_rule"]) if wb.get("materials_rule") else ""
    p=f"{st['prompt_prefix']} {s['keyframe_prompt']}{det}{mat} {' '.join(roles)} Avoid: {'; '.join(st.get('negatives',[]))}"
    return p,refs
jobs=[("cinematic","S02"),("cinematic","S06"),("claymation","S02"),("pixar3d","S06")]
def run(j):
    k,s=j; p,r=build(k,s); os.makedirs(f"{ROOT}/bake",exist_ok=True)
    try: return j,gen(p,r,f"{ROOT}/bake/{k}_{s}_gpt.png",size="9:16",model="gpt25",tag="bake")
    except Exception as e: return j,"ERR "+str(e)[:300]
with cf.ThreadPoolExecutor(4) as ex:
    for j,u in ex.map(run,jobs): print(j,u[:120])
