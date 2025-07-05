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
    def __init__(self, title:str|None = None, xlabel:str|None = None, ylabel:str|None = None, size:tuple[int, int] = (300, 200)):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        # Configurar para não expandir
        self.set_hexpand(False)
        self.set_vexpand(False)
        
        # Calcular figsize baseado no tamanho fornecido
        width_inches = size[0] / 100  # Converter pixels para polegadas
        height_inches = size[1] / 100
        
        # Configurar tema escuro para matplotlib
        self.fig = Figure(figsize=(width_inches, height_inches), dpi=100, facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot()
        
        # Aplicar estilo escuro
        self.fig.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.ax.spines['bottom'].set_color('#ffffff')
        self.ax.spines['top'].set_color('#ffffff')
        self.ax.spines['left'].set_color('#ffffff')
        self.ax.spines['right'].set_color('#ffffff')
        self.ax.tick_params(colors='#ffffff')
        self.ax.xaxis.label.set_color('#ffffff')
        self.ax.yaxis.label.set_color('#ffffff')
        self.ax.title.set_color('#ffffff')
        
        # Configurar grade
        self.ax.grid(True, color='#404040', alpha=0.3)
        
        self.line, = self.ax.plot([], [], color='#00ff00', linewidth=1.5)  # Linha verde para contraste
        if title:
            self.ax.set_title(title, color='#ffffff', fontsize=10)
        if xlabel:
            self.ax.set_xlabel(xlabel, color='#ffffff')
        if ylabel:
            self.ax.set_ylabel(ylabel, color='#ffffff')

        self.canvas = FigureCanvas(self.fig)
        self.canvas.set_size_request(size[0], size[1])
        
        # Configurar fundo do canvas para tema escuro
        self.canvas.set_css_classes(["dark_canvas"])
        
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