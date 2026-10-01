#!/usr/bin/env python3
"""Conservative scanner for [count,index...] face streams against signed BE XYZ vertices."""
import pathlib,struct,json,argparse
def scan(b,vbase,vcount,vstride=6,min_faces=2,max_face_vertices=8):
 out=[]
 # require vertex block bounds and reasonable coordinate magnitude
 if vbase<0 or vbase+(vcount-1)*vstride+6>len(b):return out
 verts=[struct.unpack_from(">hhh",b,vbase+i*vstride) for i in range(vcount)]
 sane=sum(all(-20000<=q<=20000 for q in v) for v in verts)/max(1,vcount)
 if sane<.9:return out
 for off in range(0,len(b)-4):
  p=off;faces=[];used=set()
  while p<len(b):
   n=b[p]
   if n<3 or n>max_face_vertices or p+1+n>len(b):break
   ix=list(b[p+1:p+1+n])
   if any(i>=vcount for i in ix) or len(set(ix))<3:break
   faces.append(ix);used.update(ix);p+=1+n
   # common word alignment padding
   if p&1 and p<len(b) and b[p]==0:p+=1
   if len(faces)>=256:break
  if len(faces)>=min_faces:
   coverage=len(used)/vcount
   out.append({"vertex_base":vbase,"vertex_count":vcount,"vertex_stride":vstride,
    "face_base":off,"face_end":p,"face_count":len(faces),"vertex_coverage":coverage,
    "score":round(len(faces)*(0.5+coverage),4)})
 out.sort(key=lambda x:(-x["score"],x["face_base"]))
 return out
if __name__=="__main__":
 a=argparse.ArgumentParser();a.add_argument("binary");a.add_argument("--vbase",type=lambda x:int(x,0),required=True);a.add_argument("--vcount",type=int,required=True);a.add_argument("--vstride",type=int,default=6);a.add_argument("-o","--output");q=a.parse_args()
 r=scan(pathlib.Path(q.binary).read_bytes(),q.vbase,q.vcount,q.vstride);s=json.dumps(r,indent=2)
 pathlib.Path(q.output).write_text(s) if q.output else print(s)
