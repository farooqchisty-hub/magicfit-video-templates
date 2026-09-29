"""Image generation via treg -> reAPI Nano Banana Pro. gen(prompt, refs, out, size)"""
import json,subprocess,time,os,urllib.request,sys
os.environ["PATH"]=os.path.expanduser("~/.local/bin")+":"+os.environ["PATH"]
LOG=os.path.join(os.path.dirname(__file__),"..","costs.jsonl")
def _call(args,timeout=180):
    r=subprocess.run(["treg","call",*args],capture_output=True,text=True,timeout=timeout)
    try: return json.loads(r.stdout)
    except Exception: raise RuntimeError(f"treg: {r.stdout[:400]} {r.stderr[:400]}")
def gen(prompt,refs=(),out="out.png",size="9:16",res="2K",tries=2,tag=""):
    body={"model":"gemini-3-pro-image-preview","prompt":prompt,"size":size,"resolution":res}
    if refs: body["image_urls"]=list(refs)
    last=None
    for t in range(tries):
        j=_call(["reapi.image-gen.gemini-3-pro-image","--method","POST","--data",json.dumps(body)])
        tid=j.get("id")
        if not tid: last=j; continue
        for _ in range(60):
            time.sleep(5)
            s=_call(["reapi.tasks.get","--query",f"id={tid}"])
            st=s.get("status")
            if st is None: raise RuntimeError(f"poll: {json.dumps(s)[:300]}")
            if st=="completed":
                url=s["output"]["image_urls"][0]
                req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
                os.makedirs(os.path.dirname(out) or ".",exist_ok=True)
                open(out,"wb").write(urllib.request.urlopen(req,timeout=120).read())
                open(LOG,"a").write(json.dumps({"t":time.time(),"tag":tag,"out":out,"usd":0.03})+"\n")
                open(out+".url","w").write(url)
                return url
            if st=="failed": last=s; break
    raise RuntimeError(f"gen failed: {json.dumps(last)[:500]}")
if __name__=="__main__":
    a=json.loads(sys.argv[1]); print(gen(**a))
