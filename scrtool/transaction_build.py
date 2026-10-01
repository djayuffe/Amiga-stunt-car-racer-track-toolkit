import json,pathlib
from .track import from_editor_dict,SIZE
from .reinsert import make_patch
from .io import sha256
from .errors import ValidationError,EvidenceError
def build_from_editors(source,editor_paths):
 patches=[]
 for path in editor_paths:
  d=json.loads(pathlib.Path(path).read_text());meta=d.get("source")
  if not isinstance(meta,dict):raise ValidationError(f"{path}: missing source metadata")
  if meta.get("sha256")!=sha256(source):raise EvidenceError(f"{path}: source hash mismatch")
  o=meta.get("offset")
  if not isinstance(o,int) or o<0 or o+SIZE>len(source):raise ValidationError(f"{path}: offset")
  native=source[o:o+SIZE]
  if meta.get("native_sha256")!=sha256(native):raise EvidenceError(f"{path}: native hash mismatch")
  patches.append(make_patch(source,o,from_editor_dict(d)))
 return {"schema":"scr-transaction-v1","source_sha256":sha256(source),"patches":patches}
def merge(source_sha,*txs):
 out={"schema":"scr-transaction-v1","source_sha256":source_sha,"patches":[]};seen=set()
 for tx in txs:
  if tx.get("schema")!="scr-transaction-v1" or tx.get("source_sha256")!=source_sha:raise EvidenceError("transaction source mismatch")
  for p in tx.get("patches",[]):
   o=p["offset"]
   if o in seen:raise ValidationError(f"duplicate offset {o}")
   seen.add(o);out["patches"].append(p)
 return out
def reverse_transaction(source_after,tx):
 if tx.get("schema")!="scr-transaction-v1":raise ValidationError("transaction schema")
 rev=[]
 for p in tx["patches"]:
  o=p["offset"];before=bytes.fromhex(p["before_hex"]);after=bytes.fromhex(p["after_hex"])
  if source_after[o:o+SIZE]!=after:raise EvidenceError(f"postimage mismatch at {o}")
  rev.append({"schema":"scr-reinsert-v1","source_sha256":sha256(source_after),"offset":o,"before_sha256":p["after_sha256"],"after_sha256":p["before_sha256"],"before_hex":p["after_hex"],"after_hex":p["before_hex"]})
 return {"schema":"scr-transaction-v1","source_sha256":sha256(source_after),"patches":rev}
