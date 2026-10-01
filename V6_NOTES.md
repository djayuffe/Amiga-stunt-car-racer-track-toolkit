# v6

* Corrects v5's 902-byte hypothesis.
* Adds a verified canonical 804-byte codec with explicit offsets.
* X/Z is one packed byte per piece.
* Adds byte-identical round-trip and offset assertions.
* Keeps compressed source decoding conceptually separate from the expanded editor block.
* Native protected-disk write-back remains disabled until the exact compressed encoder
  and disk-sector protection/checksum path are verified.
