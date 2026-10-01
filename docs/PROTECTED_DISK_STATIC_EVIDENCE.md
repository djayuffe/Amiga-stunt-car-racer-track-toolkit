# Protected disk: static evidence

The supplied image is exactly 901,120 bytes = 1760 logical 512-byte sectors.

Static analysis finds only **874 unique sectors**. The largest
duplicate-content group contains **850 sectors**.

The boot area contains the literal loader/protection signature:

`Protection (C)Copyright 1989 Rob Northen Computing. All Rights Reserved.`

This establishes that a normal AmigaDOS sector writer is not a sufficient native authoring
strategy. A bootable modified disk requires reproducing the protection/custom-track encoding
as observed by the loader or patching/bypassing that loader in a separately validated build.

The kit therefore supports analysis and evidence-gated byte patches, but does not call a
logical-sector edit a verified protected-disk rewrite.
