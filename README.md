# Amiga Stunt Car Racer Track Toolkit

Reverse-engineering toolkit for the Amiga version of **Stunt Car Racer**. It focuses on protected-disk evidence, the verified 804-byte native track resource format, editor-safe JSON interchange, guarded reinsertion workflows, and OBJ mesh/export helpers for analysis.

The repository focuses on the Amiga/Motorola 68000 game data format and the native Stunt Car Racer track resource pipeline.

## What This Contains

- `scrtool/` - installable Python package with track decoding, encoding, ADF metadata checks, bank split/join, patching, recovery, and transaction helpers.
- `tools/` - research utilities for geometry scanning, protected-disk diagnostics, ABI inference, emulator trace normalization, and verified/legacy track codecs.
- `editor/` - Blender importer and a small browser-based level inspector for JSON exports.
- `docs/` - reverse-engineering notes for the 804-byte format, native geometry, exact mesh status, disk evidence, provenance, and dynamic trace contracts.
- `tests/` - executable smoke and regression tests covering productized commands, release passes, codec round trips, editor interchange, and disk-evidence classification.

## Important Data Notice

The toolkit can analyze a legally obtained `Stunt Car Racer` disk image, but this repository does not grant permission to redistribute proprietary game media. The unpacked archive included `raw/original.adf`; it is intentionally ignored by Git and is not uploaded.

Place your own local image under `raw/original.adf` or pass a path explicitly when running ADF tools.

## Install

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

Useful command entry points:

```sh
scrtool --help
scrtool-advanced --help
scrtool-edit --help
scrtool-recovery --help
scrtool-transaction --help
scrtool-transaction-build --help
```

## Quick Examples

Inspect an Amiga disk image:

```sh
scrtool adf-info raw/original.adf
python adf_probe.py raw/original.adf -o probe.json
```

Decode a verified 804-byte track resource into editor JSON:

```sh
scrtool track-decode LittleRamp.bin LittleRamp.json
```

Encode an edited JSON file back to the native 804-byte resource:

```sh
scrtool --force track-encode LittleRamp.json LittleRamp.bin
```

Scan a decoded RAM or binary dump for plausible track resources:

```sh
scrtool-recovery scan decoded_game_ram.bin --min-score 60 -o candidates.json
scrtool-recovery extract decoded_game_ram.bin recovered_tracks
```

Build a guarded transaction from edited track JSON:

```sh
scrtool-transaction-build build decoded_game_ram.bin track_patch.json edited/LittleRamp.json
scrtool-transaction decoded_game_ram.bin track_patch.json --output patched_game_ram.bin --receipt receipt.json
```

Compile native geometry tables from a local compatible `Track.cpp`-style source, then export an exact mesh candidate:

```sh
python compile_native_tables.py /path/to/Track.cpp -o native_tables.json
python exact_mesh.py LittleRamp.bin native_tables.json -o exact_little_ramp
```

## Verified Track Format

The canonical track resource is 804 bytes:

| Offset | Size | Meaning |
|---:|---:|---|
| 0 | 1 | active section count |
| 1 | 1 | player start section |
| 2 | 100 | packed grid X/Z bytes |
| 102 | 100 | angle/template bytes |
| 202 | 100 | left Y/profile IDs |
| 302 | 100 | right Y/profile IDs |
| 402 | 200 | 100 big-endian left height/shift words |
| 602 | 200 | 100 big-endian right height/shift words |
| 802 | 1 | standard boost |
| 803 | 1 | super boost |

`scrtool.track`, `tools/track804_codec_verified.py`, and the release tests all use this verified 804-byte layout. `tools/track804_codec.py` is retained only as a compatibility shim for an older experimental 902-byte fixture.

## Editor Workflow

The JSON representation keeps a complete `native` backing record and exposes editable `pieces` for UI tools. This keeps round trips conservative: unknown or not-yet-modeled native fields stay intact while editors can change grid position, section config, profile IDs, and height values.

The included HTML editor is standalone:

```sh
open editor/scr_level_editor.html
```

The Blender importer reads exported JSON and creates preview geometry with native fields preserved as custom properties. Preview meshes are analysis aids; exact road/object reconstruction still depends on native table provenance described in `docs/EXACT_MESH_V4.md` and `docs/PROVENANCE_V4.md`.

## Audit Notes

This cleanup fixed these release issues:

- Project metadata now matches the archive version: `1.7.0`.
- The missing `tools/track804_codec.py` compatibility module has been restored so the full test suite runs.
- GPLv3 licensing, copyright attribution, CI, package metadata, and command entry points are explicit.
- Proprietary disk images are ignored to avoid accidental public redistribution.
- The README now separates verified facts, experimental helpers, and local-data requirements.

## Test

Run the complete dependency-free test sweep:

```sh
for test_file in tests/*.py; do
  python "$test_file"
done
```

Run syntax/bytecode compilation with caches kept inside the repository:

```sh
PYTHONPYCACHEPREFIX=.pycache python -m compileall scrtool tools tests *.py
```

CI runs both checks on every push and pull request.

## License

Copyright (C) 2026 Ulf Bertilsson.

Released under the GNU General Public License version 3 or later. See `LICENSE` and `NOTICE`.

Stunt Car Racer, Amiga, and other third-party names or data remain the property of their respective owners. This project is an independent reverse-engineering toolkit and does not include redistributable game media.
