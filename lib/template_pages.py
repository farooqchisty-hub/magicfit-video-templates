"""Readable review pages for bundle templates -> docs/templates/"""
import json,glob,os,html
E=html.escape; ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
css=open(f"{ROOT}/lib/page.py").read().split('CSS="""')[1].split('"""')[0]
ARCH=["ingested","applied","worn","handheld","carried","home","consumable"]
OUT=f"{ROOT}/docs/templates"; os.makedirs(OUT,exist_ok=True)
def s(x): return E(str(x)) if x is not None else ""
cards=[]
for f in sorted(glob.glob(f"{ROOT}/bundle/templates/*/template.json")):
    t=json.load(open(f)); tid=os.path.basename(os.path.dirname(f)); st=json.load(open(f.replace("template.json","style.json")))
    fit=t.get("fit",{}).get("archetypes",{})
    fitrows="".join(f"<tr><td><b>{a}</b></td><td><span class='tag'>{s(fit.get(a,['?'])[0] if isinstance(fit.get(a),list) else fit.get(a))}</span></td><td>{s(fit.get(a,['',''])[1] if isinstance(fit.get(a),list) and len(fit.get(a))>1 else '')}</td></tr>" for a in ARCH)
    base=f"../bundle/templates/{tid}/"
    assets="".join(f'<figure><img loading="lazy" src="{base}{x["asset"]}" alt=""><figcaption><b>{s(x.get("name",x["id"]))}</b></figcaption></figure>' for x in t.get("cast",[])+t.get("locations",[])+t.get("world_bible",{}).get("signature_objects",[]) if x.get("asset"))
    ex=t.get("example_fill",{}).get("lines",{})
    script="".join(f"<tr><td>{s(L.get('t'))}</td><td><b>{s(L.get('speaker'))}</b>{'' if L.get('on_camera',True) else ' (off camera)'}</td><td>{('<b>Fixed:</b> '+s(L['fixed_line'])) if L.get('fixed_line') else s(L.get('line_intent'))}<div class='sub'>{s(L.get('rules',''))} Max {s(L.get('max_words'))} words. Delivery: {s(L.get('delivery'))}</div></td><td class='sub'>{s(ex.get(L['id'],''))}</td></tr>" for L in t.get("script",[]))
    shots=""
    for sh in t.get("shots",[]):
        pa=sh.get("product_action")
        shots+=f"<h3>{s(sh['id'])} · {sh.get('t0')} to {sh.get('t1')} s · {s(sh.get('product_role','absent'))}</h3><p>{s(sh.get('action'))}</p>"
        if pa: shots+="<div class='wrap'><table>"+"".join(f"<tr><td><b>{a}</b></td><td>{s(pa.get(a))}</td></tr>" for a in ARCH)+"</table></div>"
    adj=t.get("world_bible",{}).get("product_adjacent",{})
    adjrows="".join(f"<tr><td><b>{k}</b></td><td>{s('; '.join(v) if isinstance(v,list) else v)}</td></tr>" for k,v in adj.items())
    units="".join(f"<h3>{s(u['id'])} · {u.get('len_s')} s{' · exact-risk' if u.get('exact_risk') else ''}</h3><pre>{s(u.get('prompt'))}</pre>" for u in t.get("units",[]))
    lore="".join(f"<li>{s(x)}</li>" for x in t.get("world_bible",{}).get("lore",[]))
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{s(t["title"])} Template</title><style>{css}</style></head><body><main>
<p><a href="./">All templates</a> · <a href="{base}template.json">template.json</a> · <a href="../sheets/{t['style']}/">original storyboard</a></p><span class="tag">{s(st.get("name"))}</span><span class="tag">{s(tid)}</span>
<h1>{s(t["title"])}</h1><p class="log">{s(t["logline"])}</p>
<h2>Fit by product type</h2><div class="wrap"><table>{fitrows}</table></div><p class="sub">Refuses: {s("; ".join(t.get("fit",{}).get("avoid",[])))}</p>
<h2>Cast, world and props (shipped with the template)</h2><div class="assets">{assets}</div><div class="box"><ul>{lore}</ul></div>
<h2>Script: what each line must do</h2><p class="sub">Right column is the worked example for Red Bull Sugarfree.</p><div class="wrap"><table><tr><th>Time</th><th>Speaker</th><th>Intent (template)</th><th>Example</th></tr>{script}</table></div>
<h2>Product-adjacent props by type</h2><div class="wrap"><table>{adjrows}</table></div>
<h2>Shots and how the product appears for each type</h2>{shots}
<h2>Generation units (templated prompts)</h2>{units}
</main></body></html>'''
    open(f"{OUT}/{tid}.html","w").write(page)
    g=lambda a: (fit.get(a) or ["?"])[0] if isinstance(fit.get(a),list) else fit.get(a,"?")
    cards.append(f'<a class="ic" href="{tid}.html"><div class="pm"><span class="tag">{s(st.get("name"))}</span><h3>{s(t["title"])}</h3><p class="sub">{s(t["logline"])}</p><p class="sub">{" · ".join(f"{a}: <b>{g(a)}</b>" for a in ARCH)}</p></div></a>')
idx=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Video Templates</title><style>{css}
.ig{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}.ic{{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;color:inherit;text-decoration:none}}.ic:hover{{border-color:var(--acc)}}.ic h3{{margin:6px 0 2px}}</style></head><body><main>
<p><a href="../">Plan</a> · <a href="../sheets/">Storyboards</a> · <a href="../videos/">Videos</a></p><h1>{len(cards)} video templates</h1><p class="sub">The sellable, product-agnostic versions of the approved storyboards. Each page shows fit per product type, the line intents, how the product appears in every product shot for all 7 product types, and the templated generation prompts.</p><div class="ig">{"".join(cards)}</div></main></body></html>'''
open(f"{OUT}/index.html","w").write(idx); print(len(cards))
