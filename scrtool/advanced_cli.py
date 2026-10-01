import argparse,pathlib,json,sys
from .track import decode,encode,from_editor_dict,editor_dict
from .bank import split_bank,join_bank
from .diff import diff,apply
from .io import read_file,atomic_write,atomic_json,sha256
def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
 for n,args in [("validate-track",["input"]),("bank-split",["input","output_dir"]),("bank-join",["input_dir","output"]),("diff",["before","after","output"]),("patch",["input","patch","output"])]:
  q=s.add_parser(n)
  for x in args:q.add_argument(x)
 a=p.parse_args(argv)
 try:
  if a.cmd=="validate-track":
   b=read_file(a.input);t=decode(b);print(json.dumps({"valid":True,"sha256":sha256(b),"sections":t.sections}))
  elif a.cmd=="bank-split":
   ts=split_bank(read_file(a.input));d=pathlib.Path(a.output_dir);d.mkdir(parents=True,exist_ok=True);m={"schema":"scr-bank-v1","tracks":[]}
   for i,t in enumerate(ts):
    o=d/f"track_{i:03d}.json";atomic_json(o,editor_dict(t));m["tracks"].append({"index":i,"file":o.name,"sha256":sha256(encode(t))})
   atomic_json(d/"manifest.json",m)
  elif a.cmd=="bank-join":
   d=pathlib.Path(a.input_dir);m=json.loads((d/"manifest.json").read_text());ts=[]
   for e in m["tracks"]:
    t=from_editor_dict(json.loads((d/e["file"]).read_text()))
    if sha256(encode(t))!=e["sha256"]:raise ValueError("manifest hash mismatch")
    ts.append(t)
   atomic_write(a.output,join_bank(ts))
  elif a.cmd=="diff":atomic_json(a.output,{"schema":"scr-track-patch-v1","changes":diff(decode(read_file(a.before)),decode(read_file(a.after)))})
  else:
   q=json.loads(pathlib.Path(a.patch).read_text())
   if q.get("schema")!="scr-track-patch-v1":raise ValueError("patch schema")
   atomic_write(a.output,encode(apply(decode(read_file(a.input)),q["changes"])))
 except Exception as e:print("ERROR:",e,file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
