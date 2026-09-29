"""Word-level transcript via Replicate incredibly-fast-whisper. python3 transcribe.py in.mp4 out.json"""
import json,sys,base64,subprocess,urllib.request,time,os,tempfile
KEY=open(os.path.expanduser("~/.replicate_key")).read().strip()
src,out=sys.argv[1],sys.argv[2]; w=tempfile.mktemp(suffix=".mp3")
subprocess.run(["ffmpeg","-y","-v","error","-i",src,"-vn","-ac","1","-ar","16000","-b:a","48k",w],check=True)
uri="data:audio/mpeg;base64,"+base64.b64encode(open(w,"rb").read()).decode()
def req(u,d=None):
    r=urllib.request.Request(u,data=json.dumps(d).encode() if d else None,headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json","User-Agent":"magicfit-templates/1.0"}); return json.load(urllib.request.urlopen(r,timeout=120))
p=req("https://api.replicate.com/v1/models/vaibhavs10/incredibly-fast-whisper/predictions",{"input":{"audio":uri,"timestamp":"word","language":"english","task":"transcribe"}}) if False else None
v=req("https://api.replicate.com/v1/models/vaibhavs10/incredibly-fast-whisper")["latest_version"]["id"]
p=req("https://api.replicate.com/v1/predictions",{"version":v,"input":{"audio":uri,"timestamp":"word","language":"english","task":"transcribe"}})
while p["status"] not in ("succeeded","failed","canceled"): time.sleep(3); p=req(f"https://api.replicate.com/v1/predictions/{p['id']}")
if p["status"]!="succeeded": sys.exit(str(p.get("error")))
o=p["output"]; words=[{"word":c["text"].strip(),"start":c["timestamp"][0],"end":c["timestamp"][1] if c["timestamp"][1] is not None else c["timestamp"][0]+0.3} for c in o.get("chunks",[])]
json.dump({"text":o.get("text"),"words":words},open(out,"w"),indent=1); print(o.get("text"))
