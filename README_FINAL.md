
## Final closure release

Use `tools/track804_codec_verified.py` for the canonical 804-byte expanded block and
`tools/editor_interchange.py` for safe editor-facing JSON. Generated meshes are derived
artifacts; edit native integer fields, then regenerate geometry.

`tools/geometry_candidate_scanner.py` is intentionally conservative and does not invent
object identities.

See `FINAL_CLOSURE_AUDIT.md` for the exact closed/open boundary.
