#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re,hashlib
ap=argparse.ArgumentParser(); ap.add_argument('adf'); ap.add_argument('-o','--out',default='probe.json'); a=ap.parse_args()
b=Path(a.adf).read_bytes();
ranges=[]; active=[]
for i in range(len(b)//512):
 if any(b[i*512:(i+1)*512]): active.append(i)
if active:
 s=p=active[0]
 for x in active[1:]:
  if x!=p+1:ranges.append([s,p]);s=x
  p=x
 ranges.append([s,p])
strings=[]
for m in re.finditer(rb'[ -~]{8,}',b):
 s=m.group().decode('latin1')
 if any(k in s.upper() for k in ('TRACK','RAMP','JUMP','BRIDGE','ROLLER','MOVE.','FETCH','PROTECTION')):
  strings.append({'offset':m.start(),'text':s[:240]})
obj={'size':len(b),'sha256':hashlib.sha256(b).hexdigest(),'boot_magic':b[:4].decode('latin1','replace'),'nonzero_block_ranges':ranges,'interesting_strings':strings}
Path(a.out).write_text(json.dumps(obj,indent=2)); print(a.out)
