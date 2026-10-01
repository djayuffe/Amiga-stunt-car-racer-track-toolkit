#!/usr/bin/env python3
"""Verified codec for the canonical expanded 804-byte Stunt Car Racer track block."""
from dataclasses import dataclass
import struct, json
SIZE=804; N=100
@dataclass
class Track804:
    num_sections:int
    player_start:int
    road_xz:list
    angle_template:list
    left_y_id:list
    right_y_id:list
    left_shift:list
    right_shift:list
    standard_boost:int
    super_boost:int

def decode(b:bytes)->Track804:
    if len(b)!=SIZE: raise ValueError(f"expected {SIZE} bytes, got {len(b)}")
    return Track804(
      b[0],b[1],list(b[2:102]),list(b[102:202]),list(b[202:302]),list(b[302:402]),
      list(struct.unpack(">100H",b[402:602])),list(struct.unpack(">100H",b[602:802])),
      b[802],b[803])

def encode(t:Track804)->bytes:
    if not 0<=t.num_sections<=100: raise ValueError("num_sections outside 0..100")
    arrs=(t.road_xz,t.angle_template,t.left_y_id,t.right_y_id)
    if any(len(a)!=100 for a in arrs) or len(t.left_shift)!=100 or len(t.right_shift)!=100:
        raise ValueError("canonical arrays must contain 100 entries")
    out=bytearray(804); out[0]=t.num_sections;out[1]=t.player_start
    out[2:102]=bytes(t.road_xz);out[102:202]=bytes(t.angle_template)
    out[202:302]=bytes(t.left_y_id);out[302:402]=bytes(t.right_y_id)
    struct.pack_into(">100H",out,402,*t.left_shift);struct.pack_into(">100H",out,602,*t.right_shift)
    out[802]=t.standard_boost;out[803]=t.super_boost
    return bytes(out)

def to_dict(t):
    d=t.__dict__.copy();d["schema"]="scr-track804-v2";return d
def from_dict(d):
    return Track804(**{k:d[k] for k in Track804.__dataclass_fields__})

if __name__=="__main__":
 import argparse,pathlib
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
 p=sp.add_parser("decode");p.add_argument("input");p.add_argument("output")
 p=sp.add_parser("encode");p.add_argument("input");p.add_argument("output")
 a=ap.parse_args()
 if a.cmd=="decode":
  pathlib.Path(a.output).write_text(json.dumps(to_dict(decode(pathlib.Path(a.input).read_bytes())),indent=2))
 else:
  pathlib.Path(a.output).write_bytes(encode(from_dict(json.loads(pathlib.Path(a.input).read_text()))))
