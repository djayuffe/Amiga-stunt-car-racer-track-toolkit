# Provenance — v4

The exact conversion semantics were checked against the public Multi Stunt Car `src/Track.cpp`, itself a modern continuation of the Stunt Car Remake code, and against Vesuri's manually labelled Amiga disassembly. The kit does not embed the full third-party table dump. Instead `compile_native_tables.py` compiles a user-supplied local source into the small data file consumed by `exact_mesh.py`.

Verified facts include seven used X/Z templates (0,1,3,4,6,7,10), 128 Y profiles, 0x800 local rotation extent, PC_FACTOR 2 in the remake, and end-to-start seam correction across track cubes.
