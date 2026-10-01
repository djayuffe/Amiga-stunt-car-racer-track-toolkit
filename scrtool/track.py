from dataclasses import dataclass,asdict
from .binary import Reader,Writer
from .errors import ValidationError
SIZE=804;N=100
@dataclass
class Track:
 sections:int;start:int;xz:list;config:list;left_profile:list;right_profile:list;left_height:list;right_height:list;boost:int;super_boost:int
 def validate(self):
  if not 0<=self.sections<=N:raise ValidationError("sections")
  if self.sections and not 0<=self.start<self.sections:raise ValidationError("start")
  for n in ("xz","config","left_profile","right_profile","left_height","right_height"):
   if len(getattr(self,n))!=N:raise ValidationError(n+" length")
  for a in (self.xz,self.config,self.left_profile,self.right_profile):
   if any(not 0<=v<=255 for v in a):raise ValidationError("byte range")
  for a in (self.left_height,self.right_height):
   if any(not 0<=v<=65535 for v in a):raise ValidationError("word range")
  if not 0<=self.boost<=255 or not 0<=self.super_boost<=255:raise ValidationError("boost")
def decode(b):
 if len(b)!=SIZE:raise ValidationError(f"track must be {SIZE} bytes")
 r=Reader(b);t=Track(r.u8(),r.u8(),list(r.bytes(N)),list(r.bytes(N)),list(r.bytes(N)),list(r.bytes(N)),[r.u16be() for _ in range(N)],[r.u16be() for _ in range(N)],r.u8(),r.u8());t.validate();return t
def encode(t):
 t.validate();w=Writer();w.u8(t.sections);w.u8(t.start)
 for a in (t.xz,t.config,t.left_profile,t.right_profile):w.bytes(bytes(a))
 for a in (t.left_height,t.right_height):
  for v in a:w.u16be(v)
 w.u8(t.boost);w.u8(t.super_boost);b=w.finish();assert len(b)==SIZE;return b
def editor_dict(t):
 return {"schema":"scr-editor-v1","native":asdict(t),"pieces":[{"index":i,"x":t.xz[i]>>4,"z":t.xz[i]&15,"config":t.config[i],"geometry":t.config[i]&15,"quadrant":(t.config[i]>>4)&3} for i in range(t.sections)]}

def from_editor_dict(d):
 if d.get("schema")!="scr-editor-v1":raise ValidationError("unsupported editor schema")
 n=d.get("native")
 if not isinstance(n,dict):raise ValidationError("missing native backing")
 t=Track(**n);t.validate();pieces=d.get("pieces")
 if not isinstance(pieces,list) or len(pieces)!=t.sections:raise ValidationError("piece count mismatch")
 seen=set()
 for p in pieces:
  i=p.get("index")
  if not isinstance(i,int) or not 0<=i<t.sections or i in seen:raise ValidationError("invalid/duplicate piece index")
  seen.add(i);x=p.get("x");z=p.get("z");cfg=p.get("config")
  if not isinstance(x,int) or not 0<=x<=15 or not isinstance(z,int) or not 0<=z<=15:raise ValidationError("grid coordinate")
  if not isinstance(cfg,int) or not 0<=cfg<=255:raise ValidationError("config")
  t.xz[i]=(x<<4)|z;t.config[i]=cfg
  for key,attr in (("left_profile","left_profile"),("right_profile","right_profile"),("left_height","left_height"),("right_height","right_height")):
   if key in p:getattr(t,attr)[i]=p[key]
 t.validate();return t
