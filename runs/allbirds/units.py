import json,sys,os,re,subprocess,concurrent.futures as cf
T="../../bundle/templates/anime-01-rookie-arc"; t=json.load(open(f"{T}/template.json")); U=t["asset_urls"]
f=json.load(open("fill.json")); card=f["product"]
def k(s): return open(f"keyframes/{s}.png.url").read()
plan={"U1":[U["dax"],U["mika"],U["bowl"],k("S01"),k("S02")],
      "U2":[card["image"],U["mika"],k("S04"),k("S05"),k("S06")],
      "U3":[U["mika"],U["dax"],U["bowl"],card["image"],k("S07"),k("S10")],
      "U4":[card["image"],k("S11")]}
extra={"U1":" [Image3] is the skate bowl. [Image4] and [Image5] are storyboard frames for the first shots: match their composition and anime style.",
 "U2":" [Image3], [Image4] and [Image5] are the storyboard frames for these shots in order: match their composition, with the sneakers exactly like [Image1] (black knit upper, black laces, thick rounded white sole).",
 "U3":" [Image3] is the skate bowl. Throughout this unit Mika wears the black knit sneakers with thick white soles from [Image4] on her feet. [Image5] and [Image6] are storyboard frames: match their composition.",
 "U4":" [Image2] is the storyboard frame: match its composition. Two sneakers side by side, exactly like [Image1]."}
lens={u["id"]:u["len_s"] for u in t["units"]}
only=sys.argv[1:] or list(plan)
def go(uid):
    p=re.sub(r"@Image(\d)",r"[Image\1]",f["unit_prompts"][uid])+extra[uid]
    r=subprocess.run(["python3","../../testkit/videogen.py","--out",f"units/{uid}.mp4","--duration",str(lens[uid]),"--prompt",p,"--tag",f"allbirds/{uid}"]+sum([["--ref",x] for x in plan[uid]],[]),capture_output=True,text=True)
    return uid,(r.stdout+r.stderr).strip()[-300:]
with cf.ThreadPoolExecutor(4) as ex:
    for u,o in ex.map(go,only): print(u,o)
