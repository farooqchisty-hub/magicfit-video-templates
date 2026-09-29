import json,subprocess,sys,time,re
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=[]
for i,q in enumerate(qs):
    d={}
    for attempt in range(4):
        r=subprocess.run(['treg','call','scrapecreators.reddit.search.posts','--query','query='+q,'--query','sort=relevance','--query','timeframe=year','--query','trim=true'],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except: d={}
        if d.get('treg_saturated') or not d: time.sleep(4); continue
        break
    posts=d.get('posts') or (d.get('output') or {}).get('posts') or []
    for p in posts:
        out.append(dict(q=q,sub=p.get('subreddit'),score=p.get('score'),nc=p.get('num_comments'),date=(p.get('created_at_iso') or '')[:10],url=p.get('url'),title=p.get('title'),text=re.sub(r'\s+',' ',p.get('selftext') or '')[:700]))
    print(i,q,len(posts),list(d.keys())[:6],file=sys.stderr)
json.dump(out,open(sys.argv[2],'w'),indent=1)
