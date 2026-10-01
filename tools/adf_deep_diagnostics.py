#!/usr/bin/env python3
import pathlib,hashlib,collections,json,re,sys
b=pathlib.Path(sys.argv[1]).read_bytes()
if len(b)%512: raise SystemExit("not 512-byte aligned")
ss=[b[i:i+512] for i in range(0,len(b),512)]
g=collections.defaultdict(list)
for i,s in enumerate(ss):g[hashlib.sha1(s).hexdigest()].append(i)
strings=[{"offset":m.start(),"text":m.group().decode("ascii","replace")} for m in re.finditer(rb"[\x20-\x7e]{12,}",b)]
r={"bytes":len(b),"sectors":len(ss),"unique_sectors":len(g),
"largest_duplicate_groups":sorted(({"count":len(v),"sectors":v} for v in g.values()),key=lambda x:x["count"],reverse=True)[:20],
"strings":strings[:100]}
print(json.dumps(r,indent=2))
