# Exact dynamic-trace contract

The boot disassembly establishes an Exec/IORequest loader path and a 0x9800-byte allocation.
To finish exact protected-disk inversion, instrument an Amiga emulator at the loader boundary
and emit:

```
MEMW PC ADDRESS SIZE VALUE
MEMR PC ADDRESS SIZE VALUE
IO   PC COMMAND OFFSET LENGTH DATA_ADDRESS
```

All numeric fields except SIZE are hexadecimal.

`tools/normalize_emulator_trace.py` converts this into deterministic JSON. The required
evidence is the ordered IO requests plus writes into the allocated/decode buffers. Comparing
pre/post buffers identifies the protection transform and checksum without guessing.

For object ABI recovery, continue tracing memory reads made by the world renderer. Repeated
reads from a candidate block reveal vertex stride; subsequent index/pointer reads reveal face
records. Only then should `candidate_to_obj.py` be upgraded from points to faces.
