from .track import decode,SIZE
def score_track(b,offset=0):
 if offset<0 or offset+SIZE>len(b):return None
 x=b[offset:offset+SIZE]
 try:t=decode(x)
 except Exception:return None
 score=0;why=[]
 if 1<=t.sections<=100:score+=30;why.append("section_count")
 if t.sections==0 or t.start<t.sections:score+=15;why.append("start_range")
 active=t.xz[:t.sections]
 if active and len(set(active))>1:score+=15;why.append("xz_variation")
 cfg=t.config[:t.sections]
 if cfg and sum((v&15)<=10 for v in cfg)/len(cfg)>=.75:score+=20;why.append("geometry_nibbles")
 if t.sections and any(t.left_height[i]!=t.left_height[0] or t.right_height[i]!=t.right_height[0] for i in range(t.sections)):score+=10;why.append("height_variation")
 if t.boost<=100 and t.super_boost<=100:score+=10;why.append("boost_range")
 return {"offset":offset,"score":score,"reasons":why,"sections":t.sections,"start":t.start}
def scan(b,step=1,min_score=60):
 r=[]
 for o in range(0,max(0,len(b)-SIZE+1),step):
  q=score_track(b,o)
  if q and q["score"]>=min_score:r.append(q)
 return sorted(r,key=lambda x:(-x["score"],x["offset"]))

def resolve_overlaps(candidates,size=SIZE):
 chosen=[]
 for c in sorted(candidates,key=lambda x:(-x["score"],x["offset"])):
  a,b=c["offset"],c["offset"]+size
  if any(not (b<=x["offset"] or a>=x["offset"]+size) for x in chosen):continue
  chosen.append(c)
 return sorted(chosen,key=lambda x:x["offset"])
