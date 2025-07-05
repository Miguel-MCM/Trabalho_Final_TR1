import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk # type:ignore

import matplotlib
matplotlib.use("GTK4Agg")  # usa o backend GTK4Agg
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar

import numpy as np

class GraphFrame(Gtk.Box):
    def __init__(self, title:str, xlabel:str, ylabel:str, size:tuple[int, int]):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.fig = Figure(figsize=(3, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.line, = self.ax.plot([], [])
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(size[0], size[1])
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.set_hexpand(True)

        self.append(self.toolbar)
        self.append(self.canvas)

        self.xdata = np.array([])
        self.ydata = np.array([])

    def update(self, x:np.ndarray, y:np.ndarray) -> None:
        self.xdata = x
        self.ydata = y
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        self.ax.relim();
        self.ax.autoscale_view()
        self.canvas.draw()