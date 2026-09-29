"""Build contact sheet pages. python3 lib/page.py [style_key ...]  (no args = all + index)"""
import json,os,sys,html,subprocess,glob
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
DOCS=f"{ROOT}/docs/sheets"
E=html.escape
CSS="""
:root{--bg:#f7f6f2;--fg:#1c1b19;--mute:#6b6760;--line:#e2ded5;--card:#fff;--acc:#1f6f5c;--accs:#e3f1ec}
@media (prefers-color-scheme:dark){:root{--bg:#121211;--fg:#ecebe7;--mute:#a09c94;--line:#2c2b28;--card:#1b1a18;--acc:#6fd0b3;--accs:#17302a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.55 -apple-system,BlinkMacSystemFont,Inter,Segoe UI,sans-serif}
main{max-width:1240px;margin:0 auto;padding:32px 16px 80px}h1{font-size:30px;margin:4px 0}h2{font-size:19px;margin:38px 0 12px;padding-top:14px;border-top:1px solid var(--line)}
.sub{color:var(--mute)}.tag{display:inline-block;font-size:12px;padding:2px 9px;border-radius:99px;background:var(--accs);color:var(--acc);font-weight:600;margin-right:6px}
.log{font-size:17px;max-width:820px}.grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px}@media(max-width:1000px){.grid{grid-template-columns:repeat(3,1fr)}}@media(max-width:560px){.grid{grid-template-columns:repeat(2,1fr)}}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;font-size:12.5px}
.frame{position:relative;aspect-ratio:9/16;background:#000}.frame img{width:100%;height:100%;object-fit:cover;display:block}
.cap{position:absolute;left:6%;right:6%;top:66%;text-align:center;color:#fff;font-weight:650;font-size:13px;line-height:1.2;text-shadow:0 2px 6px rgba(0,0,0,.8)}
.pm{padding:8px 10px}.pm b{color:var(--acc)}.pm .l{margin-top:4px}.pm .m{color:var(--mute)}
.assets{display:flex;gap:12px;flex-wrap:wrap}.assets figure{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden}.assets img{height:230px;display:block}.assets figcaption{padding:6px 10px;font-size:12.5px}
table{width:100%;border-collapse:collapse;font-size:13.5px}th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--mute);font-size:12px}
pre{white-space:pre-wrap;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px;font:12.5px/1.5 ui-monospace,Menlo,monospace}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:800px){.two{grid-template-columns:1fr}}.box{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
a{color:var(--acc)}.wrap{overflow-x:auto}
"""
def jpg(src,dst,w):
    if not os.path.exists(src): return False
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    if not os.path.exists(dst) or os.path.getmtime(dst)<os.path.getmtime(src):
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",src,"-vf",f"scale={w}:-2","-q:v","4",dst])
    return True
def build(key):
    d=f"{ROOT}/styles/{key}"; st=json.load(open(f"{d}/style.json")); b=json.load(open(f"{d}/board.json"))
    out=f"{DOCS}/{key}"; os.makedirs(out,exist_ok=True)
    spk={c["id"]:c["name"].split()[0] for c in b.get("cast",[])}
    lines={}
    for L in b.get("script",[]): lines.setdefault(L.get("shot"),[]).append(L)
    panels=[]
    for s in b["shots"]:
        ok=jpg(f"{d}/img/{s['id']}.png",f"{out}/{s['id']}.jpg",540)
        cap=f'<div class="cap">{E(s.get("caption",""))}</div>' if s.get("caption") else ""
        img=f'<img loading="lazy" src="{s["id"]}.jpg" alt="">' if ok else '<div style="color:#999;padding:40% 10px;text-align:center">not rendered</div>'
        panels.append(f'<div class="panel"><div class="frame">{img}{cap}</div><div class="pm"><b>{s["id"]}</b> · {s["t0"]:.1f} to {s["t1"]:.1f}s · {E(s.get("beat",""))}<div class="m">{E(s.get("framing",""))}, {E(s.get("camera",""))}</div><div class="l">{E(s.get("action",""))}</div>{('<div class="m">Details: '+E("; ".join(s["dressing"]))+'</div>') if s.get("dressing") else ""}<div class="m">Product: {E(s.get("product_state",""))} · Sound: {E(s.get("audio",""))}</div></div></div>')
    assets=[]
    for c in b.get("cast",[]):
        if jpg(f"{d}/img/{c['id']}.png",f"{out}/{c['id']}.jpg",900): assets.append(f'<figure><img src="{c["id"]}.jpg" alt=""><figcaption><b>{E(c["name"])}</b>, {E(c["role"])}<br><span class="sub">Voice: {E(c.get("voice",""))}</span></figcaption></figure>')
    for l in b.get("locations",[]):
        if jpg(f"{d}/img/{l['id']}.png",f"{out}/{l['id']}.jpg",500): assets.append(f'<figure><img src="{l["id"]}.jpg" alt=""><figcaption><b>{E(l["name"])}</b></figcaption></figure>')
    wb=b.get("world_bible",{}); wbh=""
    if wb:
        props=[]
        for o in wb.get("signature_objects",[]):
            if jpg(f"{d}/img/{o['id']}.png",f"{out}/{o['id']}.jpg",900): props.append(f'<figure><img src="{o["id"]}.jpg" alt=""><figcaption><b>{E(o["name"])}</b></figcaption></figure>')
        locs="".join(f'<div class="box"><b>{E(k)}</b><p><span class="sub">Foreground</span><br>{E("; ".join(v.get("foreground",[])))}</p><p><span class="sub">Midground</span><br>{E("; ".join(v.get("midground",[])))}</p><p><span class="sub">Background</span><br>{E("; ".join(v.get("background",[])))}</p></div>' for k,v in wb.get("locations",{}).items())
        pp="".join(f'<li><b>{E(spk.get(k,k))}</b>: {E("; ".join(v))}</li>' for k,v in wb.get("personal_props",{}).items())
        bs="".join(f'<li><b>{E(x["name"])}</b>: {E(x["mark"])}, {E(x["colors"])}. On: {E(x["appears_on"])}. Text in post: {E(x["text_in_post"])}</li>' for x in wb.get("brand_system",[]))
        wbh=f'''<h2>World bible</h2><p class="sub">Fixed with the concept: the lore, the objects and the textures that make this world specific. Only product-adjacent props change per product.</p>
<div class="box"><b>Lore</b><ul>{"".join(f"<li>{E(x)}</li>" for x in wb.get("lore",[]))}</ul>{("<p><b>Materials.</b> "+E(wb["materials_rule"])+"</p>") if wb.get("materials_rule") else ""}<p><b>Wear and time.</b> {E(wb.get("wear_and_time",""))}</p></div>
<h3>Signature objects</h3><div class="assets">{"".join(props)}</div>
<h3>Set dressing by location</h3><div class="two">{locs}</div>
<div class="two" style="margin-top:14px"><div class="box"><b>Personal props</b><ul>{pp}</ul></div><div class="box"><b>Fictional brand system</b><ul>{bs}</ul><b>Sound world</b><p>{E("; ".join(wb.get("sound_world",[])))}</p></div></div>'''
    words=sum(len(L["line"].split()) for L in b.get("script",[]))
    script="".join(f'<tr><td>{E(L["t"])}</td><td><b>{E(spk.get(L["speaker"],L["speaker"]))}</b>{"" if L.get("on_camera") else " (off camera)"}</td><td>{E(L["line"])}<div class="sub">{E(L.get("delivery",""))}{(" · Say: "+E(L["phonetic"])) if L.get("phonetic") else ""}</div></td><td class="sub">{E(L.get("line_intent",""))}</td></tr>' for L in b.get("script",[]))
    beats="".join(f'<tr><td>{E(x["t"])}</td><td><b>{E(x["id"])}</b></td><td>{E(x["summary"])}</td></tr>' for x in b["beats"])
    units="".join(f'<h3>{E(u["id"])} · {u["t0"]} to {u["t1"]} s · {u["len_s"]} s generation{" · exact-risk (short, cheap to re-roll)" if u.get("exact_risk") else ""}</h3><p class="sub">Shots {", ".join(u["shots"])} · References: {E(", ".join(u.get("refs",[])))}</p><pre>{E(u["prompt"])}</pre>' for u in b["units"])
    music="".join(f'<tr><td>{m["t0"]} to {m["t1"]} s</td><td><b>{E(m["section"])}</b></td><td>{E(m["brief"])}</td></tr>' for m in b.get("music",[]))
    sfx="".join(f'<li>{x["t"]} s: {E(x["sound"])} ({E(x["why"])})</li>' for x in b.get("sfx",[])) or "<li>None; native sound only</li>"
    ad="".join(f'<tr><td><b>{E(k)}</b></td><td>{E(v["moment"])}</td><td>{E(v["scale"])}</td></tr>' for k,v in b.get("adaptation",{}).items())
    cl=st["caption_look"]; capspec=", ".join(f"{k.replace('_',' ')}: {v}" for k,v in cl.items())
    c=b.get("cost_estimate",{})
    world=b.get("world",{})
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(b["title"])} Storyboard</title><style>{CSS}</style></head><body><main>
<p><a href="../">All storyboards</a></p><span class="tag">{E(st["name"])}</span><span class="tag">{b["runtime_s"]} s · {b["aspect"]}</span><span class="tag">Red Bull Sugarfree</span>
<h1>{E(b["title"])}</h1><p class="log">{E(b["logline"].replace("{product}","Red Bull Sugarfree"))}</p>
<p class="sub">{E(st.get("why_it_sells",""))}</p>
<h2>Contact sheet</h2><p class="sub">One keyframe per shot, with the caption as it will appear.</p><div class="grid">{"".join(panels)}</div>
<h2>Cast and world</h2><div class="assets">{"".join(assets)}</div>
<p><b>World.</b> {E(world.get("setting",""))} <b>Palette.</b> {E(world.get("palette",""))}<br><b>Fictional brands.</b> {E("; ".join(world.get("fictional_brands",[])))}</p>
{wbh}<h2>Beats</h2><div class="wrap"><table><tr><th>Time</th><th>Beat</th><th>What happens</th></tr>{beats}</table></div>
<h2>Screenplay</h2><p class="sub">{words} spoken words in {b["runtime_s"]} s. Each line keeps its intent (fixed in the template) and its wording (written for this product).</p><div class="wrap"><table><tr><th>Time</th><th>Speaker</th><th>Line</th><th>Intent (template)</th></tr>{script}</table></div>
<h2>Generation plan</h2>{units}
<h2>Sound, music, voice, captions</h2><div class="two"><div class="box"><b>Score</b> (one continuous piece, sections stitched at picture cuts)<table>{music}</table><p><b>Added sound</b></p><ul>{sfx}</ul></div>
<div class="box"><b>Voices</b><ul>{"".join(f"<li>{E(spk.get(v['speaker'],v['speaker']))}: {E(v['plan'])}</li>" for v in b.get("voices",[]))}</ul><b>Captions</b><p>{E(capspec)}</p><b>Post text</b><ul>{"".join(f"<li>{t['t0']} to {t['t1']} s: {E(t['text'])} / {E(t.get('sub',''))} ({E(t.get('style',''))})</li>" for t in b.get("post_text",[]))}</ul></div></div>
<h2>Adaptation contract</h2><p class="sub">How this same concept takes any physical product.</p><div class="wrap"><table><tr><th>Product type</th><th>Where it sits in the story</th><th>Scale</th></tr>{ad}</table></div>
<h2>Style bible</h2><div class="box"><p><b>Look.</b> {E(st.get("visual_grammar",""))}</p><p><b>Camera.</b> {E(st.get("camera",""))}</p><p><b>Light and texture.</b> {E(st.get("light",""))} {E(st.get("texture",""))}</p><p><b>Pacing.</b> {E(st.get("pacing",""))}</p><p><b>Sound.</b> {E(st.get("sound",""))}</p><p><b>Known failures.</b></p><ul>{"".join(f"<li>{E(x)}</li>" for x in st.get("failure_modes",[]))}</ul></div>
<h2>Claims and cost</h2><p><b>Claims used</b> (all from the product page): {E("; ".join(b.get("claims_used",[])))}</p><p><b>Video estimate:</b> {c.get("seconds","?")} s of generation at ${c.get("usd_per_s","?")}/s = ${c.get("first_pass_usd","?")} first pass, ${E(str(c.get("with_retakes_usd","?")))} with retakes, plus about ${c.get("music_usd","?")} music.</p>
</main></body></html>'''
    open(f"{out}/index.html","w").write(page)
    return b,st
def index(keys):
    cards=[]
    for k in keys:
        b=json.load(open(f"{ROOT}/styles/{k}/board.json")); st=json.load(open(f"{ROOT}/styles/{k}/style.json"))
        th="".join(f'<img src="{k}/{s["id"]}.jpg" alt="">' for s in b["shots"][:5] if os.path.exists(f"{DOCS}/{k}/{s['id']}.jpg"))
        cards.append(f'<a class="ic" href="{k}/"><div class="th">{th}</div><div class="pm"><span class="tag">{E(st["name"])}</span><h3>{E(b["title"])}</h3><p class="sub">{E(b["logline"].replace("{product}","Red Bull Sugarfree"))}</p></div></a>')
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Storyboard Contact Sheets</title><style>{CSS}
.ig{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}}.ic{{display:block;background:var(--card);border:1px solid var(--line);border-radius:12px;overflow:hidden;color:inherit;text-decoration:none}}.ic:hover{{border-color:var(--acc)}}.th{{display:grid;grid-template-columns:repeat(5,1fr)}}.th img{{width:100%;aspect-ratio:9/16;object-fit:cover;display:block}}.ic h3{{margin:6px 0 2px;font-size:17px}}</style></head><body><main>
<h1>Storyboard contact sheets</h1><p class="sub">{len(keys)} styles, one flagship concept each, all for Red Bull Sugarfree, 30 s, 9:16. Checkpoint 1: review and approve.</p><div class="ig">{"".join(cards)}</div></main></body></html>'''
    open(f"{DOCS}/index.html","w").write(page)
if __name__=="__main__":
    keys=sys.argv[1:] or sorted(os.path.basename(p) for p in glob.glob(f"{ROOT}/styles/*") if os.path.exists(f"{p}/board.json"))
    for k in keys: build(k)
    allk=sorted(os.path.basename(p) for p in glob.glob(f"{ROOT}/styles/*") if os.path.exists(f"{p}/board.json"))
    index(allk); print("built",keys)
