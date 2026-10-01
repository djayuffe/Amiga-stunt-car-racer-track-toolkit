#!/usr/bin/env python3
import pathlib,struct,json,argparse
a=argparse.ArgumentParser();a.add_argument("binary");a.add_argument("candidate_json");a.add_argument("obj");a.add_argument("--index",type=int,default=0);q=a.parse_args()
b=pathlib.Path(q.binary).read_bytes();c=json.loads(pathlib.Path(q.candidate_json).read_text())[q.index]
V=[struct.unpack_from(">hhh",b,c["vertex_base"]+i*c["vertex_stride"]) for i in range(c["vertex_count"])]
p=c["face_base"];F=[]
while len(F)<c["face_count"]:
 n=b[p];F.append(list(b[p+1:p+1+n]));p+=1+n
 if p&1 and p<len(b) and b[p]==0:p+=1
s=["# scanned ABI candidate"]+[f"v {x} {y} {z}" for x,y,z in V]+["f "+" ".join(str(i+1) for i in f) for f in F]
pathlib.Path(q.obj).write_text("\n".join(s)+"\n");print(len(V),len(F))
