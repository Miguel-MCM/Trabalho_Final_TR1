import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk # type:ignore

from gui.graph_frame import GraphFrame

import numpy as np

class PhysicalPage(Gtk.Box):
    def __init__(self, size:tuple[int, int]):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.size = size
        self.set_css_classes(["physical_page"])
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_size_request(size[0], size[1])
        self.set_hexpand(True)
        self.set_vexpand(False)

        # Título
        title = Gtk.Label(label="Camada Física")
        title.set_markup("<span size='large' weight='bold'>Camada Física</span>")
        self.append(title)

        # Container principal para os gráficos
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_container.set_hexpand(True)
        main_container.set_vexpand(True)
        self.append(main_container)

        # Grid 2x2 para os 4 gráficos
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        # Configurar o grid para não expandir os widgets
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        main_container.append(grid)

        # Tamanho fixo dos gráficos
        graph_width = size[0]//2  # Tamanho fixo em pixels
        graph_height = size[1]  # Tamanho fixo em pixels

        # Gráfico 1: Codificador Banda Base
        self.graph1 = GraphFrame(
            title="Codificador Banda Base",
            size=(graph_width, graph_height),
            xlabel="Tempo (s)",
            ylabel="Amplitude"
        )
        self.graph1.set_size_request(graph_width, graph_height)
        self.graph1.set_hexpand(False)
        grid.attach(self.graph1, 0, 0, 1, 1)

        # Gráfico 4: Decodificador Banda Base
        self.graph4 = GraphFrame(
            title="Decodificador Banda Base",
            size=(graph_width, graph_height),
            xlabel="Tempo (s)",
            ylabel="Amplitude"
        )
        self.graph4.set_size_request(graph_width, graph_height)
        self.graph4.set_hexpand(False)
        grid.attach(self.graph4, 1, 0, 1, 1)

    def update_encoder_graph(self, x:np.ndarray, y:np.ndarray):
        self.graph1.update(x, y)

    def update_decoder_graph(self, x:np.ndarray, y:np.ndarray):
        self.graph4.update(x, y)