"""Lint a template dir against TEMPLATE_SPEC.md. Prints PASS or the problems."""
import json,re,sys,os
ARCH=["ingested","applied","worn","handheld","carried","home","consumable"]
CARD={"product.name","product.brand","product.phonetic","product.short_name","product.visual","product.archetype","product.scale","product.benefits","product.tagline","product.use_moments","product.tagline_or_line.L7"}
BANNED=re.compile(r"\b(red bull|sugarfree|sugar-free|cans?|sips?|sipping|fizz\w*|taurine|caffeine)\b",re.I)
def lint(d):
    P=[]; t=json.load(open(f"{d}/template.json"))
    if not os.path.exists(f"{d}/style.json"): P.append("missing style.json")
    raw=json.dumps({k:v for k,v in t.items() if k!="example_fill"})
    wb=t.get("world_bible",{}); pa=wb.get("product_adjacent",{})
    import copy as _c
    tt=_c.deepcopy({k:v for k,v in t.items() if k!="example_fill"})
    tt.get("world_bible",{}).get("product_adjacent",{}).pop("ingested",None)
    for s in tt.get("shots",[]): s.get("product_action",{}).pop("ingested",None)
    raw_no_adj=json.dumps(tt)
    for m in set(x.lower() for x in BANNED.findall(raw_no_adj)): P.append(f"example-product word outside example_fill: {m}")
    if re.search("[—–]",open(f"{d}/template.json").read()): P.append("em or en dash present")
    fit=t.get("fit",{}).get("archetypes",{})
    for a in ARCH:
        if a not in fit: P.append(f"fit missing {a}")
    shots={s["id"]:s for s in t.get("shots",[])}; lines={l["id"] for l in t.get("script",[])}
    for s in t.get("shots",[]):
        if s.get("product_role","absent")!="absent":
            pa2=s.get("product_action",{})
            miss=[a for a in ARCH if not pa2.get(a)]
            if miss: P.append(f"{s['id']} product_action missing {miss}")
            if "{{action}}" not in s.get("keyframe_prompt",""): P.append(f"{s['id']} keyframe_prompt lacks {{{{action}}}}")
    for l in t.get("script",[]):
        for k in ["line_intent","max_words","delivery"]:
            if k not in l: P.append(f"{l['id']} missing {k}")
    for m in set(re.findall(r"\{\{([^}]+)\}\}",raw)):
        if m in ("action",) or m in CARD: continue
        if m.startswith("action.") and m[7:] in shots and shots[m[7:]].get("product_action"): continue
        if m.startswith("line.") and m[5:] in lines: continue
        if m.startswith("product.tagline_or_line.") and m.split(".")[-1] in lines: continue
        P.append(f"unknown slot {{{{{m}}}}}")
    for grp in ["cast","locations"]:
        for x in t.get(grp,[]):
            if not x.get("asset") or not os.path.exists(f"{d}/{x['asset']}"): P.append(f"{grp} {x.get('id')} asset missing")
    for x in wb.get("signature_objects",[]):
        if not x.get("asset") or not os.path.exists(f"{d}/{x['asset']}"): P.append(f"signature {x.get('id')} asset missing")
    au=t.get("asset_urls",{})
    ids=[x["id"] for x in t.get("cast",[])+t.get("locations",[])+wb.get("signature_objects",[]) if x.get("asset")]
    miss=[i for i in ids if i not in au]
    if miss: P.append(f"asset_urls missing ids {miss} (run lib/publish_bundle.py)")
    bad=[k for k,v in au.items() if "farooqchisty-hub.github.io" not in v]
    if bad: P.append(f"asset_urls not on permanent host: {bad[:3]}")
    ef=t.get("example_fill",{})
    if not ef.get("product") or not ef.get("lines") or not ef.get("actions"): P.append("example_fill incomplete (product, lines, actions)")
    words=sum(len(str(v).split()) for v in ef.get("lines",{}).values())
    if words>75: P.append(f"example spoken words {words} > 75")
    return P
if __name__=="__main__":
    for d in sys.argv[1:]:
        p=lint(d); print(d, "PASS" if not p else "FAIL"); [print("  -",x) for x in p]
