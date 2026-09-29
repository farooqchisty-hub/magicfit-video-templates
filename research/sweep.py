import json,subprocess,os,sys,concurrent.futures as cf
os.environ["PATH"]=os.path.expanduser("~/.local/bin")+":"+os.environ["PATH"]
BRANDS=["Liquid Death","Olipop","poppi","AG1","Athletic Brewing","Magic Spoon","Oura","Ridge","MANSCAPED","Native","Dr. Squatch","Glossier","Rare Beauty","SKIMS","Gymshark","Allbirds","Bombas","Brooklinen","Our Place","Stanley 1913","Owala","CELSIUS","GHOST","Liquid I.V.","Gruns","Bloom Nutrition","YETI","Jones Road Beauty","Summer Fridays","Graza","Fishwife","Chamberlain Coffee","Nutrafol","Ritual","Seed Health","True Classic","Quince","Therabody","HexClad","Caraway","Blueland","Lovevery","Loop Earplugs","Huel","Surreal","Oatly","Dollar Shave Club","Mid-Day Squares","Starface","Touchland","Cometeer","Laneige","e.l.f. Cosmetics","Hismile","Snif","Arrae","Primal Kitchen","Feastables","Prime Hydration","Red Bull"]
def pull(b):
    fn=f"research/raw/{b.replace(' ','_').replace('.','')}.json"
    if os.path.exists(fn): return b,"cached"
    r=subprocess.run(["treg","call","scrapecreators.x.v1-facebook-adlibrary-company-ads","--query",f"companyName={b}","--query","country=US","--query","media_type=VIDEO","--query","trim=true"],capture_output=True,text=True)
    open(fn,"w").write(r.stdout); 
    try: n=len(json.loads(r.stdout).get("results",[]))
    except Exception: n="ERR "+r.stdout[:120]+r.stderr[:120]
    return b,n
with cf.ThreadPoolExecutor(8) as ex:
    for b,n in ex.map(pull,BRANDS): print(b,n)
