import json,subprocess,sys,time,re
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=[]
for i,q in enumerate(qs):
    d={}
    for attempt in range(4):
        r=subprocess.run(['treg','call','scrapecreators.x.v1-linkedin-search-posts','--query','query='+q,'--query','date_posted=last-year'],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except: d={}
        if d.get('treg_saturated') or not d: time.sleep(4); continue
        break
    posts=d.get('posts') or []
    for p in posts:
        out.append(dict(q=q,author=(p.get('author') or {}).get('name'),fol=(p.get('author') or {}).get('followers'),likes=p.get('likeCount'),nc=p.get('commentCount'),date=(p.get('datePublished') or '')[:10],url=p.get('url'),text=re.sub(r'\s+',' ',p.get('description') or '')[:1500]))
    print(i,q,len(posts),list(d.keys())[:5],file=sys.stderr)
json.dump(out,open(sys.argv[2],'w'),indent=1)
