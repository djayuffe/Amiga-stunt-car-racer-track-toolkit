#!/usr/bin/env python3
import pathlib,struct,argparse
a=argparse.ArgumentParser();a.add_argument("input");a.add_argument("output");a.add_argument("--offset",type=lambda x:int(x,0),required=True);a.add_argument("--vertices",type=int,required=True);q=a.parse_args()
b=pathlib.Path(q.input).read_bytes();s=["# candidate points; topology intentionally unknown"]
for i in range(q.vertices):
 x,y,z=struct.unpack_from(">hhh",b,q.offset+6*i);s.append(f"v {x} {y} {z}")
pathlib.Path(q.output).write_text("\n".join(s)+"\n")
