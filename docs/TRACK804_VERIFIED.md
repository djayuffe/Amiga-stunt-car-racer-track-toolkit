# Canonical 804-byte expanded track block — corrected

v6 resolves the v5 arithmetic discrepancy.

The X and Z grid positions are **packed together into one byte per track piece** (`road_xz`);
they are not two independent 100-byte arrays.

| Offset | Length | Field |
|---:|---:|---|
| 0 | 1 | number of sections |
| 1 | 1 | player start section |
| 2 | 100 | packed road X/Z |
| 102 | 100 | angle/template |
| 202 | 100 | left Y-profile ID |
| 302 | 100 | right Y-profile ID / road-line flag |
| 402 | 200 | 100 unsigned big-endian left cumulative height words |
| 602 | 200 | 100 unsigned big-endian right cumulative height words |
| 802 | 1 | standard boost |
| 803 | 1 | super boost |

Total: 2 + 100*4 + 200*2 + 2 = **804 bytes**.

The verified codec preserves all 100 slots, including inactive tail entries. A no-op
decode/encode is therefore byte-identical.

## Compressed source representation

The on-disk/original compressed form is different from this expanded block. The decoded
template/configuration byte controls repeat runs and whether left/right profile IDs are
stored independently. Template lows 12–15 are special encodings. Height shifts are
derived cumulatively from native Y-profile tables.

Do not confuse this 804-byte expanded editor/interchange representation with the
compressed protected-disk source stream.
