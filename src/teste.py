#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk # type:ignore

import numpy as np
from gui.graph_frame import GraphFrame
from gui.config_page import ConfigPage
from gui.base_window import BaseWindow
from gui.aplication_frame import AplicationFrame
from gui.link_page import LinkPage

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
        physical_page = self.create_physical_page()
        notebook.append_page(physical_page, Gtk.Label(label="Física"))

    def process_data_through_layers(self, input_text: str) -> dict:
        """Processa dados através de todas as camadas usando os objetos configurados"""
        result = {
            'input_text': input_text,
            'input_bits': '',
            'coded_data': '',
            'error_detection_data': '',
            'flow_control_data': '',
            'final_link_data': '',
            'modulated_signal': None,
            'demodulated_signal': None
        }
        
        # Camada de Aplicação: Converter texto para bits
        input_bits = ''.join(format(ord(char), '08b') for char in input_text)
        result['input_bits'] = ' '.join(input_bits[i:i+8] for i in range(0, len(input_bits), 8))
        
        # Converter string de bits para numpy array
        bits_array = np.array([int(bit) for bit in input_bits])
        
        # Camada de Enlace: Codificação
        if self.coding is not None:
            try:
                coded_data = self.coding.frame_data(bits_array)
                # Converter de volta para string formatada
                coded_bits = ''.join(str(bit) for bit in coded_data)
                result['coded_data'] = ' '.join(coded_bits[i:i+8] for i in range(0, len(coded_bits), 8))
            except Exception as e:
                print(f"Erro na codificação: {e}")
                result['coded_data'] = result['input_bits']
        else:
            result['coded_data'] = result['input_bits']
        
        # Camada de Enlace: Detecção de Erro
        if self.error_detector is not None:
            try:
                # Converter dados codificados para numpy array
                coded_bits = result['coded_data'].replace(' ', '')
                coded_array = np.array([int(bit) for bit in coded_bits])
                
                if hasattr(self.error_detector, 'add_trailer'):
                    error_data = self.error_detector.add_trailer(coded_array)
                    error_bits = ''.join(str(bit) for bit in error_data)
                    result['error_detection_data'] = ' '.join(error_bits[i:i+8] for i in range(0, len(error_bits), 8))
                else:
                    result['error_detection_data'] = result['coded_data']
            except Exception as e:
                print(f"Erro na detecção de erro: {e}")
                result['error_detection_data'] = result['coded_data']
        else:
            result['error_detection_data'] = result['coded_data']
        
        # Camada de Enlace: Controle de Fluxo (simulado)
        result['flow_control_data'] = result['error_detection_data']
        
        # Camada de Enlace: Dados Finais
        result['final_link_data'] = result['flow_control_data']
        
        # Camada Física: Modulação
        if self.modulator is not None:
            try:
                # Converter bits para array numpy para modulação
                final_bits = result['final_link_data'].replace(' ', '')
                bits_array = np.array([int(bit) for bit in final_bits])
                modulated_signal = self.modulator.modulate(bits_array)
                result['modulated_signal'] = modulated_signal
                
                # Simular demodulação
                result['demodulated_signal'] = self.modulator.demodulate(modulated_signal)
            except Exception as e:
                print(f"Erro na modulação: {e}")
        
        return result

    def update_all_displays(self, result: dict):
        """Atualiza todos os displays com os dados processados"""
        # Atualizar camada de aplicação
        input_bits_buffer = self.input_bits.get_buffer()
        input_bits_buffer.set_text(result['input_bits'])
        
        output_text_buffer = self.output_text.get_buffer()
        output_text_buffer.set_text(result['input_text'])  # Por enquanto, saída = entrada
        
        output_bits_buffer = self.output_bits.get_buffer()
        output_bits_buffer.set_text(result['input_bits'])
        

        
        # Atualizar camada de enlace
        self.link_output1.get_buffer().set_text(result['coded_data'])
        self.link_output2.get_buffer().set_text(result['error_detection_data'])
        self.link_output3.get_buffer().set_text(result['flow_control_data'])
        self.link_output4.get_buffer().set_text(result['final_link_data'])
        
        # Atualizar gráficos da camada física
        if result['modulated_signal'] is not None:
            self.update_physical_graphs(result)

    def update_physical_graphs(self, result: dict):
        """Atualiza os gráficos da camada física"""
        # Gerar dados de tempo
        t = np.linspace(0, 1, 1000)
        
        # Sinal original (bits)
        bits = result['final_link_data'].replace(' ', '')
        signal_original = np.array([int(bit) for bit in bits])
        # Repetir o sinal para preencher o tempo
        signal_original = np.tile(signal_original, len(t) // len(signal_original) + 1)[:len(t)]
        self.graph1.update(t, signal_original)
        
        # Sinal modulado
        if result['modulated_signal'] is not None:
            modulated_t = np.linspace(0, len(result['modulated_signal']) / self.sample_rate, len(result['modulated_signal']))
            self.graph2.update(modulated_t, result['modulated_signal'])
            
            # Espectro de frequência
            f = np.linspace(0, self.sample_rate/2, 500)
            spectrum = np.abs(np.fft.fft(result['modulated_signal']))
            # Garantir que o espectro tenha o mesmo tamanho que f
            if len(spectrum) > len(f):
                spectrum = spectrum[:len(f)]
            elif len(spectrum) < len(f):
                # Preencher com zeros se necessário
                spectrum = np.pad(spectrum, (0, len(f) - len(spectrum)), 'constant')
            self.graph3.update(f, spectrum)
        
        # Sinal demodulado
        if result['demodulated_signal'] is not None:
            demodulated_t = np.linspace(0, len(result['demodulated_signal']) / self.sample_rate, len(result['demodulated_signal']))
            self.graph4.update(demodulated_t, result['demodulated_signal'])

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

    def create_physical_page(self):
        """Cria a página física com 4 gráficos usando GraphFrame"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page.set_margin_start(10)
        page.set_margin_end(10)
        page.set_margin_top(10)
        page.set_margin_bottom(10)

        # Título
        title = Gtk.Label(label="Camada Física")
        title.set_markup("<span size='large' weight='bold'>Camada Física</span>")
        page.append(title)

        # Grid 2x2 para os 4 gráficos
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        page.append(grid)

        # Gráfico 1: Sinal Original
        self.graph1 = GraphFrame("Sinal Original", "Tempo (s)", "Amplitude", (self.size[0]//2 - 20, self.size[1]//2 - 20))
        grid.attach(self.graph1, 0, 0, 1, 1)

        # Gráfico 2: Sinal Modulado
        self.graph2 = GraphFrame("Sinal Modulado", "Tempo (s)", "Amplitude", (self.size[0]//2 - 20, self.size[1]//2 - 20))
        grid.attach(self.graph2, 1, 0, 1, 1)

        # Gráfico 3: Espectro de Frequência
        self.graph3 = GraphFrame("Espectro de Frequência", "Frequência (Hz)", "Magnitude", (self.size[0]//2 - 20, self.size[1]//2 - 20))
        grid.attach(self.graph3, 0, 1, 1, 1)

        # Gráfico 4: Sinal Demodulado
        self.graph4 = GraphFrame("Sinal Demodulado", "Tempo (s)", "Amplitude", (self.size[0]//2 - 20, self.size[1]//2 - 20))
        grid.attach(self.graph4, 1, 1, 1, 1)

        # Botão para atualizar gráficos
        update_button = Gtk.Button(label="Atualizar Gráficos")
        update_button.connect("clicked", self.on_update_graphs)
        page.append(update_button)

        return page

    def on_process_text(self, button):
        """Callback para processar texto"""
        # Obter texto de entrada
        bits = ''.join(format(ord(char), '08b') for char in self.input_text)
        print(bits)
        self.link_page.set_data_input(bits)


    def on_update_graphs(self, button):
        """Callback para atualizar gráficos"""
        # Obter texto de entrada atual
        text_buffer = self.input_text.get_buffer()
        start, end = text_buffer.get_bounds()
        input_text = text_buffer.get_text(start, end, True)
        
        if not input_text.strip():
            # Se não há texto, usar dados de exemplo
            input_text = "Hello World"
        
        # Processar dados através de todas as camadas
        result = self.process_data_through_layers(input_text)
        
        # Atualizar gráficos da camada física
        self.update_physical_graphs(result)

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.example.communication")

    def do_activate(self):
        win = Window(self)
        win.present()

if __name__ == "__main__":
    App().run(None)