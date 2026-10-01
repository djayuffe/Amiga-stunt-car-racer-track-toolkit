#!/usr/bin/env python3
"""Editor-neutral SCR track interchange.

This layer intentionally edits native integer fields, not generated mesh vertices.
"""
import json, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from track804_codec_verified import decode,encode,to_dict,from_dict

def unpack_xz(v): return (v&15, (v>>4)&15)
def pack_xz(x,z):
    if not(0<=x<16 and 0<=z<16): raise ValueError("grid coordinate outside 0..15")
    return (z<<4)|x

def export_editor(raw):
    t=decode(raw)
    pieces=[]
    for i in range(t.num_sections):
        x,z=unpack_xz(t.road_xz[i])
        pieces.append({"index":i,"grid_x":x,"grid_z":z,
          "configuration":t.angle_template[i],
          "geometry_type":t.angle_template[i]&15,
          "quadrant":(t.angle_template[i]>>4)&3,
          "left_y_id":t.left_y_id[i],"right_y_id":t.right_y_id[i],
          "left_shift":t.left_shift[i],"right_shift":t.right_shift[i]})
    return {"schema":"scr-editor-v1","num_sections":t.num_sections,
      "player_start":t.player_start,"standard_boost":t.standard_boost,
      "super_boost":t.super_boost,"pieces":pieces,
      "_native_tail":to_dict(t)}

def import_editor(d):
    if d.get("schema")!="scr-editor-v1": raise ValueError("bad schema")
    t=from_dict(d["_native_tail"])
    t.num_sections=d["num_sections"];t.player_start=d["player_start"]
    t.standard_boost=d["standard_boost"];t.super_boost=d["super_boost"]
    if len(d["pieces"])!=t.num_sections: raise ValueError("piece count mismatch")
    for p in d["pieces"]:
        i=p["index"]
        t.road_xz[i]=pack_xz(p["grid_x"],p["grid_z"])
        t.angle_template[i]=p["configuration"]
        t.left_y_id[i]=p["left_y_id"];t.right_y_id[i]=p["right_y_id"]
        t.left_shift[i]=p["left_shift"];t.right_shift[i]=p["right_shift"]
    return encode(t)

if __name__=="__main__":
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument("mode",choices=["export","import"]);ap.add_argument("src");ap.add_argument("dst");a=ap.parse_args()
 if a.mode=="export": pathlib.Path(a.dst).write_text(json.dumps(export_editor(pathlib.Path(a.src).read_bytes()),indent=2))
 else: pathlib.Path(a.dst).write_bytes(import_editor(json.loads(pathlib.Path(a.src).read_text())))
