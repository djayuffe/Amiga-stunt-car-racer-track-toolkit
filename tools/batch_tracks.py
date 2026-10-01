#!/usr/bin/env python3
import pathlib,json,sys,hashlib
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from track804_codec_verified import decode,to_dict
from editor_interchange import export_editor
src=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
files=[src] if src.is_file() else sorted(p for p in src.iterdir() if p.is_file());m=[]
for p in files:
 b=p.read_bytes(); chunks=[b] if len(b)==804 else ([b[i:i+804] for i in range(0,len(b),804)] if len(b)%804==0 else [])
 for i,c in enumerate(chunks):
  try:t=decode(c)
  except Exception:continue
  n=p.stem+(f"_{i:02d}" if len(chunks)>1 else "")
  (out/(n+".native.json")).write_text(json.dumps(to_dict(t),indent=2))
  (out/(n+".editor.json")).write_text(json.dumps(export_editor(c),indent=2))
  m.append({"name":n,"sha256":hashlib.sha256(c).hexdigest(),"sections":t.num_sections})
(out/"manifest.json").write_text(json.dumps(m,indent=2));print("exported",len(m))
