import json,urllib.request,os,time,sys,base64,subprocess,concurrent.futures as cf
KEY=open(os.path.expanduser("~/.openrouter_key")).read().strip()
def ask(model,msgs,max_tokens=60000):
    body={"model":model,"messages":msgs,"max_tokens":max_tokens}
    t=time.time(); r=json.load(urllib.request.urlopen(urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"}),timeout=900))
    u=r.get("usage",{}); return r["choices"][0]["message"]["content"],u.get("cost"),int(time.time()-t),u
spec=open("TEMPLATE_SPEC.md").read(); ref=open("bundle/templates/cinematic-01-night-stint/template.json").read()
ugc_style=open("styles/ugc/style.json").read(); ugc1=json.load(open("bundle/templates/ugc-01-finals-week/template.json"))
brief=("You are a senior creative director and template engineer. Write a NEW, second template for the UGC creator testimonial style, as one complete template.json following the spec exactly, including spec v2 fields (durations_supported, narrator (null for UGC), tiered beats with min_s/max_s, script lines with tier and sentences ranges) and the voice standard (full natural sentences, listen-only test, product line as a real sentence). "
 "The existing UGC template is 'Finals Week' (a grad student in a library at 2am), so your concept must differ in story engine, world, cast and tone. North American casting, fictional world, no real brands, no em or en dashes anywhere. "
 "Include all 7 product_action archetypes for every product shot, honest fit ratings, cast with card_prompt, locations with plate_prompt, a rich world_bible (lore, 3-layer set dressing, personal props, 2 to 3 signature objects with prop_prompt, brand_system, wear_and_time, sound_world, product_adjacent by archetype), units with templated prompts, music, captions from the style, post_text, qa, and example_fill for Red Bull Sugarfree. For asset fields use paths like assets/<id>.jpg (they will be rendered later). Output ONLY the JSON.\n\n"
 "=== SPEC ===\n"+spec+"\n=== REFERENCE TEMPLATE (structure and quality bar; do not copy its concept) ===\n"+ref+"\n=== UGC STYLE BIBLE ===\n"+ugc_style+"\n=== EXISTING UGC TEMPLATE LOGLINE ===\n"+ugc1["logline"])
script_brief=("Write the spoken script for a 30 second anime-style video ad following this voice standard: full natural sentences with connecting words, a warm dramatic-but-clear narrator voiceover carries the story, characters only talk to each other in natural lines, at most one short reaction line, the product is named inside a natural sentence with the reason this character uses it, claims only from the page. Word budget about 62 words total. "
 "Story: at the Harbor Cup skate final a rookie, Mika, has fallen twice; the three-time champion Dax laughs; she laces up her new shoes and lands the run. Product: Allbirds Tree Runner (page claims: breathable and lightweight; feels silky smooth and cool on your skin; perfect for everyday casual wear, walking, and warmer weather). "
 "Reply JSON only: {\"lines\":[{\"speaker\":\"narrator|mika|dax\",\"text\":\"...\"}]}")
jobs=[]
for m in ["openai/gpt-6-luna","openai/gpt-6-luna-pro"]:
    jobs.append(("template",m,[{"role":"user","content":brief}]))
    jobs.append(("script",m,[{"role":"user","content":script_brief}]))
def img(p): return "data:image/jpeg;base64,"+base64.b64encode(open(p,"rb").read()).decode()
qa_q="You are the QA checker for AI keyframes in a video ad. The product must match its reference; no real brands or logos other than the product; no readable text drawn by the model except the fictional team name HALCYON and car number 27; faces consistent; no physics errors; no extra fingers. List every defect you see in this frame, precisely, as JSON: {\"defects\":[\"...\"],\"pass\":true|false}."
for f in ["take1_79","take2_logo"]:
    for m in ["openai/gpt-6-luna","openai/gpt-6-luna-pro","anthropic/claude-sonnet-4.5"]:
        jobs.append((f"qa_{f}",m,[{"role":"user","content":[{"type":"text","text":qa_q},{"type":"image_url","image_url":{"url":img(f"luna_test/{f}.jpg")}}]}]))
def go(j):
    n,m,msgs=j
    try: c,cost,s,u=ask(m,msgs); return n,m,c,cost,s,u
    except Exception as e: return n,m,"ERR "+str(e)[:200],0,0,{}
res=[]
with cf.ThreadPoolExecutor(10) as ex:
    for n,m,c,cost,s,u in ex.map(go,jobs):
        tag=m.split("/")[-1]; open(f"luna_test/{n}_{tag}.txt","w").write(c); res.append((n,tag,cost,s,u.get("completion_tokens"))); print(n,tag,"cost",cost,"secs",s,"out_tokens",u.get("completion_tokens"))
