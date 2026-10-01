# Deep continuation

This pass audits the actual packaged capabilities and the original ADF.

New hard evidence:
- 901120-byte / 1760-sector image;
- 874 unique logical sectors;
- very large duplicate-sector groups;
- Rob Northen Computing protection signature in boot area.

Also corrected capability discovery: exact_mesh.py, compile_native_tables.py, native_mesh.py
and extract_tracks.py are present at project root, not under tools/.

No polygon topology or protected-sector encoding is invented. Those require either a
renderer-linked executable/memory image or a dynamic loader trace.
