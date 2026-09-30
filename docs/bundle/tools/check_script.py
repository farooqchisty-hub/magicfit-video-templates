"""Script gate. python3 check_script.py script.json
script.json: {"duration":30,"pace_wps":2.4,"lines":[{"speaker":"narrator","text":"..."},...],"context":"one line on the story"}
Checks: word budget, fragments, reading grade, and (if OPENROUTER_API_KEY or ~/.openrouter_key exists) a model judge.
Exit 1 if it fails."""
import json,sys,re,os,urllib.request
d=json.load(open(sys.argv[1])); L=d["lines"]; dur=d["duration"]; pace=d.get("pace_wps",2.4)
changes=sum(1 for a,b in zip(L,L[1:]) if a["speaker"]!=b["speaker"])
budget=(dur-1.5-0.4*changes)*pace
words=sum(len(x["text"].split()) for x in L)
fails=[];warns=[]
if words>budget*1.03: fails.append(f"over budget: {words} words vs {budget:.0f} for {dur}s with {changes} speaker changes")
if words<budget*0.75: warns.append(f"under budget: {words} words vs {budget:.0f} (room for more explanation)")
FUNC=set("a an the is are was were be been am i you he she it we they my your her his its our their to of in on at for with and but so because that which this these those can will would do does did has have had not just if when then there here".split())
short=0;frags=[]
VERB=set("i you he she it we they is are am was were be been do does did have has had can could will would should may might must give get go see look come let thank stay keep need want know think make take hold wait watch listen".split())
for x in L:
    for sent in re.split(r"(?<=[.!?])\s+",x["text"].strip()):
        w=re.findall(r"[A-Za-z']+",sent)
        if not w: continue
        verbish=any(t.lower() in VERB or "'" in t for t in w)
        if len(w)<5 and not verbish: short+=1; frags.append(sent)
        elif len(w)>=5 and not any(t.lower() in FUNC for t in w): fails.append(f"telegraphic sentence (no function words): {sent}")
allowed=max(1,round(dur/30))
if short>allowed: fails.append(f"{short} verbless fragments (max {allowed} for {dur}s, one reaction line): {frags}")
def syl(w):
    w=w.lower(); v=re.findall(r"[aeiouy]+",w); n=len(v)-(1 if w.endswith("e") and len(v)>1 else 0); return max(1,n)
txt=" ".join(x["text"] for x in L); sents=max(1,len(re.findall(r"[.!?]",txt))); ws=re.findall(r"[A-Za-z']+",txt)
grade=0.39*len(ws)/sents+11.8*sum(syl(w) for w in ws)/max(1,len(ws))-15.59
if grade>9: warns.append(f"reading grade {grade:.1f} (aim 6 to 8)")
key=os.environ.get("OPENROUTER_API_KEY") or (open(os.path.expanduser("~/.openrouter_key")).read().strip() if os.path.exists(os.path.expanduser("~/.openrouter_key")) else None)
judge=None
if key:
    q=("You judge the spoken script of a short video ad. Definitions: CONVERSATIONAL means every line is a complete, natural sentence a warm storyteller or a real person would say out loud, with connecting words; clipped ad-speak, noun fragments or text-message shorthand ('Visibility nil.', 'Two falls.', 'Brand. Claim.') score 3 or lower even if punchy. LISTEN_ONLY means a listener with the screen off understands who, what is happening, why it matters and how the product helps. PRODUCT_LINE means the product is named inside a natural sentence that gives the reason this character uses it. PRODUCT_FIT means the product's use makes physical and story sense for this character and world (biology, scale, logic). Score each 1 to 10. Reply JSON only: {\"listen_only\":n,\"conversational\":n,\"product_line\":n,\"product_fit\":n,\"worst_line\":\"...\",\"why\":\"...\"}.\nStory context: "+d.get("context","")+"\nScript:\n"+"\n".join(f'{x["speaker"]}: {x["text"]}' for x in L))
    body={"model":"anthropic/claude-sonnet-4.5","temperature":0,"messages":[{"role":"user","content":q}]}
    try:
        r=json.load(urllib.request.urlopen(urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"}),timeout=90))
        t=r["choices"][0]["message"]["content"]; judge=json.loads(t[t.find("{"):t.rfind("}")+1])
        low=[k for k in ("listen_only","conversational","product_line","product_fit") if judge.get(k,0)<8]
        if low: fails.append(f"judge below 8 on {low}: worst line {judge.get('worst_line')!r}; why: {judge.get('why')}")
    except Exception as e: warns.append(f"judge unavailable: {str(e)[:120]}")
print(json.dumps({"words":words,"budget":round(budget),"speaker_changes":changes,"est_seconds":round(words/pace+0.4*changes+1.5,1),"reading_grade":round(grade,1),"judge":judge,"fails":fails,"warns":warns},indent=1))
sys.exit(1 if fails else 0)
