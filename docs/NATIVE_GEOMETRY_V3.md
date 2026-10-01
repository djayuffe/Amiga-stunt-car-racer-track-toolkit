# Native geometry findings — v3

## Confirmed engine model

The low nibble of each angle/template byte is a geometry type index. The original engine uses it to select a geometry record from `trackGeometryDatabase`; the record supplies steering/direction metadata and coordinate/interpolation data. In the labelled Amiga disassembly the database begins at `gameData+$10882`, followed by `segmentGeometryOffsetTable` at `+$108a2`, `trackDataOffsetTable` at `+$109a2`, and `geometryParameterTable` at `+$109c2`.

The reconstruction source confirms these native templates currently used by the conversion:

| ID | form | segments | native type | length reduction | steering |
|---:|---|---:|---:|---:|---:|
| 0 | straight | 8 | 0x00 | 128 | 0x20 |
| 1 | curve right | 8 | 0x80 | 135 | 0x3e |
| 3 | curve left | 8 | 0xc0 | 135 | 0x3e |
| 4 | diagonal/straight | 13 | 0x40 | 128 | 0x20 |
| 6 | curve right | 9 | 0x80 | 122 | 0x32 |
| 7 | curve left | 9 | 0xc0 | 122 | 0x32 |
| 10 | diagonal/straight | 11 | 0x40 | 124 | 0x20 |

IDs 2,5,8,9 have no converted X/Z template in the remake table. They must not be fabricated.

## Y profiles

The left Y ID's bit 7 selects word-vs-packed-byte profile storage. The right Y ID's bit 7 is instead the alternating road-line colour flag; both IDs use the lower 7 bits as profile indices. The actual surface height is profile Y plus the corresponding per-piece overall Y shift.

## Exact mesh algorithm

For each piece the conversion obtains its template X/Z coordinate pairs, reverses pair order when bit 4 is set, rotates X/Z using the top two angle bits, then assigns left and right Y values from their profile IDs plus global shifts. Each sample has four vertices: top-left, top-right, bottom-left and bottom-right. The engine/remake finally copies boundary coordinates between adjacent pieces so the loop joins exactly.

`native_mesh.py` now exposes these semantics in JSON. Its OBJ is still explicitly an editor ribbon because this kit does not yet bundle the complete copyrighted profile/XZ data tables.
