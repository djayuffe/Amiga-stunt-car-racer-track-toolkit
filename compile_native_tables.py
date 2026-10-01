#!/usr/bin/env python3
"""Compile native SCR X/Z and 128 Y-profile tables from a Track.cpp-style source.
Does not redistribute source tables; it converts a locally supplied source file.
"""
from pathlib import Path
import argparse,re,json
PIECES=(0,1,3,4,6,7,10)
def nums(s): return [int(x,16) for x in re.findall(r'0x([0-9a-fA-F]+)',s)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('-o','--out',default='native_tables.json');a=ap.parse_args()
 s=Path(a.source).read_text(errors='replace'); arrays={}
 pat=r'static\s+unsigned\s+char\s+([A-Za-z0-9_]+)\s*\[[^\]]*\]\s*=\s*\{(.*?)\};'
 for m in re.finditer(pat,s,re.S): arrays[m.group(1)]=nums(m.group(2))
 xz={}
 for i in PIECES:
  n=f'Amiga_Piece{i}_XZ'
  if n not in arrays: raise SystemExit(f'missing {n}')
  xz[str(i)]=arrays[n]
 mm=re.search(r'Amiga_Piece_Y\s*\[NUM_AMIGA_PIECE_Y\]\s*=\s*\{(.*?)\};',s,re.S)
 if not mm: raise SystemExit('missing Amiga_Piece_Y mapping')
 refs=re.findall(r'\{\s*([BW]\d+)\s*,\s*(TRUE|FALSE)\s*,\s*sizeof\([^)]*\)\s*\}',mm.group(1))
 if len(refs)!=128: raise SystemExit(f'expected 128 Y profiles, found {len(refs)}')
 y=[]
 for name,w in refs:
  if name not in arrays: raise SystemExit(f'missing {name}')
  y.append({'name':name,'words':w=='TRUE','raw':arrays[name]})
 out={'schema':'scr-native-tables-v1','xz_raw':xz,'y_raw':y}
 Path(a.out).write_text(json.dumps(out,separators=(',',':')))
 print(f'wrote {a.out}: {len(xz)} X/Z templates, {len(y)} Y profiles')
if __name__=='__main__': main()
