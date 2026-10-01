# Reverse-engineering status

## Confirmed from supplied ADF

* 901,120 bytes / 1760 sectors.
* DOS0 boot signature with Rob Northen protection string.
* Original track names are visible in the image, but canonical 804-byte track resources are not present verbatim.
* SHA-256: `548fd106cd62f2d80159d48ddd5293d8b22b6b17f80c17a84a61d75f5c8a9e06`.

## Confirmed independently against source derived from the Amiga binary

* Eight original track resources.
* 804-byte canonical resource layout.
* 16 near-section templates selected by the low nibble of the angle/template byte.
* reusable byte/word Y-coordinate profile tables.
* mesh generation is segmented and creates road top + left/right side faces.

## Current deliverables

* exact 804 parser and binary-preserving JSON exporter;
* raw/decoded binary scanner;
* centerline OBJ preview;
* Blender layout importer preserving native fields as custom properties;
* standalone HTML 16x16 layout inspector;
* original ADF + provenance report.

## Remaining for pixel/geometry-faithful mesh extraction

1. Port the full near-section X/Z template table and Y profile pointer tables.
2. Port signed nibble/byte/word Y decoding exactly.
3. Port orientation/extra-180 transform and segment stitching.
4. Export road top and side triangles to OBJ/glTF.
5. Identify non-track polygon/object databases (car, posts/gantries/background props) separately from road templates.
6. Validate generated vertices against the remake/disassembly and, ideally, emulator memory traces from this exact ADF.
