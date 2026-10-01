# ABI closure tooling

This pass adds conservative face-stream discovery and candidate OBJ export. Given a proven
or trace-inferred vertex base/count/stride, the scanner searches for contiguous polygon
records whose indices remain in range and scores candidates by face count and vertex coverage.

It does not choose an arbitrary candidate as authoritative. Multiple surviving candidates
remain explicit in JSON so renderer trace evidence can select the actual ABI.

Protection transforms now have inverse round-trip property tests, including 512-byte blocks.
