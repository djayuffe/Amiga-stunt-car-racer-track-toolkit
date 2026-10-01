import argparse,json,pathlib,sys
from .transaction import validate_transaction,apply_transaction
from .io import read_file,atomic_write,atomic_json
def main(argv=None):
 p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("transaction");p.add_argument("--output");p.add_argument("--receipt");p.add_argument("--dry-run",action="store_true");a=p.parse_args(argv)
 try:
  b=read_file(a.source);tx=json.loads(pathlib.Path(a.transaction).read_text())
  if a.dry_run:print(json.dumps({"valid":True,"patches":len(validate_transaction(b,tx)),"bytes":len(b)}));return 0
  if not a.output:raise ValueError("--output required")
  out,r=apply_transaction(b,tx);atomic_write(a.output,out)
  if a.receipt:atomic_json(a.receipt,r)
 except Exception as e:print("ERROR:",e,file=sys.stderr);return 2
 return 0
if __name__=="__main__":raise SystemExit(main())
