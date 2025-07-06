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
        self.aplication_frame = AplicationFrame(on_process_text=self.on_process_text, set_variables={ "input_text": self.set_input_text })
        main_vbox.append(self.aplication_frame)

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

        self.link_page.set_data_input(bits)
        self.process_frame(np.array([int(bit) for bit in bits]))

    def process_frame(self, bits:np.ndarray):

        deframe_failed = False
        edc_failed = False

        if self.coding is not None and self.error_detector is not None:
            try:
                bits_with_edc = self.coding.add_edc(bits)
                self.link_page.set_edc_input(''.join(map(lambda x: str(int(x)), bits_with_edc)))
            except Exception as e:
                bits_with_edc = bits
                self.link_page.set_edc_input(e.args[0])
        else:
            bits_with_edc = bits
            self.link_page.set_edc_input('Nenhum')

        if self.coding is not None:
            try:
                framed_bits = self.coding.frame_data(bits)
                self.link_page.set_frame_input(''.join(map(lambda x: str(int(x)), framed_bits)))
            except Exception as e:
                framed_bits = bits_with_edc
                self.link_page.set_frame_input(e.args[0])
        else:
            framed_bits = bits_with_edc
            self.link_page.set_frame_input('Nenhum')

        self.link_page.set_sent_bits_input(''.join(map(lambda x: str(int(x)), framed_bits)))


        encoded_bits = self.modulator.modulate(framed_bits)
        x = np.linspace(0, len(encoded_bits) / self.sample_rate, num=len(encoded_bits))
        self.physical_page.update_encoder_graph(x, encoded_bits)

        self.communication.send(encoded_bits)
        received_bits = self.communication.receive()
        self.physical_page.update_decoder_graph(x, received_bits)

        decoded_bits = self.modulator.demodulate(received_bits)
        self.link_page.set_received_bits_output(''.join(map(lambda x: str(int(x)), decoded_bits)))

        if self.coding is not None:
            try:
                deframed_bits = self.coding.deframe_data(decoded_bits)
                self.link_page.set_frame_output(''.join(map(lambda x: str(int(x)), deframed_bits)))
            except Exception as e:
                deframed_bits = decoded_bits
                self.link_page.set_frame_output(e.args[0])
                deframe_failed = True
        else:
            deframed_bits = decoded_bits
            self.link_page.set_frame_output('Nenhum')

        if deframe_failed:
            self.link_page.set_edc_output('Falha no desenquadramento')
            self.link_page.set_data_output('Falha no desenquadramento')
            self.aplication_frame.update_output("Falha no desenquadramento")
            return

        if self.coding is not None and self.error_detector is not None:
            try:
                if (error := self.coding.check_edc(deframed_bits)):
                    raise ValueError(error)
                no_error_bits = self.coding.remove_edc(deframed_bits)
                self.link_page.set_edc_output(''.join(map(lambda x: str(int(x)), no_error_bits)))
            except Exception as e:
                no_error_bits = deframed_bits
                self.link_page.set_edc_output(e.args[0])
                edc_failed = True
        else:
            no_error_bits = deframed_bits
            self.link_page.set_edc_output('Nenhum')

        self.link_page.set_data_output(''.join(map(lambda x: str(int(x)), no_error_bits)))

        if edc_failed:
            self.link_page.set_data_output('Falha no EDC')
            self.aplication_frame.update_output("Falha no EDC")
            return

        # Convert bits back to text for output
        try:
            # Convert bits to bytes
            bit_string = ''.join(map(str, no_error_bits))
            # Pad to complete bytes if necessary
            if len(bit_string) % 8 != 0:
                bit_string = bit_string.ljust(len(bit_string) + (8 - len(bit_string) % 8), '0')
            
            # Convert bytes to text
            output_text = ''
            for i in range(0, len(bit_string), 8):
                byte = bit_string[i:i+8]
                if byte:
                    char_code = int(byte, 2)
                    if char_code < 128:  # Only printable ASCII
                        output_text += chr(char_code)
            
            # Update the application frame output
            self.aplication_frame.update_output(output_text)
        except Exception as e:
            self.aplication_frame.update_output(f"Erro na decodificação: {str(e)}")




class Simulator(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.communication")

    def do_activate(self):
        win = Window(self)
        win.present()

if __name__ == "__main__":
    Simulator().run(None)