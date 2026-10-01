import pathlib,json,hashlib
def verify_release(root,manifest="RELEASE_MANIFEST.json"):
 root=pathlib.Path(root);m=json.loads((root/manifest).read_text());bad=[];seen=set()
 for e in m["files"]:
  p=root/e["path"];seen.add(e["path"])
  if not p.is_file():bad.append({"path":e["path"],"error":"missing"});continue
  b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
  if len(b)!=e["bytes"]:bad.append({"path":e["path"],"error":"size","expected":e["bytes"],"actual":len(b)})
  if h!=e["sha256"]:bad.append({"path":e["path"],"error":"sha256","expected":e["sha256"],"actual":h})
 return {"valid":not bad,"checked":len(m["files"]),"errors":bad}
