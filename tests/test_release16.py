import pathlib,sys,tempfile,json
r=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(r))
from scrtool.track import *;from scrtool.io import sha256,atomic_json;from scrtool.transaction_build import *;from scrtool.transaction import apply_transaction
a=Track(2,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,0,0);src=b"H"+encode(a)+b"M"+encode(a)+b"T"
with tempfile.TemporaryDirectory() as td:
 d=pathlib.Path(td);paths=[]
 for n,o in enumerate((1,806)):
  q=editor_dict(decode(src[o:o+804]));q["source"]={"sha256":sha256(src),"offset":o,"native_sha256":sha256(src[o:o+804])};q["pieces"][0]["x"]=n+1;p=d/f"{n}.json";atomic_json(p,q);paths.append(p)
 tx=build_from_editors(src,paths);mod,receipt=apply_transaction(src,tx);rev=reverse_transaction(mod,tx);orig,_=apply_transaction(mod,rev);assert orig==src
 t1={**tx,"patches":[tx["patches"][0]]};t2={**tx,"patches":[tx["patches"][1]]};assert len(merge(sha256(src),t1,t2)["patches"])==2
 try:merge(sha256(src),t1,t1);assert False
 except ValidationError:pass
print("release 1.6 build/reverse/merge: PASS")
