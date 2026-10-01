import pathlib,sys
r=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(r))
from scrtool.track import *;from scrtool.bank import *;from scrtool.diff import diff,apply
a=Track(2,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,0,0);b=decode(encode(a));b.xz[1]=171;b.left_height[1]=1234
x=join_bank([a,b]);assert join_bank(split_bank(x))==x
try:split_bank(x+b"x");assert False
except ValidationError:pass
assert encode(apply(a,diff(a,b)))==encode(b)
print("release 1.2 bank/diff: PASS")
