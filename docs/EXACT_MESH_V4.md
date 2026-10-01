# Exact/native mesh pipeline — v4

`compile_native_tables.py` compiles the seven native X/Z templates and 128 Y profiles from a locally supplied Track.cpp-style reconstruction. `exact_mesh.py` combines those tables with an 804-byte track.

The implementation mirrors the documented conversion path: signed little-endian X/Z words, native quadrant rotation around 0x800, optional pair reversal, packed/word Y decoding, per-side overall Y shift, PC_FACTOR=2, four vertices per longitudinal sample, and the original seam-closure copy between adjacent cubes.

Outputs are deliberately separated into road, left side and right side indexed triangle groups. `track.mesh.json` retains per-piece ranges and native template IDs for editor tooling.

This is materially different from `native_mesh.py`, which remains a lightweight proxy visualizer.
