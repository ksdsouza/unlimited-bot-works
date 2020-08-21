import gi
import numpy as np
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GdkPixbuf


class ScreenUtil:
    def __init__(self):
        self.window = Gdk.get_default_root_window().get_screen().get_active_window()

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
    width = p.get_width()
    height = p.get_height()
    channels = p.get_channels()
    rows = p.get_rowstride()

    assert p.get_colorspace() == GdkPixbuf.Colorspace.RGB
    assert p.get_bits_per_sample() == 8
    assert channels == (4 if p.get_has_alpha() else 3)
    assert rows >= width * channels

    a = np.frombuffer(p.get_pixels(), dtype=np.uint8)
    if a.shape[0] == width * channels * height:
        return a.reshape((height, width, channels))

    b = np.zeros((height, width * channels), 'uint8')
    for j in range(height):
        b[j, :] = a[rows * j:rows * j + width * channels]
    return b.reshape((height, width, channels))
