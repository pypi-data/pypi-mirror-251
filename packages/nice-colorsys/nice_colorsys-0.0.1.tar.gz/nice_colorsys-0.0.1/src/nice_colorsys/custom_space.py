from  .nice_colorsys import spaces, rgb

def register_space(space: type, to_rgb, from_rgb, name=None):
    if name is None:
        name = space.__name__
    spaces[name] = space
    space.to_rgb = to_rgb
    to_name = f"to_{name}"
    setattr(rgb, to_name, from_rgb)
    f = lambda x: getattr(x.to_rgb(), to_name)()
    for s in (set(spaces) - {"rgb", name}):
        setattr(spaces[s], f"to_{name}", f)
    for s in (set(spaces) - {"rgb", "hsluv"}):
        setattr(
            space,
            f"to_{s}",
            (lambda _s: lambda x: getattr(x.to_rgb(), f"to_{_s}")())(s)
        )