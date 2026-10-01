#!/usr/bin/env python3
"""Editor mesh generator for canonical 804-byte Stunt Car Racer tracks.
Uses confirmed native template metadata. Geometry is an editor reconstruction, not a claim of bit-exact Amiga vertices.
"""
from pathlib import Path
import argparse, json, math
from extract_tracks import parse
# Confirmed from Track.cpp Piece_Templates. Undefined native templates are retained but not meshed specially.
TEMPLATES={
0:dict(name='straight8',segments=8,type=0x00,curve_left=False,length_reduction=128,steering=0x20),
1:dict(name='curve_right8',segments=8,type=0x80,curve_left=False,length_reduction=135,steering=0x3e),
2:dict(name='undefined2',segments=0,type=0,curve_left=False,length_reduction=0,steering=0),
3:dict(name='curve_left8',segments=8,type=0xc0,curve_left=True,length_reduction=135,steering=0x3e),
4:dict(name='diagonal13',segments=13,type=0x40,curve_left=False,length_reduction=128,steering=0x20),
5:dict(name='undefined5',segments=0,type=0,curve_left=False,length_reduction=0,steering=0),
6:dict(name='curve_right9',segments=9,type=0x80,curve_left=False,length_reduction=122,steering=0x32),
7:dict(name='curve_left9',segments=9,type=0xc0,curve_left=True,length_reduction=122,steering=0x32),
8:dict(name='undefined8',segments=0,type=0,curve_left=False,length_reduction=0,steering=0),
9:dict(name='undefined9',segments=0,type=0,curve_left=False,length_reduction=0,steering=0),
10:dict(name='diagonal11',segments=11,type=0x40,curve_left=False,length_reduction=124,steering=0x20),
}
def enrich(t):
    for p in t['pieces']:
        p['native_template']=dict(TEMPLATES.get(p['template'],dict(name='unknown',segments=0,type=None)))
        p['right_line_colour_flag']=bool(p['right_y_id']&0x80)
        p['right_y_profile_index']=p['right_y_id']&0x7f
        p['left_y_word_storage']=bool(p['left_y_id']&0x80)
        p['left_y_profile_index']=p['left_y_id']&0x7f
    t['schema']='scr804-v3'; return t
def ribbon_obj(t,width=.75,grid=8.0,height_scale=1/256):
    # Smooth editor ribbon through native piece centres. Native metadata is emitted as comments.
    ps=t['pieces']; out=['# SCR v3 editor ribbon','# NOT bit-exact Amiga section geometry','o SCR_track']
    verts=[]; faces=[]
    n=len(ps)
    for i,p in enumerate(ps):
        prev=ps[(i-1)%n]; nxt=ps[(i+1)%n]
        x=p['grid_x']*grid; z=p['grid_z']*grid
        dx=(nxt['grid_x']-prev['grid_x']); dz=(nxt['grid_z']-prev['grid_z'])
        l=math.hypot(dx,dz) or 1; nx=-dz/l; nz=dx/l
        yl=p['left_y_shift']*height_scale; yr=p['right_y_shift']*height_scale
        verts += [(x+nx*width*grid,yl,z+nz*width*grid),(x-nx*width*grid,yr,z-nz*width*grid)]
        out.append(f"# piece {i} template={p['template']} profileL={p['left_y_profile_index']} profileR={p['right_y_profile_index']}")
    for v in verts: out.append('v %.6f %.6f %.6f'%v)
    for i in range(n):
        j=(i+1)%n; a=2*i+1;b=2*i+2;c=2*j+2;d=2*j+1
        faces.append((a,b,c,d))
    for f in faces: out.append('f '+' '.join(map(str,f)))
    return '\n'.join(out)+'\n'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('track');ap.add_argument('-o','--out',default='mesh_out');a=ap.parse_args()
    t=enrich(parse(Path(a.track).read_bytes()));o=Path(a.out);o.mkdir(parents=True,exist_ok=True)
    (o/'track.native.json').write_text(json.dumps(t,indent=2));(o/'track.editor.obj').write_text(ribbon_obj(t))
    print('wrote',o/'track.native.json','and',o/'track.editor.obj')
if __name__=='__main__':main()
