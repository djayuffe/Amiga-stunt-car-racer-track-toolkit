#!/usr/bin/env python3
from pathlib import Path
import argparse, json, struct
TRACK_SIZE=804; N=100
NAMES=['LittleRamp','SteppingStones','HumpBack','BigRamp','SkiJump','DrawBridge','HighJump','RollerCoaster']
def s16(b,o): return struct.unpack_from('>h',b,o)[0]
def parse(buf):
    if len(buf)!=TRACK_SIZE: raise ValueError('track must be 804 bytes')
    i=0; n=buf[i]; i+=1; start=buf[i]; i+=1
    xz=list(buf[i:i+N]); i+=N; ang=list(buf[i:i+N]); i+=N
    ly=list(buf[i:i+N]); i+=N; ry=list(buf[i:i+N]); i+=N
    ls=[s16(buf,i+2*j) for j in range(N)]; i+=2*N
    rs=[s16(buf,i+2*j) for j in range(N)]; i+=2*N
    std,sup=buf[i],buf[i+1]
    pieces=[]
    for j in range(min(n,N)):
        c=xz[j]; a=ang[j]
        pieces.append({'index':j,'grid_x':c&15,'grid_z':(c>>4)&15,'angle_quadrant':(a>>6)&3,
          'rotate_180':bool(a&0x10),'template':a&15,'left_y_id':ly[j], 'right_y_id':ry[j],
          'left_y_profile_index':ly[j]&0x7f, 'left_y_word_storage':bool(ly[j]&0x80),
          'right_y_profile_index':ry[j]&0x7f, 'right_line_colour_flag':bool(ry[j]&0x80),
          'left_y_shift':ls[j],'right_y_shift':rs[j]})
    return {'num_pieces':n,'start_piece':start,'standard_boost':std,'super_boost':sup,'pieces':pieces,
            'raw_arrays':{'xz':xz,'angle_template':ang,'left_y_id':ly,'right_y_id':ry,'left_y_shift':ls,'right_y_shift':rs}}
def plausible(buf):
    if len(buf)!=TRACK_SIZE: return False
    n,start=buf[0],buf[1]
    if not (8<=n<=100 and start<n): return False
    xz=buf[2:102]; ang=buf[102:202]
    # Active slots should occupy a 16x16 grid and templates use low nibble; score continuity on grid.
    pts=[(v&15,v>>4) for v in xz[:n]]
    jumps=sum(abs(pts[i][0]-pts[i-1][0])+abs(pts[i][1]-pts[i-1][1])>3 for i in range(1,n))
    return jumps <= max(3,n//8) and sum((v&15)<=15 for v in ang[:n])==n
def obj_from_track(t, scale=1.0):
    # Logical centerline preview. Heights use mean overall side shift; exact road cross-section requires geometry DB/profile tables.
    out=['# Stunt Car Racer logical track centerline','o track_centerline']
    for p in t['pieces']:
        y=(p['left_y_shift']+p['right_y_shift'])/2.0/256.0
        out.append(f"v {p['grid_x']*scale:.6f} {y*scale:.6f} {p['grid_z']*scale:.6f}")
    if t['pieces']:
        out.append('l '+' '.join(str(i+1) for i in range(len(t['pieces'])))+' 1')
    return '\n'.join(out)+'\n'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('-o','--out',default='out'); ap.add_argument('--scan',action='store_true')
    a=ap.parse_args(); b=Path(a.input).read_bytes(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    if len(b)==TRACK_SIZE:
        hits=[(0,b)]
    elif a.scan:
        hits=[]
        for o in range(0,len(b)-TRACK_SIZE+1):
            q=b[o:o+TRACK_SIZE]
            if plausible(q): hits.append((o,q))
    else: raise SystemExit('Input is not 804 bytes; use --scan for decoded RAM/binary images')
    manifest=[]
    for k,(o,q) in enumerate(hits):
        t=parse(q); stem=f'track_{k:02d}_off_{o:08x}'
        (out/(stem+'.bin')).write_bytes(q)
        (out/(stem+'.json')).write_text(json.dumps(t,indent=2))
        (out/(stem+'.obj')).write_text(obj_from_track(t))
        manifest.append({'offset':o,'stem':stem,'num_pieces':t['num_pieces'],'start_piece':t['start_piece']})
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(f'{len(hits)} candidate track(s) exported to {out}')
if __name__=='__main__': main()
