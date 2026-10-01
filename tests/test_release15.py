import pathlib,sys
r=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(r))
from scrtool.track import *;from scrtool.reinsert import make_patch;from scrtool.transaction import *;from scrtool.io import sha256
a=Track(2,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,0,0);b=decode(encode(a));b.xz[1]=163
src=b"HEAD"+encode(a)+b"MID!"+encode(a)+b"TAIL";p1=make_patch(src,4,b);p2=make_patch(src,812,b);tx={"schema":"scr-transaction-v1","source_sha256":sha256(src),"patches":[p1,p2]}
out,r=apply_transaction(src,tx);assert len(out)==len(src) and out[:4]==b"HEAD" and out[808:812]==b"MID!" and out[-4:]==b"TAIL" and len(r["patches"])==2
try:validate_transaction(src,{**tx,"patches":[p1,p1]});assert False
except ValidationError:pass
print("release 1.5 transactions: PASS")
