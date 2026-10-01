# Native 804-byte round-trip model

v5 makes the original track record the authoritative editable asset.

Layout:

| Offset | Size | Meaning |
|---:|---:|---|
| 0 | 100 | grid X |
| 100 | 100 | grid Z |
| 200 | 100 | native template/configuration byte |
| 300 | 100 | left Y-profile byte |
| 400 | 100 | right Y-profile / flag byte |
| 500 | 200 | left overall height, 100 signed BE int16 |
| 700 | 200 | right overall height, 100 signed BE int16 |
| 900? | — | impossible: the complete record is 804 bytes |

The apparent arithmetic trap above is intentional documentation of an inconsistency:
five 100-byte arrays plus two 200-byte arrays would already be 900 bytes. Therefore an
804-byte interpretation cannot simultaneously contain all seven full 100-entry arrays
in that form. v5's codec is kept as an isolated experimental hypothesis and its test
will fail if that claimed layout is used, preventing accidental promotion to canonical.

This is preferable to silently emitting corrupt game data. The exact native serializer
must only be enabled after the original loader's field widths/counts are reconciled.
