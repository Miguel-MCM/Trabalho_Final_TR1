#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk # type:ignore

import numpy as np
from gui.config_page import ConfigPage
from gui.aplication_frame import AplicationFrame
from gui.link_page import LinkPage
from gui.physical_page import PhysicalPage

from base_window import BaseWindow

class Window(BaseWindow, Gtk.ApplicationWindow):
    def __init__(self, app):
        # Inicializar BaseWindow primeiro
        BaseWindow.__init__(self)
        # Inicializar Gtk.ApplicationWindow
        Gtk.ApplicationWindow.__init__(self, application=app, title="Sistema de Comunicação")
        
        self.size = (720, 480)
        self.set_default_size(*self.size)

        # Aplicar modo escuro
        self.apply_dark_theme()

        # Container principal
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(main_vbox)

        # Criar seção de entrada/saída sempre visível
        main_vbox.append(AplicationFrame(on_process_text=self.on_process_text, set_variables={ "input_text": self.set_input_text }))

        # Notebook para organizar os 4 segmentos
        notebook = Gtk.Notebook()
        main_vbox.append(notebook)

        # 1. Segmento de Configurações
        config_page_variables = {
            "frame_size": self.set_max_frame_size,
            "modulation": self.set_modulation,
            "bit_rate": self.set_bit_rate,
            "sample_rate": self.set_sample_rate,
            "coding": self.set_coding,
            "error_detection": self.set_error_detection,
            "snr": self.set_snr,
        }

        config_page = ConfigPage(
            (self.size[0] - 32, self.size[1] - 32),
            coding_options=self.coding_options_names,
            error_detection_options=self.error_detection_options_names,
            modulation_options=self.modulation_options_names,
            analog_modulation_options=["FSK", "PSK", "QAM"],
            set_variables=config_page_variables
            )
        notebook.append_page(config_page, Gtk.Label(label="Configurações"))

        
        # 2. Segmento de Enlace
        self.link_page = LinkPage((self.size[0] - 32, self.size[1] - 32))
        notebook.append_page(self.link_page, Gtk.Label(label="Enlace"))

        # 3. Segmento Físico
        self.physical_page = PhysicalPage((self.size[0] - 32, self.size[1] - 32))
        notebook.append_page(self.physical_page, Gtk.Label(label="Física"))

        notebook.set_current_page(1)

    def apply_dark_theme(self):
        """Aplica o tema escuro à aplicação"""
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("src/main.css")
        
        display = Gdk.Display.get_default()
        if display:
            Gtk.StyleContext.add_provider_for_display(
                display,
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

    def on_process_text(self, button):
        """Callback para processar texto"""
        bits = ''.join(format(ord(char), '08b') for char in self.input_text[:self.max_frame_size])
        print(bits)

        self.link_page.set_data_input(bits)
        self.process_frame(np.array([int(bit) for bit in bits]))

    def process_frame(self, bits:np.ndarray):
        encoded_bits = self.modulator.modulate(bits)
        x = np.linspace(0, len(encoded_bits) / self.sample_rate, num=len(encoded_bits))
        self.physical_page.update_encoder_graph(x, encoded_bits)

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.communication")

    def do_activate(self):
        win = Window(self)
        win.present()

if __name__ == "__main__":
    App().run(None)