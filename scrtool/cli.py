import argparse,json,pathlib,sys
from .track import decode,encode,editor_dict,Track,from_editor_dict
from .adf import ADF
from .io import read_file,atomic_write,atomic_json,sha256
from .errors import SCRToolError,ValidationError
def ensure_target(p,force):
 if pathlib.Path(p).exists() and not force:raise ValidationError(f"output exists: {p}; use --force")
def main(argv=None):
 p=argparse.ArgumentParser(prog="scrtool");p.add_argument("--force",action="store_true");s=p.add_subparsers(dest="cmd",required=True)
 for n in ("track-decode","track-encode"):
  q=s.add_parser(n);q.add_argument("input");q.add_argument("output")
 q=s.add_parser("track-batch-decode");q.add_argument("input_dir");q.add_argument("output_dir")
 q=s.add_parser("adf-info");q.add_argument("input")
 q=s.add_parser("adf-patch");q.add_argument("input");q.add_argument("manifest");q.add_argument("output")
 a=p.parse_args(argv)
 try:
  if a.cmd=="track-decode":
   ensure_target(a.output,a.force);atomic_json(a.output,editor_dict(decode(read_file(a.input,804))))
  elif a.cmd=="track-encode":
   ensure_target(a.output,a.force);d=json.loads(pathlib.Path(a.input).read_text());t=from_editor_dict(d) if "schema" in d else Track(**d.get("native",d));atomic_write(a.output,encode(t))
  elif a.cmd=="track-batch-decode":
   src=pathlib.Path(a.input_dir);dst=pathlib.Path(a.output_dir)
   if not src.is_dir():raise ValidationError("input_dir is not a directory")
   dst.mkdir(parents=True,exist_ok=True);manifest={"schema":"scr-batch-v1","files":[]}
   for f in sorted(x for x in src.iterdir() if x.is_file()):
    b=read_file(f)
    if len(b)!=804:continue
    o=dst/(f.stem+".json")
    if o.exists() and not a.force:raise ValidationError(f"output exists: {o}; use --force")
    t=decode(b);atomic_json(o,editor_dict(t));manifest["files"].append({"source":f.name,"output":o.name,"sha256":sha256(b),"sections":t.sections})
   atomic_json(dst/"manifest.json",manifest)
  elif a.cmd=="adf-info":
   x=ADF(read_file(a.input,901120));x.validate();print(json.dumps({"bytes":len(x.data),"sectors":len(x.sectors),"sha256":x.fingerprint()},indent=2))
  else:
   ensure_target(a.output,a.force);x=ADF(read_file(a.input,901120));m=json.loads(pathlib.Path(a.manifest).read_text());atomic_write(a.output,x.guarded_patch(m["input_sha256"],m["patches"]).data)
 except (SCRToolError,OSError,json.JSONDecodeError) as e:print(f"ERROR: {e}",file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
