#!/usr/bin/env python3
import pathlib,json
root=pathlib.Path(__file__).resolve().parents[1]
names=["exact_mesh.py","compile_native_tables.py","extract_tracks.py","native_mesh.py",
"editor/blender_import_scr.py","editor/scr_level_editor.html",
"tools/track804_codec_verified.py","tools/editor_interchange.py","tools/geometry_candidate_scanner.py",
"tools/adf_deep_diagnostics.py"]
out={}
for n in names:
 p=root/n
 out[n]={"present":p.exists(),"bytes":p.stat().st_size if p.exists() else 0}
print(json.dumps(out,indent=2))
