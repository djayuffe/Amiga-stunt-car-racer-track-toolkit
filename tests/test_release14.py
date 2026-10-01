import pathlib,sys
r=pathlib.Path(__file__).parents[1];sys.path.insert(0,str(r))
from scrtool.track import *;from scrtool.recover import resolve_overlaps;from scrtool.reinsert import *
assert [x["offset"] for x in resolve_overlaps([{"offset":10,"score":80},{"offset":20,"score":90},{"offset":1000,"score":70}])]==[20,1000]
t=Track(2,0,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,[0]*100,0,0);src=b"HEAD"+encode(t)+b"TAIL";u=decode(encode(t));u.xz[1]=163
p=make_patch(src,4,u);out=apply_patch(src,p);assert out[:4]==b"HEAD" and out[-4:]==b"TAIL" and decode(out[4:808]).xz[1]==163
print("release 1.4 overlap/reinsert: PASS")
