# Native 804-byte track interchange

The PC remake's `ReadAmigaTrackData()` defines the canonical representation used by this kit. It reads exactly 804 bytes: 2 header bytes, six fixed 100-entry arrays (four byte arrays + two big-endian word arrays), then standard/super boost bytes.

Offsets are deliberately stable and are suitable for a third-party editor. Do not normalize away the raw IDs: the low nibble of angle/template selects reusable near-section geometry; the left profile high bit selects word-format Y coordinates; the right profile high bit has separate road-line-colour semantics.

## Editor contract

An editor should preserve all 100 native slots even when only `num_pieces` are active. For active pieces expose grid X/Z, rough quadrant, extra-180 flag, template ID, left/right Y/profile ID, and signed overall left/right Y shift. Derived meshes should be caches, never authoritative source data.

## Geometry reconstruction

The original engine does not store each road piece as an independent triangle mesh. It combines a near-section template with Y-coordinate/profile tables and per-piece transforms/shifts, then emits top/left/right faces. The remake confirms top faces are emitted as two triangles per segment and side faces likewise. Exact reconstruction therefore requires the template X/Z coordinate tables plus decoded Y profile tables; these are the next authoritative layer to port from the labelled 68000 source/remake.
