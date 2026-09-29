import json,sys,os,re,subprocess,concurrent.futures as cf
T="../../bundle/templates/pixar3d-01-night-owl"; t=json.load(open(f"{T}/template.json")); U=t["asset_urls"]
f=json.load(open("fill.json")); card=f["product"]
def kfu(s):
    p=f"keyframes/{s}.png.url"
    return open(p).read() if os.path.exists(p) else open(f"../../styles/pixar3d/img/{s}.png.url").read()
plan={"U1":[U["mabel"],U["teo"],U["lamp_room"],U["lighthouse"],kfu("S01"),kfu("S03")],
      "U2":[card["image"],U["mabel"],kfu("S05"),kfu("S06")],
      "U3":[U["mabel"],U["lamp_room"],U["lighthouse"],U["ferry"],kfu("S07"),kfu("S08")],
      "U4":[card["image"],U["mabel"],kfu("S10")]}
extra={"U1":" [Image3] is the lamp room and [Image4] the lighthouse exterior. [Image5] and [Image6] are storyboard frames for shots 1 and 3: match their composition and look.",
 "U2":" [Image3] and [Image4] are the storyboard frames for shots 1 and 2: match their composition, with the product at the size shown there.",
 "U3":" [Image2] is the lamp room, [Image3] the lighthouse and [Image4] the ferry. [Image5] and [Image6] are storyboard frames for shots 1 and 2.",
 "U4":" [Image3] is the storyboard frame: match its composition."}
lens={u["id"]:u["len_s"] for u in t["units"]}
only=sys.argv[1:] or list(plan)
def go(uid):
    p=re.sub(r"@Image(\d)",r"[Image\1]",f["unit_prompts"][uid])+extra[uid]
    r=subprocess.run(["python3","../../testkit/videogen.py","--out",f"units/{uid}.mp4","--duration",str(lens[uid]),"--prompt",p,"--tag",f"balm/{uid}"]+sum([["--ref",x] for x in plan[uid]],[]),capture_output=True,text=True)
    return uid,(r.stdout+r.stderr).strip()[-300:]
with cf.ThreadPoolExecutor(4) as ex:
    for u,o in ex.map(go,only): print(u,o)
