#!/usr/bin/env python3
"""Compatibility codec for the legacy experimental 902-byte track record.

The verified native Stunt Car Racer resource is the 804-byte format implemented
by ``tools/track804_codec_verified.py`` and ``scrtool.track``. This module is
kept only so old experimental fixtures and round-trip tests remain executable.
"""

from dataclasses import dataclass
from typing import List
import json
import struct

SIZE = 902
N = 100


@dataclass
class Track804:
    x: List[int]
    z: List[int]
    template: List[int]
    left_profile: List[int]
    right_profile: List[int]
    left_height: List[int]
    right_height: List[int]
    standard_boost: int
    super_boost: int


def decode(data: bytes) -> Track804:
    if len(data) != SIZE:
        raise ValueError(f"expected experimental {SIZE} bytes, got {len(data)}")
    pos = 0

    def take(length: int) -> bytes:
        nonlocal pos
        chunk = data[pos : pos + length]
        pos += length
        return chunk

    track = Track804(
        list(take(N)),
        list(take(N)),
        list(take(N)),
        list(take(N)),
        list(take(N)),
        list(struct.unpack(">100h", take(200))),
        list(struct.unpack(">100h", take(200))),
        take(1)[0],
        take(1)[0],
    )
    if pos != SIZE:
        raise AssertionError("internal codec size mismatch")
    return track


def encode(track: Track804) -> bytes:
    arrays = (
        track.x,
        track.z,
        track.template,
        track.left_profile,
        track.right_profile,
        track.left_height,
        track.right_height,
    )
    if any(len(values) != N for values in arrays):
        raise ValueError("all track arrays must contain exactly 100 entries")

    out = bytearray()
    for values in (track.x, track.z, track.template, track.left_profile, track.right_profile):
        if any(not 0 <= int(value) <= 255 for value in values):
            raise ValueError("byte field outside 0..255")
        out.extend(bytes(map(int, values)))

    for values in (track.left_height, track.right_height):
        if any(not -32768 <= int(value) <= 32767 for value in values):
            raise ValueError("height outside int16")
        out.extend(struct.pack(">100h", *map(int, values)))

    for value in (track.standard_boost, track.super_boost):
        if not 0 <= int(value) <= 255:
            raise ValueError("boost outside 0..255")
        out.append(int(value))

    if len(out) != SIZE:
        raise AssertionError("internal codec size mismatch")
    return bytes(out)


def to_json_dict(track: Track804) -> dict:
    return {
        "schema": "scr-native-804-experimental-v1",
        "x": track.x,
        "z": track.z,
        "template": track.template,
        "left_profile": track.left_profile,
        "right_profile": track.right_profile,
        "left_height": track.left_height,
        "right_height": track.right_height,
        "standard_boost": track.standard_boost,
        "super_boost": track.super_boost,
    }


def from_json_dict(data: dict) -> Track804:
    if data.get("schema") not in (None, "scr-native-804-v1", "scr-native-804-experimental-v1"):
        raise ValueError("unsupported schema")
    return Track804(
        **{
            key: data[key]
            for key in (
                "x",
                "z",
                "template",
                "left_profile",
                "right_profile",
                "left_height",
                "right_height",
                "standard_boost",
                "super_boost",
            )
        }
    )


def main() -> int:
    import argparse
    import pathlib

    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="cmd", required=True)
    decode_cmd = subcommands.add_parser("decode")
    decode_cmd.add_argument("input")
    decode_cmd.add_argument("output")
    encode_cmd = subcommands.add_parser("encode")
    encode_cmd.add_argument("input")
    encode_cmd.add_argument("output")
    args = parser.parse_args()

    if args.cmd == "decode":
        track = decode(pathlib.Path(args.input).read_bytes())
        pathlib.Path(args.output).write_text(json.dumps(to_json_dict(track), indent=2), encoding="utf-8")
    else:
        track = from_json_dict(json.loads(pathlib.Path(args.input).read_text(encoding="utf-8")))
        pathlib.Path(args.output).write_bytes(encode(track))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
