"""Captions without libass: renders transparent PNG overlays + an ffconcat timeline, plus an SRT.
Usage: python3 captions.py <timing.json> <template.json|caption_look.json> <out_dir>
timing.json: {"words":[{"word":"Hour","start":0.6,"end":0.9},...]}   (Whisper word timestamps)
         or  {"lines":[{"text":"Hour nineteen.","start":0.6,"end":2.8},...]}  (fallback, words spread evenly)
         optional "post":[{"text":"Product Name","sub":"Tagline","start":27.4,"end":30,"y":0.22}], "duration":30
Writes <out_dir>/captions.ffconcat (feed to assemble.py as "captions_concat"), PNG frames, captions.srt.
Needs Pillow (pip install pillow)."""
import json,sys,re,os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=os.path.dirname(os.path.abspath(__file__))
def font(weight,size):
    for p in [f"{HERE}/fonts/InterTight-{weight}.ttf",f"{HERE}/fonts/InterTight-600.ttf","/System/Library/Fonts/Helvetica.ttc","/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
def words_from(d):
    if d.get("words"): return [dict(w=x["word"].strip(),s=float(x["start"]),e=float(x["end"])) for x in d["words"] if x["word"].strip()]
    out=[]
    for L in d.get("lines",[]):
        ws=L["text"].split(); dur=(L["end"]-L["start"])/max(len(ws),1)
        out+=[dict(w=w,s=L["start"]+i*dur,e=L["start"]+(i+1)*dur) for i,w in enumerate(ws)]
    return out
def rgb(h,a=255): h=h.lstrip("#"); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)
def chunks(words,maxw):
    out=[];cur=[]
    for w in words:
        cur.append(w)
        if len(cur)>=maxw or re.search(r"[.!?,:;]$",w["w"]): out.append(cur);cur=[]
    if cur: out.append(cur)
    return out
def render(W,H,look,cap_words=None,active=None,post=None):
    im=Image.new("RGBA",(W,H),(0,0,0,0))
    if cap_words:
        size=int(H*float(re.findall(r"[\d.]+",str(look.get("size","5.2")))[0])/100) if "%" in str(look.get("size","5.2%")) else int(H*0.052)
        f=font(800 if re.search("Black|ExtraBold|Heavy",look.get("font","")) else 600,size)
        col=rgb(look.get("color","#FFFFFF")); act=re.findall(r"#[0-9A-Fa-f]{6}",str(look.get("active_word",""))); actc=rgb(act[0]) if act else col
        dim=col[:3]+(178,)
        m=re.search(r"(\d+)%",str(look.get("position",""))); cy=int(H*int(m.group(1))/100) if m else int(H*0.68)
        maxw=int(W*0.86); lines=[[]]; 
        for i,w in enumerate(cap_words):
            test=" ".join(x["w"] for _,x in lines[-1]+[(i,w)])
            if f.getlength(test)>maxw and lines[-1]: lines.append([])
            lines[-1].append((i,w))
        spec=" ".join(str(look.get(k,"")) for k in ("outline","shadow","stroke"))
        om=re.search(r"(\d+)\s*px\s*(?:solid\s*)?(#[0-9A-Fa-f]{6}|black|white)?[^,;]*?(?:outline|stroke)",spec) or re.search(r"(\d+)\s*px\s*(#[0-9A-Fa-f]{6})",str(look.get("outline","")))
        if om:
            c=om.group(2) or "black"; c={"black":"#000000","white":"#FFFFFF"}.get(c,c)
            sw,sc=max(2,int(int(om.group(1))*H/1280)),rgb(c)
        else: sw,sc=0,None
        lh=int(size*1.18); top=cy-lh*len(lines)//2
        layer=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(layer)
        boxed=bool(look.get("box")) and str(look.get("box")).lower() not in ("false","none","0")
        for li,L in enumerate(lines):
            text=" ".join(x["w"] for _,x in L); tw=f.getlength(text); x=(W-tw)/2; y=top+li*lh
            if boxed: d.rounded_rectangle([x-24,y-10,x+tw+24,y+lh-4],radius=14,fill=(0,0,0,165))
            for i,w in L:
                d.text((x,y),w["w"],font=f,fill=actc if i==active else (col if sw else dim),stroke_width=sw,stroke_fill=sc); x+=f.getlength(w["w"]+" ")
        if not boxed:
            sh=Image.new("RGBA",(W,H),(0,0,0,0)); sd=ImageDraw.Draw(sh)
            for li,L in enumerate(lines):
                text=" ".join(x["w"] for _,x in L); tw=f.getlength(text); sd.text(((W-tw)/2,top+li*lh+3),text,font=f,fill=(0,0,0,170))
            im=Image.alpha_composite(im,sh.filter(ImageFilter.GaussianBlur(6)))
        im=Image.alpha_composite(im,layer)
    if post and post.get("kind")=="namecard":
        d=ImageDraw.Draw(im); f1=font(800,int(H*0.036)); f2=font(600,int(H*0.022)); x0=int(W*0.06); y0=int(H*post.get("y",0.60))
        tw=max(f1.getlength(post["text"]),f2.getlength(post.get("sub","")))+int(W*0.08); bh=int(H*0.085); sk=int(bh*0.35)
        d.polygon([(x0,y0),(x0+tw+sk,y0),(x0+tw,y0+bh),(x0-sk,y0+bh)],fill=rgb(post.get("bar","#1E90FF"),235))
        d.text((x0+int(W*0.025),y0+int(bh*0.08)),post["text"],font=f1,fill=(255,255,255,255))
        if post.get("sub"): d.text((x0+int(W*0.025),y0+int(bh*0.56)),post["sub"],font=f2,fill=(255,255,255,235))
        return im
    if post and post.get("kind")=="sfx":
        sz=int(H*post.get("size",0.09)); f=font(800,sz); txt=post["text"]
        layer=Image.new("RGBA",(int(f.getlength(txt))+sz,int(sz*1.6)),(0,0,0,0)); ld=ImageDraw.Draw(layer)
        ld.text((sz//2,sz//4),txt,font=f,fill=(255,255,255,255),stroke_width=max(3,sz//10),stroke_fill=rgb(post.get("outline","#3AA0FF")))
        layer=layer.rotate(post.get("angle",10),expand=True,resample=Image.BICUBIC)
        im.alpha_composite(layer,(int(W*post.get("x",0.5))-layer.width//2,int(H*post.get("y",0.4))-layer.height//2))
        return im
    if post:
        d=ImageDraw.Draw(im); y=int(H*post.get("y",0.22)); maxw=W*0.86
        for txt,base in [(post["text"],0.058),(post.get("sub",""),0.034)]:
            if not txt: continue
            sz=int(H*base); f=font(800 if base>0.04 else 600,sz)
            words=txt.split(); rows=[txt]
            if f.getlength(txt)>maxw:
                rows=[];cur=""
                for w in words:
                    t=(cur+" "+w).strip()
                    if f.getlength(t)>maxw and cur: rows.append(cur);cur=w
                    else: cur=t
                rows.append(cur)
            while max(f.getlength(r) for r in rows)>maxw and sz>12: sz=int(sz*0.92); f=font(800 if base>0.04 else 600,sz)
            for r in rows:
                tw=f.getlength(r); d.text(((W-tw)/2,y),r,font=f,fill=(255,255,255,255),stroke_width=max(2,sz//14),stroke_fill=(16,38,63,255)); y+=int(sz*1.18)
            y+=int(sz*0.25)
    return im
def srt_ts(t): ms=int(round(t*1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
def build(timing,look,out,W=1080,H=1920):
    os.makedirs(out,exist_ok=True); words=words_from(timing); ch=chunks(words,int(look.get("max_words_on_screen",4)))
    ev=[]  # (start,end,chunk_index,active_index)
    for ci,c in enumerate(ch):
        endc=min(c[-1]["e"]+0.25, ch[ci+1][0]["s"] if ci+1<len(ch) else c[-1]["e"]+0.6)
        for i,w in enumerate(c): ev.append((w["s"], c[i+1]["s"] if i+1<len(c) else endc, ci, i))
    posts=timing.get("post",[]); dur=float(timing.get("duration", max([e[1] for e in ev]+[p["end"] for p in posts]+[1])))
    cuts=sorted(set([0,dur]+[e[0] for e in ev]+[e[1] for e in ev]+[p["start"] for p in posts]+[p["end"] for p in posts]))
    blank=f"{out}/blank.png"; Image.new("RGBA",(W,H),(0,0,0,0)).save(blank)
    lines=["ffconcat version 1.0"]; cache={}
    for a,b in zip(cuts,cuts[1:]):
        if b-a<0.001: continue
        m=(a+b)/2; e=next((x for x in ev if x[0]<=m<x[1]),None); p=next((x for x in posts if x["start"]<=m<x["end"]),None)
        key=(e[2],e[3]) if e else None, posts.index(p) if p else None
        if key==(None,None): fn=blank
        else:
            if key not in cache:
                fn=f"{out}/c{len(cache):03d}.png"; render(W,H,look,ch[e[2]] if e else None,e[3] if e else None,p).save(fn); cache[key]=fn
            fn=cache[key]
        lines+= [f"file '{os.path.abspath(fn)}'",f"duration {b-a:.3f}"]
    lines.append(f"file '{os.path.abspath(blank)}'")
    open(f"{out}/captions.ffconcat","w").write("\n".join(lines)+"\n")
    srt=[]
    for ci,c in enumerate(ch):
        endc=min(c[-1]["e"]+0.25, ch[ci+1][0]["s"] if ci+1<len(ch) else c[-1]["e"]+0.6)
        srt.append(f"{ci+1}\n{srt_ts(c[0]['s'])} --> {srt_ts(endc)}\n{' '.join(x['w'] for x in c)}\n")
    open(f"{out}/captions.srt","w").write("\n".join(srt))
    return f"{out}/captions.ffconcat"
if __name__=="__main__":
    t=json.load(open(sys.argv[1])); L=json.load(open(sys.argv[2])); L=L.get("captions",L.get("caption_look",L))
    print(build(t,L,sys.argv[3]))
