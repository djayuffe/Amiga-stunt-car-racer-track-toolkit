from .track import SIZE,decode,encode
from .io import sha256
from .errors import EvidenceError,ValidationError
def extract_at(source,offset):
 if offset<0 or offset+SIZE>len(source):raise ValidationError("track offset OOB")
 raw=source[offset:offset+SIZE];return decode(raw),raw
def make_patch(source,offset,new_track):
 _,old=extract_at(source,offset);new=encode(new_track)
 return {"schema":"scr-reinsert-v1","source_sha256":sha256(source),"offset":offset,"before_sha256":sha256(old),"after_sha256":sha256(new),"before_hex":old.hex(),"after_hex":new.hex()}
def apply_patch(source,p):
 if p.get("schema")!="scr-reinsert-v1" or sha256(source)!=p["source_sha256"]:raise EvidenceError("schema/source mismatch")
 o=int(p["offset"]);x=bytes.fromhex(p["before_hex"]);y=bytes.fromhex(p["after_hex"])
 if len(x)!=SIZE or len(y)!=SIZE or o<0 or o+SIZE>len(source):raise ValidationError("bounds/size")
 if source[o:o+SIZE]!=x or sha256(x)!=p["before_sha256"] or sha256(y)!=p["after_sha256"]:raise EvidenceError("patch hash/data mismatch")
 decode(y);b=bytearray(source);b[o:o+SIZE]=y;return bytes(b)
