from dataclasses import dataclass
from .errors import ValidationError,EvidenceError
from .io import sha256
ADF_SIZE=901120;SECTOR=512
@dataclass
class ADF:
 data:bytes
 def validate(self):
  if len(self.data)!=ADF_SIZE:raise ValidationError(f"expected {ADF_SIZE}-byte image")
 @property
 def sectors(self):self.validate();return [self.data[i:i+SECTOR] for i in range(0,len(self.data),SECTOR)]
 def fingerprint(self):return sha256(self.data)
 def guarded_patch(self,expected_sha,patches):
  self.validate()
  if self.fingerprint()!=expected_sha:raise EvidenceError("input SHA-256 mismatch")
  b=bytearray(self.data)
  for p in patches:
   o=int(p["offset"]);x=bytes.fromhex(p["before_hex"]);y=bytes.fromhex(p["after_hex"])
   if len(x)!=len(y):raise ValidationError("size-changing patch")
   if o<0 or o+len(x)>len(b):raise ValidationError("patch OOB")
   if b[o:o+len(x)]!=x:raise EvidenceError(f"before mismatch at {o:#x}")
   b[o:o+len(y)]=y
  return ADF(bytes(b))
