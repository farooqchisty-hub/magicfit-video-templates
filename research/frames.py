import json,subprocess,os,concurrent.futures as cf
ads=[a for a in json.load(open("research/ads.json")) if a["page"]!="Pop Picks"]
def tile(a):
    out=f"research/tiles/{a['id']}.jpg"
    if os.path.exists(out): return 1
    fr=[]
    for i,t in enumerate([0.5,3,8,15,24,40]):
        p=f"/tmp/fr_{a['id']}_{i}.jpg"
        r=subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",a["url"],"-frames:v","1","-vf","scale=-2:360",p],capture_output=True,timeout=60)
        if os.path.exists(p) and os.path.getsize(p)>0: fr.append(p)
    if not fr: return 0
    # duration
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",a["url"]],capture_output=True,text=True,timeout=60).stdout.strip()
    a["dur"]=d
    inputs=sum([["-i",p] for p in fr],[])
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",f"{''.join(f'[{i}:v]scale=-2:360,pad=ceil(iw/2)*2:360[v{i}];' for i in range(len(fr)))}{''.join(f'[v{i}]' for i in range(len(fr)))}hstack=inputs={len(fr)}" if len(fr)>1 else "scale=-2:360",out],capture_output=True)
    for p in fr: os.remove(p)
    json.dump({"dur":d,"n":len(fr)},open(out+".meta","w"))
    return int(os.path.exists(out))
with cf.ThreadPoolExecutor(16) as ex: res=list(ex.map(tile,ads))
print(sum(res),len(ads))
