import json,subprocess,sys,time,re
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
out=[]
for i,q in enumerate(qs):
    for attempt in range(4):
        r=subprocess.run(['treg','call','anyapi.x.search.posts','--method','POST','--data',json.dumps({"query":q,"limit":20,"queryType":"Top"})],capture_output=True,text=True)
        try: d=json.loads(r.stdout)
        except: d={}
        if d.get('treg_saturated') or not d: time.sleep(4); continue
        break
    items=(d.get('output') or {}).get('data',{}).get('items',[]) or []
    for it in items:
        out.append(dict(q=q,user=it.get('authorUsername'),fol=it.get('authorFollowers'),likes=it.get('likeCount'),views=it.get('viewCount'),bm=it.get('bookmarkCount'),date=time.strftime('%Y-%m-%d',time.gmtime(it.get('createdUtc',0))),url=it.get('url'),text=re.sub(r'\s+',' ',it.get('text',''))[:600]))
    print(i,q,len(items),d.get('costUsd'),file=sys.stderr)
json.dump(out,open(sys.argv[2],'w'),indent=1)
