#!/usr/bin/env python3
"""Normalize emulator trace lines into evidence records.
Accepted lines:
MEMW <pc_hex> <addr_hex> <size> <value_hex>
MEMR <pc_hex> <addr_hex> <size> <value_hex>
IO   <pc_hex> <command_hex> <offset_hex> <length_hex> <data_addr_hex>
"""
import sys,json,re,pathlib
out=[]
for n,line in enumerate(pathlib.Path(sys.argv[1]).read_text().splitlines(),1):
 p=line.split()
 if not p or p[0].startswith("#"):continue
 try:
  if p[0] in ("MEMW","MEMR") and len(p)==5:
   out.append({"kind":p[0],"line":n,"pc":int(p[1],16),"address":int(p[2],16),"size":int(p[3],0),"value":int(p[4],16)})
  elif p[0]=="IO" and len(p)==6:
   out.append({"kind":"IO","line":n,"pc":int(p[1],16),"command":int(p[2],16),"offset":int(p[3],16),"length":int(p[4],16),"data_address":int(p[5],16)})
 except ValueError: raise SystemExit(f"bad trace line {n}: {line}")
print(json.dumps(out,indent=2))
