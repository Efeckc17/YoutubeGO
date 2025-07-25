import types, sys

Image = types.ModuleType("PIL.Image")

def new(mode, size, color):
    class _Img:
        def save(self, *args, **kwargs):
            pass
    return _Img()

Image.new = new

# Expose inside PIL module
sys.modules[__name__ + ".Image"] = Image