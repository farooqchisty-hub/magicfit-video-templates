"""Assemble units into the final ad.
Usage: python3 assemble.py edit.json
edit.json: {"fps":30,"w":1080,"h":1920,"out":"run/final.mp4",
 "clips":[{"file":"run/units/U1.mp4","in":0,"out":8.2,"gain":1.0}, ...],   (gain 0 mutes a clip's native audio)
 "music":[{"file":"run/music/tension.mp3","start":0.0}, ...],   (sections laid on the timeline, 0.4 s crossfades)
 "music_gain":0.55, "duck":true,
 "sfx":[{"file":"x.wav","start":10.6,"gain":0.8}],
 "voiceover":[{"file":"run/vo/n1.mp3","start":0.3}],   (narration; ducks the music like dialogue)
 "captions_concat":"run/captions/captions.ffconcat"}   (from captions.py)"""
import json,sys,subprocess,os,tempfile
def run(c): r=subprocess.run(c,capture_output=True,text=True); (r.returncode and sys.exit(r.stderr[-2000:]))
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout.strip())
e=json.load(open(sys.argv[1])); fps=e.get("fps",30); W=e.get("w",1080); H=e.get("h",1920)
tmp=tempfile.mkdtemp(); parts=[]
for i,c in enumerate(e["clips"]):
    p=f"{tmp}/p{i}.mp4"; d=c["out"]-c["in"]
    run(["ffmpeg","-y","-ss",str(c["in"]),"-t",f"{d:.3f}","-i",c["file"],"-f","lavfi","-t",f"{d:.3f}","-i","anullsrc=r=48000:cl=stereo",
         "-filter_complex",f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1[v];[0:a]volume={c.get('gain',1)}[ga];[ga][1:a]amix=inputs=2:duration=longest,atrim=0:{d:.3f}[a]",
         "-map","[v]","-map","[a]","-c:v","libx264","-preset","medium","-crf","18","-c:a","aac","-ar","48000",p] if subprocess.run(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=index","-of","csv=p=0",c["file"]],capture_output=True,text=True).stdout.strip() else
        ["ffmpeg","-y","-ss",str(c["in"]),"-t",f"{d:.3f}","-i",c["file"],"-f","lavfi","-t",f"{d:.3f}","-i","anullsrc=r=48000:cl=stereo",
         "-filter_complex",f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps},setsar=1[v]","-map","[v]","-map","1:a","-c:v","libx264","-preset","medium","-crf","18","-c:a","aac","-ar","48000",p])
    parts.append(p)
lst=f"{tmp}/l.txt"; open(lst,"w").write("".join(f"file '{p}'\n" for p in parts))
joined=f"{tmp}/joined.mp4"; run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",joined])
total=dur(joined)
inputs=["-i",joined]; fl=[]; n=1; mus=[]
for m in e.get("music",[]):
    inputs+=["-i",m["file"]]; fl.append(f"[{n}:a]adelay={int(m['start']*1000)}|{int(m['start']*1000)},afade=t=in:st={m['start']}:d=0.4,volume={e.get('music_gain',0.55)}[m{n}]"); mus.append(f"[m{n}]"); n+=1
vos=[]
for v in e.get("voiceover",[]):
    inputs+=["-i",v["file"]]; fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={int(v['start']*1000)}|{int(v['start']*1000)},volume={v.get('gain',1.0)}[vo{n}]"); vos.append(f"[vo{n}]"); n+=1
if vos:
    fl.append(f"[0:a]{''.join(vos)}amix=inputs={1+len(vos)}:normalize=0:duration=first[dbus]"); DIA="[dbus]"
else: DIA="[0:a]"
sfx=[]
for s in e.get("sfx",[]):
    inputs+=["-i",s["file"]]; fl.append(f"[{n}:a]adelay={int(s['start']*1000)}|{int(s['start']*1000)},volume={s.get('gain',0.8)}[s{n}]"); sfx.append(f"[s{n}]"); n+=1
if mus:
    fl.append(f"{''.join(mus)}amix=inputs={len(mus)}:normalize=0,apad,atrim=0:{total:.3f},afade=t=out:st={max(total-1.2,0):.3f}:d=1.2[mus]")
    if e.get("duck",True): fl.append(f"{DIA}asplit=2[dia][key];[mus][key]sidechaincompress=threshold=0.04:ratio=6:attack=40:release=400[mduck]"); base="[dia][mduck]"
    else: base=f"{DIA}[mus]"
    fl.append(f"{base}{''.join(sfx)}amix=inputs={2+len(sfx)}:normalize=0[mix]")
else:
    fl.append(f"{DIA}{''.join(sfx)}amix=inputs={1+len(sfx)}:normalize=0[mix]")
fl.append("[mix]loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
if e.get("captions_concat"):
    capmov=f"{tmp}/captions.mov"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",e["captions_concat"],"-vf",f"fps={fps},format=argb","-t",f"{total:.3f}","-c:v","qtrle",capmov])
    inputs+=["-i",capmov]
    fl.append(f"[{n}:v]format=rgba[cap];[0:v][cap]overlay=0:0:eof_action=pass:format=auto[vout]"); n+=1
else: fl.append("[0:v]null[vout]")
out=e.get("out","final.mp4"); os.makedirs(os.path.dirname(out) or ".",exist_ok=True)
run(["ffmpeg","-y",*inputs,"-filter_complex",";".join(fl),"-map","[vout]","-map","[aout]","-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart","-t",f"{total:.3f}",out])
print(out,f"{total:.2f}s")
