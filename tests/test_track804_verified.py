import os,sys,random
sys.path.insert(0,os.path.join(os.path.dirname(__file__),"..","tools"))
from track804_codec_verified import *
random.seed(68000)
t=Track804(46,3,[random.randrange(256) for _ in range(100)],
[random.randrange(256) for _ in range(100)],[random.randrange(256) for _ in range(100)],
[random.randrange(256) for _ in range(100)],[random.randrange(65536) for _ in range(100)],
[random.randrange(65536) for _ in range(100)],17,231)
b=encode(t)
assert len(b)==804
assert b[0]==46 and b[1]==3
assert b[2:102]==bytes(t.road_xz)
assert b[102:202]==bytes(t.angle_template)
assert b[202:302]==bytes(t.left_y_id)
assert b[302:402]==bytes(t.right_y_id)
assert b[802:804]==bytes([17,231])
assert encode(decode(b))==b
print("verified 804-byte codec round-trip: PASS")
