from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from extract_tracks import parse, obj_from_track
b=bytearray(804); b[0]=1; b[1]=0; b[2]=0x21; b[102]=0x80|3; b[202]=4; b[302]=5
b[402:404]=(0x0100).to_bytes(2,'big',signed=True); b[602:604]=(0x0200).to_bytes(2,'big',signed=True); b[802]=7; b[803]=8
t=parse(bytes(b)); p=t['pieces'][0]
assert (p['grid_x'],p['grid_z'],p['angle_quadrant'],p['template'])==(1,2,2,3)
assert p['left_y_shift']==256 and p['right_y_shift']==512
assert t['standard_boost']==7 and t['super_boost']==8
assert 'v ' in obj_from_track(t)
print('smoke: PASS')
