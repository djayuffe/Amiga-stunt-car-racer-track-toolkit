from .track import Track
F=("sections","start","xz","config","left_profile","right_profile","left_height","right_height","boost","super_boost")
def diff(a,b):
 r=[]
 for f in F:
  x,y=getattr(a,f),getattr(b,f)
  if isinstance(x,list):r += [{"field":f,"index":i,"before":u,"after":v} for i,(u,v) in enumerate(zip(x,y)) if u!=v]
  elif x!=y:r.append({"field":f,"before":x,"after":y})
 return r
def apply(t,c):
 d={f:(list(getattr(t,f)) if isinstance(getattr(t,f),list) else getattr(t,f)) for f in F}
 for x in c:
  f=x["field"]
  if f not in d:raise ValueError("field")
  if "index" in x:
   i=x["index"]
   if not isinstance(d[f],list) or not 0<=i<len(d[f]) or d[f][i]!=x["before"]:raise ValueError("before mismatch")
   d[f][i]=x["after"]
  else:
   if d[f]!=x["before"]:raise ValueError("before mismatch")
   d[f]=x["after"]
 q=Track(**d);q.validate();return q
