#!/usr/bin/env python3
"""Native-coordinate SCR mesh reconstruction from canonical 804-byte track + compiled tables."""
from pathlib import Path
import argparse,json,struct
from extract_tracks import parse
from native_mesh import TEMPLATES,enrich
PC_FACTOR=2; CUBE=0x800; TRACK_BOTTOM_Y=-0x1000

def s16le(a,b):
 v=a|(b<<8); return v-0x10000 if v&0x8000 else v

def decode_tables(t):
 xz={}
 for k,raw in t['xz_raw'].items(): xz[int(k)]=[(s16le(*raw[i:i+2]),s16le(*raw[i+2:i+4])) for i in range(0,len(raw),4)]
 ys=[]
 for p in t['y_raw']:
  r=p['raw']; q=[]
  if p['words']:
   for i in range(0,len(r),2): q.append(((r[i]&0x7f)<<8)|r[i+1])
  else:
   for b in r: q.append(((b<<1)&0xe0)|((b&0x0f)<<8))
  ys.append(q)
 return xz,ys

def rot(x,z,q):
 if q==0:return x,z
 if q==1:return z,CUBE-x
 if q==2:return CUBE-x,CUBE-z
 return CUBE-z,x

def build(track,tables):
 xzt,ys=decode_tables(tables); pieces=[]
 for p in track['pieces']:
  tid=p['template']; meta=TEMPLATES.get(tid); n=meta['segments'] if meta else 0
  if not n or tid not in xzt: raise ValueError(f'unsupported template {tid} at piece {p["index"]}')
  pairs=xzt[tid]; need=2*(n+1)
  if len(pairs)<need: raise ValueError(f'template {tid} short')
  pairs=pairs[:need]
  if p['rotate_180']: pairs=list(reversed(pairs))
  verts=[]
  for i in range(n+1):
   lx,lz=rot(*pairs[2*i],p['angle_quadrant']); rx,rz=rot(*pairs[2*i+1],p['angle_quadrant'])
   li=p['left_y_profile_index']; ri=p['right_y_profile_index']
   if i>=len(ys[li]) or i>=len(ys[ri]): raise ValueError(f'Y profile short at piece {p["index"]}')
   ly=(ys[li][i]+p['left_y_shift'])*PC_FACTOR; ry=(ys[ri][i]+p['right_y_shift'])*PC_FACTOR
   verts.append([[lx*PC_FACTOR,ly,lz*PC_FACTOR],[rx*PC_FACTOR,ry,rz*PC_FACTOR],[lx*PC_FACTOR,TRACK_BOTTOM_Y,lz*PC_FACTOR],[rx*PC_FACTOR,TRACK_BOTTOM_Y,rz*PC_FACTOR]])
  pieces.append({'piece':p,'segments':n,'verts':verts})
 # Original seam closure: next start becomes previous end, translated between cubes.
 for i,cur in enumerate(pieces):
  prev=pieces[i-1]; cp=cur['piece']; pp=prev['piece']; dx=(cp['grid_x']-pp['grid_x'])*CUBE*PC_FACTOR; dz=(cp['grid_z']-pp['grid_z'])*CUBE*PC_FACTOR
  prev['verts'][-1]=[[v[0]+dx,v[1],v[2]+dz] for v in cur['verts'][0]]
 return pieces

def world_mesh(pieces):
 V=[]; road=[]; left=[]; right=[]; meta=[]
 for P in pieces:
  p=P['piece']; base=len(V); ox=p['grid_x']*CUBE*PC_FACTOR; oz=p['grid_z']*CUBE*PC_FACTOR
  for row in P['verts']:
   for v in row: V.append((v[0]+ox,v[1],v[2]+oz))
  for s in range(P['segments']):
   a=base+s*4; b=a+4
   road += [(a,b,b+1),(a,b+1,a+1)]
   left += [(a+2,b+2,b),(a+2,b,a)]
   right += [(a+1,b+1,b+3),(a+1,b+3,a+3)]
  meta.append({'index':p['index'],'first_vertex':base,'vertex_count':len(P['verts'])*4,'segments':P['segments'],'template':p['template']})
 return V,road,left,right,meta

def obj(V,groups):
 o=['# SCR native reconstructed track mesh']
 for v in V:o.append('v %d %d %d'%v)
 for name,F in groups:
  o.append('g '+name)
  for f in F:o.append('f '+' '.join(str(i+1) for i in f))
 return '\n'.join(o)+'\n'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('track');ap.add_argument('tables');ap.add_argument('-o','--out',default='exact_out');a=ap.parse_args()
 tr=enrich(parse(Path(a.track).read_bytes())); tb=json.loads(Path(a.tables).read_text()); P=build(tr,tb); V,R,L,Q,M=world_mesh(P); out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/'track.native.obj').write_text(obj(V,[('road',R),('left_side',L),('right_side',Q)]))
 (out/'track.mesh.json').write_text(json.dumps({'schema':'scr-native-mesh-v1','vertices':V,'road':R,'left_side':L,'right_side':Q,'pieces':M},separators=(',',':')))
 print(f'{len(V)} vertices, {len(R)+len(L)+len(Q)} triangles -> {out}')
if __name__=='__main__':main()
