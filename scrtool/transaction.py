from .track import SIZE,decode
from .io import sha256
from .errors import ValidationError,EvidenceError
def validate_transaction(source,tx):
 if tx.get("schema")!="scr-transaction-v1" or sha256(source)!=tx.get("source_sha256"):raise EvidenceError("schema/source mismatch")
 ps=tx.get("patches")
 if not isinstance(ps,list) or not ps:raise ValidationError("patches")
 ranges=[];v=[]
 for i,p in enumerate(ps):
  o=p.get("offset");x=bytes.fromhex(p["before_hex"]);y=bytes.fromhex(p["after_hex"])
  if not isinstance(o,int) or o<0 or o+SIZE>len(source) or len(x)!=SIZE or len(y)!=SIZE:raise ValidationError(f"patch {i} bounds/size")
  if source[o:o+SIZE]!=x or sha256(x)!=p["before_sha256"] or sha256(y)!=p["after_sha256"]:raise EvidenceError(f"patch {i} preimage/hash")
  decode(y);a,b=o,o+SIZE
  if any(not (b<=c or a>=d) for c,d in ranges):raise ValidationError(f"patch {i} overlap")
  ranges.append((a,b));v.append((o,x,y))
 return v
def apply_transaction(source,tx):
 v=validate_transaction(source,tx);out=bytearray(source);r={"schema":"scr-transaction-receipt-v1","source_sha256":sha256(source),"patches":[]}
 for o,x,y in sorted(v):
  out[o:o+SIZE]=y;r["patches"].append({"offset":o,"before_sha256":sha256(x),"after_sha256":sha256(y)})
 out=bytes(out);r["output_sha256"]=sha256(out);r["bytes"]=len(out);return out,r
