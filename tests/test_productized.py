import pathlib,sys,tempfile
root=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(root))
from scrtool.track import *
from scrtool.binary import Reader
from scrtool.errors import *
from scrtool.adf import ADF,ADF_SIZE
from scrtool.io import atomic_write
t=Track(4,1,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,1,2);b=encode(t);assert encode(decode(b))==b
for n in (0,1,803,805):
 try:decode(bytes(n));assert False
 except ValidationError:pass
try:Reader(b"").u8();assert False
except TruncatedError:pass
a=ADF(bytes(ADF_SIZE));p=[{"offset":10,"before_hex":"0000","after_hex":"1234"}];z=a.guarded_patch(a.fingerprint(),p)
assert z.data[10:12]==bytes([0x12,0x34]) and a.data[10:12]==bytes([0,0])
try:a.guarded_patch("00"*32,p);assert False
except EvidenceError:pass
with tempfile.TemporaryDirectory() as d:
 q=pathlib.Path(d)/"x";atomic_write(q,b);assert q.read_bytes()==b
print("productized formats/file handling: PASS")
