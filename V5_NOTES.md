# v5 continuation notes

This pass found and fixed a serious specification hazard from earlier notes.

The previously repeated claim that a track is 804 bytes while containing five 100-byte
byte arrays + two 100-word height arrays + two boost bytes is arithmetically impossible:
500 + 400 + 2 = 902 bytes.

Accordingly v5 does **not** pretend to provide a game-safe 804-byte writer. It adds an
isolated 902-byte expanded-record hypothesis codec and explicit audit documentation.
It must not be used to patch the original disk.

This is an important reverse-engineering correction: read/export tools may remain useful,
but native write-back stays disabled until field counts/packing are verified from the
68000 loader itself.

Next authoritative target:
1. disassemble the track-resource read loop;
2. determine actual entry count and packed field widths;
3. fixture-test against bytes recovered from game memory;
4. only then enable native write-back.
