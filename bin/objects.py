from dataclasses import dataclass


@dataclass
class Voice:
    ogg_bytes: bytes


@dataclass
class VideoNote:
    raw_bytes: bytes
