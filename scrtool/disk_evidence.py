import hashlib
CUSTOM={0xDFF01A:"DSKBYTR",0xDFF020:"DSKPTH",0xDFF022:"DSKPTL",0xDFF024:"DSKLEN",0xDFF026:"DSKDAT",0xDFF07E:"DSKSYNC",0xDFF096:"DMACON",0xDFF09A:"INTENA",0xDFF09C:"INTREQ",0xDFF09E:"ADKCON"}
def find(d,n):
 r=[];i=0
 while True:
  i=d.find(n,i)
  if i<0:return r
  r.append(i);i+=1
def scan(d):
 refs=[]
 for a,n in CUSTOM.items():
  refs += [{"offset":o,"register":n,"address":f"{a:06X}","encoding":"absolute32","strength":"strong"} for o in find(d,a.to_bytes(4,"big"))]
  refs += [{"offset":o,"register":n,"address":f"{a:06X}","encoding":"low16","strength":"weak"} for o in find(d,(a&65535).to_bytes(2,"big"))]
 ss=[]
 for s in (b"trackdisk.device",b"disk.resource",b"Rob Northen",b"Protection (C)Copyright 1989 Rob Northen Computing"):
  ss += [{"offset":o,"text":s.decode()} for o in find(d,s)]
 strong=[x for x in refs if x["strength"]=="strong"]
 return {"schema":"scr-disk-evidence-v1","bytes":len(d),"sha256":hashlib.sha256(d).hexdigest(),"custom_register_refs":sorted(refs,key=lambda x:(x["offset"],x["register"])),"strings":ss,"classification":{"raw_custom_chip_evidence":"present" if strong else "not_proven","strong_reference_count":len(strong),"trackdisk_string":"present" if any(x["text"]=="trackdisk.device" for x in ss) else "not_found","note":"Static byte references are evidence candidates, not proof of executed code or a protection format."}}
