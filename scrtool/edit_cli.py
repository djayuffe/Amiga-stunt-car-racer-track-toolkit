import argparse,pathlib,json,sys
from .track import from_editor_dict,editor_dict
from .reinsert import extract_at,make_patch,apply_patch
from .io import read_file,atomic_write,atomic_json,sha256
def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
 q=s.add_parser("extract-at");q.add_argument("source");q.add_argument("offset",type=lambda x:int(x,0));q.add_argument("output")
 q=s.add_parser("make-reinsert");q.add_argument("source");q.add_argument("offset",type=lambda x:int(x,0));q.add_argument("edited_json");q.add_argument("patch")
 q=s.add_parser("apply-reinsert");q.add_argument("source");q.add_argument("patch");q.add_argument("output")
 a=p.parse_args(argv)
 try:
  if a.cmd=="extract-at":
   b=read_file(a.source);t,raw=extract_at(b,a.offset);d=editor_dict(t);d["source"]={"sha256":sha256(b),"offset":a.offset,"native_sha256":sha256(raw)};atomic_json(a.output,d)
  elif a.cmd=="make-reinsert":atomic_json(a.patch,make_patch(read_file(a.source),a.offset,from_editor_dict(json.loads(pathlib.Path(a.edited_json).read_text()))))
  else:atomic_write(a.output,apply_patch(read_file(a.source),json.loads(pathlib.Path(a.patch).read_text())))
 except Exception as e:print("ERROR:",e,file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
