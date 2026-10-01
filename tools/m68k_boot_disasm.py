#!/usr/bin/env python3
import pathlib,struct,sys
def sw(x): return x-65536 if x&0x8000 else x
def sl(x): return x-4294967296 if x&0x80000000 else x
def dis(b,base=0):
 pc=0; out=[]
 while pc+2<=len(b):
  at=pc; w=struct.unpack_from(">H",b,pc)[0];pc+=2;s=None
  if w==0x4e75:s="RTS"
  elif w==0x4e73:s="RTE"
  elif w==0x4e71:s="NOP"
  elif w==0x4e70:s="RESET"
  elif w==0x4eae and pc+2<=len(b):
   d=sw(struct.unpack_from(">H",b,pc)[0]);pc+=2;s=f"JSR {d}(A6)"
  elif w==0x4eee and pc+2<=len(b):
   d=sw(struct.unpack_from(">H",b,pc)[0]);pc+=2;s=f"JMP {d}(A6)"
  elif w==0x4ef9 and pc+4<=len(b):
   a=struct.unpack_from(">I",b,pc)[0];pc+=4;s=f"JMP ${a:08X}"
  elif w==0x4eb9 and pc+4<=len(b):
   a=struct.unpack_from(">I",b,pc)[0];pc+=4;s=f"JSR ${a:08X}"
  elif (w&0xff00)==0x6000:
   cc=["BRA","BSR","BHI","BLS","BCC","BCS","BNE","BEQ","BVC","BVS","BPL","BMI","BGE","BLT","BGT","BLE"][(w>>8)&15]
   d=w&255
   if d==0 and pc+2<=len(b):d=sw(struct.unpack_from(">H",b,pc)[0]);pc+=2
   else:d=d-256 if d&128 else d
   s=f"{cc} ${base+pc+d:08X}"
  elif (w&0xf100)==0x7000:
   d=w&255;d=d-256 if d&128 else d;s=f"MOVEQ #{d},D{(w>>9)&7}"
  elif w==0x203c and pc+4<=len(b):
   v=struct.unpack_from(">I",b,pc)[0];pc+=4;s=f"MOVE.L #${v:08X},D0"
  elif w==0x2f09:s="MOVE.L A1,-(SP)"
  elif w==0x2f08:s="MOVE.L A0,-(SP)"
  elif w==0x2c78 and pc+2<=len(b):
   a=struct.unpack_from(">H",b,pc)[0];pc+=2;s=f"MOVEA.L ${a:04X}.W,A6"
  raw=b[at:pc].hex()
  out.append(f"{base+at:08X}: {raw:<14} {s or f'DC.W ${w:04X}'}")
 return out
if __name__=="__main__":
 b=pathlib.Path(sys.argv[1]).read_bytes(); print("\n".join(dis(b)))
