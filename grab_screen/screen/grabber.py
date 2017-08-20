import logging

from ..exceptions import ScreenError
from ..version import __name__

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

logger = logging.getLogger(__name__)


class Grabber(tk.Tk):
    WINDOW_COLOR = '#ffffff'
    WINDOW_ALPHA = 0.2

    RECTANGLE_COLOR = '#000000'

    @classmethod
    def run(cls):
        scope = {'coords': None}

        def set_coords(_coords):
            scope['coords'] = _coords
            grabber.exit()  # close the window

        grabber = cls(on_selected=set_coords)
        try:
            grabber.mainloop()
        except KeyboardInterrupt:
            grabber.exit()

        return scope['coords']

    def __init__(self, on_selected):
        tk.Tk.__init__(self)

        self.title(__name__)

        self._on_selected = on_selected

        self._coords = None
        self._rect_id = None
        self._is_drawing = False

        self._canvas = None

        self.initialize_geometry()
        self.initialize_controls()

    def initialize_geometry(self):
        self.wait_visibility()
        self.attributes('-topmost', True)
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', self.WINDOW_ALPHA)

    def initialize_controls(self):
        self._canvas = tk.Canvas(self, bg=self.WINDOW_COLOR, cursor='crosshair')
        self._canvas.pack(fill=tk.BOTH, expand=1)

        self._canvas.bind('<Button-1>', self.start_drawing)
        self._canvas.bind('<Button-3>', self.exit)
        self._canvas.bind('<ButtonRelease-1>', self.stop_drawing)
        self._canvas.bind('<Motion>', self.draw_rectangle)

    def start_drawing(self, event):
        logger.debug("Selecting screen area.")
        self._is_drawing = True

        x = self._canvas.canvasx(event.x)
        y = self._canvas.canvasy(event.y)

        self._coords = [x, y, x, y]
        self._rect_id = self._canvas.create_rectangle(*self._coords, fill=self.RECTANGLE_COLOR)

    def draw_rectangle(self, event):
        if not self._is_drawing:
            return

        self._coords[2] = self._canvas.canvasx(event.x)
        self._coords[3] = self._canvas.canvasy(event.y)
        self._canvas.coords(self._rect_id, *self._coords)

    def stop_drawing(self, event):
        logger.debug("Screen area has been selected. Coords: %s", self._coords)
        self._is_drawing = False

        self._canvas.delete(self._rect_id)

        self._on_selected(self._coords)

    def exit(self, event=None):
        self.attributes('-alpha', 0)
        self.destroy()


def grab_area():
    logger.info("Selecting an area.")
    coords = Grabber.run()
    if not coords:
        raise ScreenError("Aborted!")

    coords = tuple(map(int, coords))
    x1, x2 = sorted(coords[0::2])
    y1, y2 = sorted(coords[1::2])
    coords = (x1, y1, x2, y2)

    logger.debug("Selected area %s.", coords)
    return coords
