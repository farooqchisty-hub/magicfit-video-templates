import json,base64,os,urllib.request,concurrent.futures as cf
KEY=open(os.path.expanduser("~/.openrouter_key")).read().strip()
ads=[a for a in json.load(open("research/ads.json")) if a["page"]!="Pop Picks"]
STY="""ugc_testimonial (creator talking to camera reviewing product)
creator_tutorial_demo (how-to, GRWM, routine, recipe, showing how to use)
unboxing_first_impression
problem_solution_before_after
founder_story
street_interview_vox_pop
skit_comedy (scripted scene with actors, humor)
podcast_clip (mic, podcast set)
green_screen_reaction (creator over screenshot/article)
us_vs_them_comparison
cinematic_brand_film (high production narrative, film look)
day_in_the_life (following a person through their routine)
athlete_celebrity_endorsement
product_hero_studio (product-only motion, packshots, CGI, macro, drops, splashes)
stop_motion
animation_2d
animation_3d_character
claymation
anime_manga
comic_book
asmr_sensory
kinetic_typography_motion_graphics (text-led, UI, graphics)
lifestyle_montage (music-driven cuts of people using product, no talking)
news_mockumentary_parody
meme_trend_format
other"""
PROMPT=f"""These are frames sampled left to right (at ~0.5s,3s,8s,15s,24s,40s) from one Meta video ad by the brand below. Classify its creative STYLE.
Styles:
{STY}
Return JSON only: {{"primary":"<style key>","secondary":"<style key or null>","person_on_camera":true/false,"talks_to_camera":true/false,"production":"lo-fi phone|polished live action|studio product|animated|mixed","other_desc":"<if other, 3-6 words>","hook_desc":"<first frame in 8 words>"}}"""
def cls(a):
    out=f"research/tiles/{a['id']}.cls.json"
    if os.path.exists(out): return json.load(open(out))
    img=base64.b64encode(open(f"research/tiles/{a['id']}.jpg","rb").read()).decode()
    body={"model":"google/gemini-2.5-flash","temperature":0,"response_format":{"type":"json_object"},"messages":[{"role":"user","content":[{"type":"text","text":PROMPT+f"\nBrand: {a['brand']}\nAd copy: {a['body'][:300]}"},{"type":"image_url","image_url":{"url":"data:image/jpeg;base64,"+img}}]}]}
    for _ in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"}),timeout=90)
            j=json.load(r); t=j["choices"][0]["message"]["content"].strip().strip("`").removeprefix("json")
            res=json.loads(t); res["cost"]=j.get("usage",{}).get("cost"); json.dump(res,open(out,"w")); return res
        except Exception as e: err=str(e)
    return {"error":err}
with cf.ThreadPoolExecutor(16) as ex: R=list(ex.map(cls,ads))
print(sum(1 for r in R if "error" in r),"errors; cost",sum((r.get("cost") or 0) for r in R))
