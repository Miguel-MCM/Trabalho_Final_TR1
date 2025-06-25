#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import matplotlib
matplotlib.use("GTK4Agg")  # usa o backend GTK4Agg
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar

import numpy as np

class GraphFrame(Gtk.Box):
    def __init__(self, parent, title, xlabel, ylabel, marker):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.fig = Figure(figsize=(4, 3), dpi=100)
        self.ax = self.fig.add_subplot()
        self.line, = self.ax.plot([], [], marker=marker)
        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_hexpand(True); self.canvas.set_vexpand(True)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.set_hexpand(True)

        self.append(self.toolbar)
        self.append(self.canvas)

        self.xdata = []
        self.ydata = []

    def update(self, x, y):
        self.xdata.append(x); self.ydata.append(y)
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        self.ax.relim(); self.ax.autoscale_view()
        self.canvas.draw()

class PlotWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="GTK4 + Matplotlib: Dois Gráficos")
        self.set_default_size(800, 400)

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(main_vbox)

        plots_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        main_vbox.append(plots_hbox)

        # instanciando dois frames independentes
        self.graph1 = GraphFrame(self, "Gráfico 1", "X1", "Y1", "o")
        self.graph2 = GraphFrame(self, "Gráfico 2", "X2", "Y2", "x")
        plots_hbox.append(self.graph1)
        plots_hbox.append(self.graph2)

        btn_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        main_vbox.append(btn_hbox)

        btn1 = Gtk.Button(label="Adicionar dados no Gráfico 1")
        btn1.connect("clicked", lambda w: self.graph1.update(len(self.graph1.xdata)+1,
                                                              np.random.random()*10))
        btn2 = Gtk.Button(label="Adicionar dados no Gráfico 2")
        btn2.connect("clicked", lambda w: self.graph2.update(len(self.graph2.xdata)+1,
                                                              np.random.random()*10))
        btn_hbox.append(btn1); btn_hbox.append(btn2)

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.twoplots")

    def do_activate(self):
        win = PlotWindow(self)
        win.present()

if __name__ == "__main__":
    App().run()