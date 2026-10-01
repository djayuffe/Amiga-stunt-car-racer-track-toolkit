import argparse,json,pathlib,sys
from .transaction_build import build_from_editors,merge,reverse_transaction
from .io import read_file,atomic_json,sha256
def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="cmd",required=True)
 q=s.add_parser("build");q.add_argument("source");q.add_argument("output");q.add_argument("editors",nargs="+")
 q=s.add_parser("merge");q.add_argument("source");q.add_argument("output");q.add_argument("transactions",nargs="+")
 q=s.add_parser("reverse");q.add_argument("modified");q.add_argument("transaction");q.add_argument("output")
 a=p.parse_args(argv)
 try:
  if a.cmd=="build":atomic_json(a.output,build_from_editors(read_file(a.source),a.editors))
  elif a.cmd=="merge":
   b=read_file(a.source);txs=[json.loads(pathlib.Path(x).read_text()) for x in a.transactions];atomic_json(a.output,merge(sha256(b),*txs))
  else:
   b=read_file(a.modified);tx=json.loads(pathlib.Path(a.transaction).read_text());atomic_json(a.output,reverse_transaction(b,tx))
 except Exception as e:print("ERROR:",e,file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
