"""Pattern Design & Grading doesn't exist yet, so there is no real piece silhouette geometry to
nest. This derives a stable, visually-varied placeholder width/height per piece (deterministic
from `piece_code`, so the same piece always renders the same size) -- explicitly a stand-in to be
replaced once Pattern Design can supply real outlines, not a modeling decision to keep.
"""

import hashlib

MIN_DIM = 40.0
MAX_DIM = 160.0


def synthetic_dimensions(piece_code: str) -> tuple[float, float]:
    digest = hashlib.sha256(piece_code.encode()).digest()
    width = MIN_DIM + (digest[0] / 255) * (MAX_DIM - MIN_DIM)
    height = MIN_DIM + (digest[1] / 255) * (MAX_DIM - MIN_DIM)
    return round(width, 1), round(height, 1)
