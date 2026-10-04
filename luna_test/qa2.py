import json,urllib.request,os,base64,concurrent.futures as cf,time
KEY=open(os.path.expanduser("~/.openrouter_key")).read().strip()
q="You are the QA checker for AI keyframes in a video ad. Rules: no real brands or logos other than the product (the product here is an Ember mug, its small 'ember' wordmark is allowed); no readable text or numbers drawn by the model except the fictional team name HALCYON and car number 27; no physics errors; no extra fingers. List every defect as JSON: {\"defects\":[\"...\"],\"pass\":true|false}."
def ask(m,f):
    img="data:image/jpeg;base64,"+base64.b64encode(open(f,"rb").read()).decode()
    body={"model":m,"max_tokens":4000,"messages":[{"role":"user","content":[{"type":"text","text":q},{"type":"image_url","image_url":{"url":img}}]}]}
    for a in range(2):
        try:
            r=json.load(urllib.request.urlopen(urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"}),timeout=150))
            return f,m,r["choices"][0]["message"]["content"].replace("\n"," ")[:450]
        except Exception as e: err=str(e)[:120]; time.sleep(3)
    return f,m,"ERR "+err
J=[(m,f) for f in ["take1_79.jpg","take2_logo.jpg"] for m in ["openai/gpt-6-luna","openai/gpt-6-luna-pro","anthropic/claude-sonnet-4.5"]]
with cf.ThreadPoolExecutor(6) as ex:
    for f,m,c in ex.map(lambda x:ask(*x),J): print("==",f,m.split('/')[-1],"\n  ",c,flush=True)
