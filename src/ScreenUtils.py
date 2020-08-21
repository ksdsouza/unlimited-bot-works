import gi
import numpy as np
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf


class ScreenUtil:
    def __init__(self):
        w = Gdk.get_default_root_window().get_screen().get_active_window()
        self.window = w

    def get_pixels(self):
        pixel_buffer = Gdk.pixbuf_get_from_window(
            self.window,
            0,
            0,
            self.window.get_width(),
            self.window.get_height()
        )
        raw_pixels = array_from_pixbuf(pixel_buffer)
        return raw_pixels[0:1155, 100:2355, :]


def array_from_pixbuf(p: GdkPixbuf) -> np.ndarray:
    w, h, c, r = (p.get_width(), p.get_height(), p.get_n_channels(), p.get_rowstride())
    assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
    assert p.get_bits_per_sample() == 8
    assert c == (4 if p.get_has_alpha() else 3)
    assert r >= w * c

    a = np.frombuffer(p.get_pixels(), dtype=np.uint8)
    if a.shape[0] == w * c * h:
        return a.reshape((h, w, c))

    b = np.zeros((h, w * c), 'uint8')
    for j in range(h):
        b[j, :] = a[r * j:r * j + w * c]
    return b.reshape((h, w, c))
