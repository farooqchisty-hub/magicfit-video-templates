"""Wan 2.7 r2v and Kling v3 omni on Replicate, ledgered. python3 othergen.py wan|kling out.mp4 duration prompt ref1 ref2 ..."""
import json,sys,os,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); LEDGER=f"{HERE}/ledger.jsonl"; KEY=open(os.path.expanduser("~/.replicate_key")).read().strip()
which,out,dur,prompt,refs=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4],sys.argv[5:]
price={"wan":0.10,"kling":0.168}[which]; est=price*dur
spent=sum(json.loads(l)["usd"] for l in open(LEDGER))
if spent+est>50: sys.exit("REFUSED cap")
H={"Authorization":f"Bearer {KEY}","Content-Type":"application/json","User-Agent":"mf/1"}
def req(u,d=None): return json.load(urllib.request.urlopen(urllib.request.Request(u,data=json.dumps(d).encode() if d else None,headers=H),timeout=180))
if which=="wan": m="wan-video/wan-2.7-r2v"; inp={"prompt":prompt,"duration":dur,"resolution":"720p","aspect_ratio":"9:16","reference_images":refs}
else: m="kwaivgi/kling-v3-omni-video"; inp={"prompt":prompt,"duration":dur,"aspect_ratio":"9:16","mode":"standard","generate_audio":True,"reference_images":refs}
p=req(f"https://api.replicate.com/v1/models/{m}/predictions",{"input":inp})
while p["status"] not in ("succeeded","failed","canceled"): time.sleep(8); p=req(f"https://api.replicate.com/v1/predictions/{p['id']}")
if p["status"]!="succeeded": sys.exit("FAILED "+str(p.get("error"))[:300])
u=p["output"] if isinstance(p["output"],str) else p["output"][0]
open(out,"wb").write(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"mf/1"}),timeout=300).read())
open(LEDGER,"a").write(json.dumps({"t":time.time(),"tag":f"bake/{which}","usd":round(est,3),"out":out})+"\n"); print(out,f"${est:.2f}")
