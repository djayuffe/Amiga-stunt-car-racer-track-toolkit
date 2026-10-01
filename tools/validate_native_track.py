#!/usr/bin/env python3
"""Validate native track JSON without assuming the active piece count."""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from track804_codec import from_json_dict, encode, decode
d=json.loads(pathlib.Path(sys.argv[1]).read_text())
t=from_json_dict(d)
raw=encode(t)
assert encode(decode(raw)) == raw
used_templates=sorted(set(t.template))
print("OK")
print("bytes:",len(raw))
print("templates:",used_templates)
print("boost:",t.standard_boost,t.super_boost)
