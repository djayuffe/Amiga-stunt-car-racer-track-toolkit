#!/usr/bin/env python3
import pathlib,json,hashlib,sys
b=bytearray(pathlib.Path(sys.argv[1]).read_bytes());m=json.loads(pathlib.Path(sys.argv[2]).read_text())
if hashlib.sha256(b).hexdigest()!=m["input_sha256"]:raise SystemExit("REFUSED: SHA mismatch")
for p in m["patches"]:
 o=int(p["offset"]);a=bytes.fromhex(p["before_hex"]);z=bytes.fromhex(p["after_hex"])
 if len(a)!=len(z) or b[o:o+len(a)]!=a:raise SystemExit(f"REFUSED at {o:#x}")
 b[o:o+len(z)]=z
pathlib.Path(m["output"]).write_bytes(b);print("patch applied")
