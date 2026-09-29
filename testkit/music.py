"""ElevenLabs music on Replicate, instrumental. python3 music.py out.mp3 seconds "prompt" [tag]  (logged to ledger, $0.0083/s)"""
import json,sys,os,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); LEDGER=f"{HERE}/ledger.jsonl"; CAP=float(os.environ.get("VIDEO_CAP","50"))
KEY=open(os.path.expanduser("~/.replicate_key")).read().strip()
out,secs,prompt=sys.argv[1],float(sys.argv[2]),sys.argv[3]; tag=sys.argv[4] if len(sys.argv)>4 else ""
spent=sum(json.loads(l)["usd"] for l in open(LEDGER)) if os.path.exists(LEDGER) else 0
est=0.0083*secs
if spent+est>CAP: sys.exit("REFUSED cap")
def req(u,d=None):
    r=urllib.request.Request(u,data=json.dumps(d).encode() if d else None,headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json","User-Agent":"magicfit/1.0"}); return json.load(urllib.request.urlopen(r,timeout=180))
p=req("https://api.replicate.com/v1/models/elevenlabs/music/predictions",{"input":{"prompt":prompt,"music_length_ms":int(secs*1000),"force_instrumental":True,"output_format":"mp3_high_quality"}})
while p["status"] not in ("succeeded","failed","canceled"): time.sleep(4); p=req(f"https://api.replicate.com/v1/predictions/{p['id']}")
if p["status"]!="succeeded": sys.exit(str(p.get("error")))
u=p["output"] if isinstance(p["output"],str) else p["output"][0]
req2=urllib.request.Request(u,headers={"User-Agent":"magicfit/1.0"}); open(out,"wb").write(urllib.request.urlopen(req2,timeout=180).read())
open(LEDGER,"a").write(json.dumps({"t":time.time(),"tag":tag,"model":"elevenlabs-music","secs":secs,"usd":round(est,4),"out":out})+"\n"); print(out,f"${est:.2f}")
