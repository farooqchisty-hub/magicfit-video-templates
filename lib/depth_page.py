import json,html,os,glob
E=html.escape; ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
css=open(f"{ROOT}/lib/page.py").read().split('CSS="""')[1].split('"""')[0]
sec=[];nav=[]
for f in sorted(glob.glob(f"{ROOT}/styles/*/board.json")):
    b=json.load(open(f)); k=b["style"]; st=json.load(open(f.replace("board","style")))
    if not os.path.isdir(f"{ROOT}/docs/sheets/{k}/v1"): continue
    wb=b.get("world_bible",{})
    rows="".join(f'<div class="pair"><div><img loading="lazy" src="../{k}/v1/{s["id"]}.jpg" alt=""><span>Before</span></div><div><img loading="lazy" src="../{k}/{s["id"]}.jpg" alt=""><span>After</span></div><p><b>{s["id"]}</b> {E("; ".join(s.get("dressing",[])))}</p></div>' for s in b["shots"] if os.path.exists(f"{ROOT}/docs/sheets/{k}/v1/{s['id']}.jpg"))
    lore="".join(f"<li>{E(x)}</li>" for x in wb.get("lore",[])[:3])
    nav.append(f'<a href="#{k}">{E(st["name"])}</a>')
    sec.append(f'<h2 id="{k}">{E(st["name"])}: {E(b["title"])}</h2><p><a href="../{k}/">Full sheet with the world bible</a></p><ul class="sub">{lore}</ul><div class="pairs">{rows}</div>')
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>World Depth Pass</title><style>{css}
.pairs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}}.pair{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px;display:grid;grid-template-columns:1fr 1fr;gap:6px}}.pair div{{position:relative}}.pair img{{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:6px;display:block}}.pair span{{position:absolute;top:6px;left:6px;background:rgba(0,0,0,.65);color:#fff;font-size:11px;padding:1px 7px;border-radius:99px}}.pair p{{grid-column:1/3;margin:4px 2px;font-size:12.5px;color:var(--mute)}}.nav{{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:14px}}</style></head><body><main>
<p><a href="../">All storyboards</a></p><h1>World depth pass: before and after</h1>
<p class="log">Same beats, cast and screenplay in all {len(sec)} styles. Each board now has a world bible (lore, a 3-layer set-dressing inventory per location, personal props, signature objects drawn as prop sheets, a fictional brand system, wear rules, a sound world), and every shot names 3 to 6 specific details from it.</p><div class="nav">{"".join(nav)}</div>
{"".join(sec)}</main></body></html>'''
open(f"{ROOT}/docs/sheets/depth/index.html","w").write(page); print(len(sec))
