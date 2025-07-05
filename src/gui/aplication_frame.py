import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk # type:ignore

from collections.abc import Callable

class AplicationFrame(Gtk.Frame):
    def __init__(self, on_process_text: Callable[[], None], set_variables:dict[str, Callable[[str], None]] = {}):
        super().__init__()
        self.set_css_classes(["aplication_frame"])
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_hexpand(True)
        self.set_vexpand(False)
        self.set_variables = set_variables

        # Container vertical para organizar entrada e saída
        section_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(section_vbox)

        # Container horizontal para entrada e saída
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        section_vbox.append(hbox)

        # Lado esquerdo - Entrada
        input_frame = Gtk.Frame(label="Entrada")
        input_frame.set_label_align(0.5)
        input_vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        input_frame.set_child(input_vbox)

        # Entrada de texto
        input_vbox.append(Gtk.Label(label="Texto:"))
        self.input_text = Gtk.TextView()
        self.input_text.set_size_request(200, 24) 
        self.input_text.set_hexpand(True)
        self.input_text.set_vexpand(True)  # Permitir expansão vertical
        self.input_text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)  # Habilitar quebra de texto
        self.input_text.set_name("input_text")
        self.input_text.get_buffer().connect('changed', lambda *_: self.update_input_text())
        self.input_text.get_buffer().connect('changed', lambda *_: self.set_variables['input_text'](self.get_text_view_text(self.input_text)))
        input_vbox.append(self.input_text)

        # Bits de entrada (readonly)
        input_vbox.append(Gtk.Label(label="Bytes:"))
        self.input_bits = Gtk.TextView()
        self.input_bits.set_size_request(200, 24)
        self.input_bits.set_hexpand(True)
        self.input_bits.set_vexpand(True)  # Permitir expansão vertical
        self.input_bits.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)  # Habilitar quebra de texto
        self.input_bits.set_editable(False)
        input_vbox.append(self.input_bits)

        hbox.append(input_frame)

        # Botão de processar
        process_button = Gtk.Button(label="Processar →")
        process_button.connect("clicked", on_process_text)
        hbox.append(process_button)

        # Lado direito - Saída
        output_frame = Gtk.Frame(label="Saída")
        output_frame.set_label_align(0.5)
        output_vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        output_frame.set_child(output_vbox)

        # Saída de texto
        output_vbox.append(Gtk.Label(label="Texto:"))
        self.output_text = Gtk.TextView()
        self.output_text.set_size_request(200, 24)
        self.output_text.set_hexpand(True)
        self.output_text.set_editable(False)
        output_vbox.append(self.output_text)

        # Bits de saída (readonly)
        output_vbox.append(Gtk.Label(label="Bytes:"))
        self.output_bits = Gtk.TextView()
        self.output_bits.set_size_request(200, 24)
        self.output_bits.set_hexpand(True)
        self.output_bits.set_editable(False)
        output_vbox.append(self.output_bits)

        hbox.append(output_frame)

    def get_text_view_text(self, text_view: Gtk.TextView) -> str:
        buffer = text_view.get_buffer()
        return buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

    def update_input_text(self):
        text = self.get_text_view_text(self.input_text)
        self.input_bits.get_buffer().set_text(''.join(format(ord(char), '02x') for char in text))

    def update_output(self, text: str):
        self.output_text.get_buffer().set_text(text)
        self.output_bits.get_buffer().set_text(''.join(format(ord(char), '02x') for char in text))