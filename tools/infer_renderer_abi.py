import collections,math
def infer(records):
 reads=[r for r in records if r.get("kind")=="MEMR"]
 if len(reads)<6:return {"status":"NEEDS_TRACE","reason":"fewer_than_6_memory_reads"}
 by=collections.defaultdict(list)
 for r in reads:by[r["pc"]].append(r)
 c=[]
 for pc,rs in by.items():
  aa=[r["address"] for r in rs];ds=[abs(y-x) for x,y in zip(aa,aa[1:]) if y!=x]
  g=0
  for d in ds:g=math.gcd(g,d)
  if 2<=g<=64:c.append({"pc":pc,"stride":g,"reads":len(rs),"min":min(aa),"max":max(aa)})
 if not c:return {"status":"NEEDS_TRACE","reason":"no_stable_stride"}
 c.sort(key=lambda x:(-x["reads"],x["stride"]));return {"status":"OK","candidates":c}
