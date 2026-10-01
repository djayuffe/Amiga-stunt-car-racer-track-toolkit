import pathlib,tempfile,os,json,hashlib
from .errors import ValidationError
def read_file(path,max_bytes=None):
 b=pathlib.Path(path).read_bytes()
 if max_bytes is not None and len(b)>max_bytes:raise ValidationError(f"file too large: {len(b)}")
 return b
def atomic_write(path,data):
 p=pathlib.Path(path);p.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(prefix=p.name+".",dir=p.parent)
 try:
  with os.fdopen(fd,"wb") as f:f.write(data);f.flush();os.fsync(f.fileno())
  os.replace(tmp,p)
 finally:
  try:os.unlink(tmp)
  except FileNotFoundError:pass
def atomic_json(path,obj):atomic_write(path,(json.dumps(obj,indent=2,sort_keys=True)+"\n").encode())
def sha256(b):return hashlib.sha256(b).hexdigest()
