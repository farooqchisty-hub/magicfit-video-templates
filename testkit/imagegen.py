"""Image model for test runs (Nano Banana Pro via treg). 
python3 imagegen.py --out path.png --size 9:16 --prompt "..." [--ref URL]...   (refs must be public URLs, max 14)
Prints the output path. Costs about $0.03 per image."""
import argparse,sys,os
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","lib")); from gen import gen
a=argparse.ArgumentParser(); a.add_argument("--out",required=True); a.add_argument("--size",default="9:16"); a.add_argument("--prompt",required=True); a.add_argument("--ref",action="append",default=[])
x=a.parse_args(); gen(x.prompt,x.ref,x.out,size=x.size,tag="papertest"); print(x.out)
