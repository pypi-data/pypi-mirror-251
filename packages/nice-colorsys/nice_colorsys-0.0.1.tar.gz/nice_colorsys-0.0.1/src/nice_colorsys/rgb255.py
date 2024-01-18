from collections import namedtuple
from .nice_colorsys import spaces, rgb
from .custom_space import register_space

rgb255 = namedtuple("rgb255", ["red", "green", "blue"])
register_space(
    rgb255,
    lambda x: rgb(*(c/255 for c in x)),
    lambda x: rgb255(*(round(c*255) for c in x))
)
rgb255.as_hex = lambda x: "".join("{:02x}".format(c) for c in x)
__all__ = ["rgb255"]