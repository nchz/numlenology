import numpy as np


def get_channels(hexcode):
    """
    Return 1d `np.array` with int values representing each channel [R,G,B] or
    [R,G,B,a] if value for transparency is present.

    Inverse of `get_hexcode`.
    """
    assert len(hexcode) in (7, 9)
    assert hexcode[0] == "#"
    rgb = hexcode[1:3], hexcode[3:5], hexcode[5:7], hexcode[7:]
    rgb = [int(x, 16) for x in rgb if x != ""]
    return np.array(rgb, dtype=np.uint8)


def get_hexcode(rgb):
    """
    Build hexcode for the color represented by array `rgb`. It may contain
    three or four channels (the extra channel is for transparency).

    Inverse of `get_channels`.
    """
    return "#" + "".join(f"{hex(int(x))[2:]:0>2}" for x in rgb)


def fade_color(c1, c2, n):
    """Return a list with `n` strings representing colors fading from `c1` to `c2`."""
    assert n >= 2

    # decompose RGB. ignore alpha if present.
    rgb1 = get_channels(c1)
    rgb2 = get_channels(c2)

    # find distances by chanel.
    step_by_channel = (rgb2 - rgb1) / (n - 1)

    # build steps.
    scale = [rgb1 + (i * step_by_channel) for i in range(n)]
    scale = [get_hexcode(c) for c in scale]

    assert scale[0] == c1
    assert scale[-1] == c2

    return scale
