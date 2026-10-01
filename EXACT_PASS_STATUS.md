# Exactness pass status

New instruction-level evidence is included in `boot_disassembly.txt`.

The supplied runtime lacks a full m68k disassembler/emulator, so this pass adds a reproducible
focused boot decoder and a deterministic dynamic-trace ingestion contract rather than claiming
a nonexistent execution trace.

Exact protected-track inversion and indexed object faces now have explicit evidence acquisition
paths. They are not marked verified until an actual loader/renderer trace is supplied or produced.
