"""Seedance on Replicate with a hard spend cap.
python3 videogen.py --out U1.mp4 --duration 9 --prompt "..." [--ref URL ...] [--first URL] [--model 2.5|2.0] [--res 720p] [--no-audio] [--tag run/U1]
Refuses if ledger total + this call's cost would exceed CAP. Ledger: testkit/ledger.jsonl"""
import argparse,json,os,sys,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__)); LEDGER=f"{HERE}/ledger.jsonl"; CAP=float(os.environ.get("VIDEO_CAP","50"))
PRICE={("2.5","480p"):0.1028,("2.5","720p"):0.2312,("2.0","480p"):0.08,("2.0","720p"):0.18}
MODEL={"2.5":"bytedance/seedance-2.5","2.0":"bytedance/seedance-2.0"}
KEY=open(os.path.expanduser("~/.replicate_key")).read().strip()
def spent(): return sum(json.loads(l)["usd"] for l in open(LEDGER)) if os.path.exists(LEDGER) else 0.0
def req(url,data=None):
    r=urllib.request.Request(url,data=json.dumps(data).encode() if data else None,headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json","Prefer":"wait=5"})
    return json.load(urllib.request.urlopen(r,timeout=120))
def run(prompt,out,duration,refs=(),first=None,model="2.5",res="720p",audio=True,tag="",aspect="9:16"):
    est=PRICE[(model,res)]*duration
    if spent()+est>CAP: sys.exit(f"REFUSED: spent ${spent():.2f} + ${est:.2f} would exceed cap ${CAP}")
    inp={"prompt":prompt,"duration":duration,"resolution":res,"aspect_ratio":aspect,"generate_audio":audio}
    if refs: inp["reference_images"]=list(refs)
    if first: inp["image"]=first; inp["aspect_ratio"]="adaptive" if model=="2.5" else aspect
    p=req(f"https://api.replicate.com/v1/models/{MODEL[model]}/predictions",{"input":inp})
    pid=p["id"]; t0=time.time()
    while p["status"] not in ("succeeded","failed","canceled"):
        time.sleep(8); p=req(f"https://api.replicate.com/v1/predictions/{pid}")
    if p["status"]!="succeeded":
        open(LEDGER,"a").write(json.dumps({"t":time.time(),"tag":tag,"usd":0,"status":p["status"],"id":pid})+"\n")
        sys.exit(f"FAILED {pid}: {str(p.get('error'))[:400]}")
    url=p["output"] if isinstance(p["output"],str) else p["output"][0]
    os.makedirs(os.path.dirname(os.path.abspath(out)),exist_ok=True)
    open(out,"wb").write(urllib.request.urlopen(url,timeout=300).read())
    open(LEDGER,"a").write(json.dumps({"t":time.time(),"tag":tag,"model":model,"res":res,"duration":duration,"usd":round(est,4),"id":pid,"out":out,"secs":int(time.time()-t0)})+"\n")
    print(out,f"${est:.2f}",f"total ${spent():.2f}")
if __name__=="__main__":
    a=argparse.ArgumentParser(); a.add_argument("--out",required=True); a.add_argument("--duration",type=int,default=5); a.add_argument("--prompt",required=True)
    a.add_argument("--ref",action="append",default=[]); a.add_argument("--first"); a.add_argument("--model",default="2.5"); a.add_argument("--res",default="720p")
    a.add_argument("--no-audio",action="store_true"); a.add_argument("--tag",default=""); a.add_argument("--aspect",default="9:16")
    x=a.parse_args(); run(x.prompt,x.out,x.duration,x.ref,x.first,x.model,x.res,not x.no_audio,x.tag,x.aspect)
