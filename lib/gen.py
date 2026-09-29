"""Image generation via treg -> reAPI Nano Banana Pro. gen(prompt, refs, out, size)"""
import json,subprocess,time,os,urllib.request,sys
os.environ["PATH"]=os.path.expanduser("~/.local/bin")+":"+os.environ["PATH"]
LOG=os.path.join(os.path.dirname(__file__),"..","costs.jsonl")
def _call(args,timeout=180):
    r=subprocess.run(["treg","call",*args],capture_output=True,text=True,timeout=timeout)
    try: return json.loads(r.stdout)
    except Exception: raise RuntimeError(f"treg: {r.stdout[:400]} {r.stderr[:400]}")
def gen(prompt,refs=(),out="out.png",size="9:16",res="2K",tries=4,tag="",model="nbpro"):
    ep="reapi.image-gen.gemini-3-pro-image"
    body={"model":"gemini-3-pro-image-preview","prompt":prompt,"size":size,"resolution":res}
    if model=="gpt25":
        ep="reapi.image-gen.gpt-image-2-5"
        px={"9:16":"1024x1536","16:9":"1536x1024","1:1":"1024x1024"}.get(size,"1024x1536")
        body={"model":"gpt-image-2.5-flare-official","prompt":prompt,"size":px,"quality":"high","n":1}
    if refs: body["image_urls"]=list(refs)
    last=None
    for t in range(tries):
        try: j=_call([ep,"--method","POST","--data",json.dumps(body)])
        except Exception as e: last={"err":str(e)}; time.sleep(15); continue
        tid=j.get("id")
        if not tid: last=j; time.sleep(15); continue
        for _ in range(90):
            time.sleep(5)
            try: s=_call(["reapi.tasks.get","--query",f"id={tid}"])
            except Exception: continue
            st=s.get("status")
            if st is None: time.sleep(5); continue
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
