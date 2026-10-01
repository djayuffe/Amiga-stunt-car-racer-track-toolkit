import argparse,json,pathlib,struct
p=argparse.ArgumentParser();p.add_argument("binary");p.add_argument("abi");p.add_argument("obj");a=p.parse_args()
b=pathlib.Path(a.binary).read_bytes();q=json.loads(pathlib.Path(a.abi).read_text());V=[];F=[]
v=q["vertices"];f=q["faces"]
for i in range(v["count"]):
 o=v["offset"]+i*v["stride"]
 if o+6>len(b):raise SystemExit("vertex OOB")
 V.append(struct.unpack_from(">hhh",b,o))
for i in range(f["count"]):
 o=f["offset"]+i*f["stride"];n=b[o]
 if n<3 or n>f.get("max_vertices",8):raise SystemExit("invalid face size")
 ix=list(b[o+1:o+1+n])
 if len(ix)!=n or any(x>=len(V) for x in ix):raise SystemExit("face index OOB")
 F.append(ix)
s=["# ABI-proven indexed mesh"]+[f"v {x} {y} {z}" for x,y,z in V]+["f "+" ".join(str(x+1) for x in q) for q in F]
pathlib.Path(a.obj).write_text("\n".join(s)+"\n");print(f"{len(V)} vertices, {len(F)} faces")
