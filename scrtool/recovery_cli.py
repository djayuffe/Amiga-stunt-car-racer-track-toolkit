import argparse,pathlib,json,sys,hashlib
from .recover import scan
from .track import SIZE,decode,editor_dict,encode,from_editor_dict
from .io import read_file,atomic_write,atomic_json,sha256
from .integrity import verify_release
def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
 q=s.add_parser("scan");q.add_argument("input");q.add_argument("--step",type=int,default=1);q.add_argument("--min-score",type=int,default=60);q.add_argument("-o","--output")
 q=s.add_parser("extract");q.add_argument("input");q.add_argument("output_dir");q.add_argument("--step",type=int,default=1);q.add_argument("--min-score",type=int,default=60)
 q=s.add_parser("verify-release");q.add_argument("root")
 q=s.add_parser("reseal-bank");q.add_argument("dir")
 a=p.parse_args(argv)
 try:
  if a.cmd=="scan":
   r=scan(read_file(a.input),a.step,a.min_score);o={"schema":"scr-recovery-scan-v1","candidates":r}
   if a.output:atomic_json(a.output,o)
   else:print(json.dumps(o,indent=2))
  elif a.cmd=="extract":
   b=read_file(a.input);d=pathlib.Path(a.output_dir);d.mkdir(parents=True,exist_ok=True);r=scan(b,a.step,a.min_score);m={"schema":"scr-recovered-v1","files":[]}
   for n,c in enumerate(r):
    raw=b[c["offset"]:c["offset"]+SIZE];name=f"{n:04d}_off_{c['offset']:08x}_{sha256(raw)[:12]}.bin";atomic_write(d/name,raw)
    m["files"].append({**c,"file":name,"sha256":sha256(raw)})
   atomic_json(d/"recovery_manifest.json",m)
  elif a.cmd=="verify-release":
   r=verify_release(a.root);print(json.dumps(r,indent=2));return 0 if r["valid"] else 3
  else:
   d=pathlib.Path(a.dir);m=json.loads((d/"manifest.json").read_text())
   for e in m["tracks"]:
    t=from_editor_dict(json.loads((d/e["file"]).read_text()));e["sha256"]=sha256(encode(t))
   m["resealed"]=True;atomic_json(d/"manifest.json",m)
 except Exception as e:print("ERROR:",e,file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
