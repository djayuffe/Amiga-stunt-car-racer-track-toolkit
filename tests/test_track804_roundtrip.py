#!/usr/bin/env python3
import os, sys, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","tools"))
from track804_codec import *
random.seed(68000)
t=Track804(
 [random.randrange(256) for _ in range(100)],
 [random.randrange(256) for _ in range(100)],
 [random.randrange(256) for _ in range(100)],
 [random.randrange(256) for _ in range(100)],
 [random.randrange(256) for _ in range(100)],
 [random.randrange(-32768,32768) for _ in range(100)],
 [random.randrange(-32768,32768) for _ in range(100)],
 17,231)
raw=encode(t)
assert len(raw)==902
assert encode(decode(raw))==raw
j=to_json_dict(decode(raw))
assert encode(from_json_dict(j))==raw
print("experimental expanded-record round-trip: PASS")
