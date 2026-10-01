import pathlib,json
def infer(a,b):
 if len(a)!=len(b):return {"status":"NEEDS_TRACE","reason":"length_mismatch"}
 if a==b:return {"status":"OK","transform":{"kind":"identity"}}
 x={u^v for u,v in zip(a,b)}
 if len(x)==1:return {"status":"OK","transform":{"kind":"xor8","key":next(iter(x))}}
 d={(v-u)&255 for u,v in zip(a,b)}
 if len(d)==1:return {"status":"OK","transform":{"kind":"add8","delta":next(iter(d))}}
 if len(a)%2==0:
  A=[int.from_bytes(a[i:i+2],"big") for i in range(0,len(a),2)];B=[int.from_bytes(b[i:i+2],"big") for i in range(0,len(b),2)]
  q={u^v for u,v in zip(A,B)}
  if len(q)==1:return {"status":"OK","transform":{"kind":"xor16be","key":next(iter(q))}}
 return {"status":"NEEDS_TRACE","reason":"no_supported_bijective_transform"}
def apply(b,t,inverse=False):
 k=t["kind"]
 if k=="identity":return b
 if k=="xor8":return bytes(x^t["key"] for x in b)
 if k=="add8":
  d=t["delta"]*(-1 if inverse else 1);return bytes((x+d)&255 for x in b)
 if k=="xor16be":
  return b"".join(((int.from_bytes(b[i:i+2],"big")^t["key"])&65535).to_bytes(2,"big") for i in range(0,len(b),2))
 raise ValueError(k)
