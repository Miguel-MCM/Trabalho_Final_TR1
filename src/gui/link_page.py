import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk # type:ignore

class LinkPage(Gtk.Box):
    def __init__(self, size:tuple[int, int]):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.set_css_classes(["link_page"])
        self.set_margin_start(20)
        self.set_margin_end(20)
        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_size_request(size[0], size[1])
        self.set_hexpand(True)
        self.set_vexpand(False)

        # Título
        title = Gtk.Label(label="Camada de Enlace")
        title.set_markup("<span size='large' weight='bold'>Camada de Enlace</span>")
        title.set_css_classes(["link_title"])
        self.append(title)

        # Container principal com duas colunas
        main_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        main_container.set_hexpand(True)
        self.append(main_container)

        # Coluna Input
        input_column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        input_column.set_hexpand(True)
        input_column.set_css_classes(["input_column"])
        
        # Label Input
        input_label = Gtk.Label(label="Entrada")
        input_label.set_markup("<span size='medium' weight='bold'>Entrada</span>")
        input_label.set_css_classes(["section_label"])
        input_column.append(input_label)

        # Grid para Input
        input_grid = Gtk.Grid()
        input_grid.set_row_spacing(5)
        input_grid.set_css_classes(["input_grid"])
        input_column.append(input_grid)

        # Header Input
        frame1_input = Gtk.Frame(label="Dados")
        frame1_input.set_css_classes(["link_frame"])
        vbox1_input = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame1_input.set_child(vbox1_input)
        self.link_input1 = Gtk.TextView()
        self.link_input1.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_input1.set_editable(False)
        self.link_input1.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_input1.set_cursor_visible(False)
        self.link_input1.set_monospace(True)
        self.link_input1.set_hexpand(True)
        self.link_input1.set_vexpand(False)
        self.link_input1.set_css_classes(["link_textview"])
        vbox1_input.append(self.link_input1)
        input_grid.attach(frame1_input, 0, 0, 1, 1)

        # Data Input
        frame2_input = Gtk.Frame(label="Detecção e Correção de Erro")
        frame2_input.set_css_classes(["link_frame"])
        vbox2_input = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame2_input.set_child(vbox2_input)
        self.link_input2 = Gtk.TextView()
        self.link_input2.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_input2.set_editable(False)
        self.link_input2.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_input2.set_cursor_visible(False)
        self.link_input2.set_monospace(True)
        self.link_input2.set_hexpand(True)
        self.link_input2.set_vexpand(False)
        self.link_input2.set_css_classes(["link_textview"])
        vbox2_input.append(self.link_input2)
        input_grid.attach(frame2_input, 0, 1, 1, 1)

        # EDC Input
        frame3_input = Gtk.Frame(label="Enquadramento")
        frame3_input.set_css_classes(["link_frame"])
        vbox3_input = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame3_input.set_child(vbox3_input)
        self.link_input3 = Gtk.TextView()
        self.link_input3.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_input3.set_editable(False)
        self.link_input3.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_input3.set_cursor_visible(False)
        self.link_input3.set_monospace(True)
        self.link_input3.set_hexpand(True)
        self.link_input3.set_vexpand(False)
        self.link_input3.set_css_classes(["link_textview"])
        vbox3_input.append(self.link_input3)
        input_grid.attach(frame3_input, 0, 2, 1, 1)

        # Bit Enviados Input
        frame4_input = Gtk.Frame(label="Bit Enviados")
        frame4_input.set_css_classes(["link_frame"])
        vbox4_input = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame4_input.set_child(vbox4_input)
        self.link_input4 = Gtk.TextView()
        self.link_input4.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_input4.set_editable(False)
        self.link_input4.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_input4.set_cursor_visible(False)
        self.link_input4.set_monospace(True)
        self.link_input4.set_hexpand(True)
        self.link_input4.set_vexpand(False)
        self.link_input4.set_css_classes(["link_textview"])
        vbox4_input.append(self.link_input4)
        input_grid.attach(frame4_input, 0, 3, 1, 1)

        main_container.append(input_column)

        # Coluna Output
        output_column = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        output_column.set_hexpand(True)
        output_column.set_css_classes(["output_column"])
        
        # Label Output
        output_label = Gtk.Label(label="Saída")
        output_label.set_markup("<span size='medium' weight='bold'>Saída</span>")
        output_label.set_css_classes(["section_label"])
        output_column.append(output_label)

        # Grid para Output
        output_grid = Gtk.Grid()
        output_grid.set_row_spacing(5)
        output_grid.set_css_classes(["output_grid"])
        output_column.append(output_grid)

        # Header Output
        frame1_output = Gtk.Frame(label="Dados")
        frame1_output.set_css_classes(["link_frame"])
        vbox1_output = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame1_output.set_child(vbox1_output)
        self.link_output1 = Gtk.TextView()
        self.link_output1.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_output1.set_editable(False)
        self.link_output1.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_output1.set_cursor_visible(False)
        self.link_output1.set_monospace(True)
        self.link_output1.set_hexpand(True)
        self.link_output1.set_vexpand(False)
        self.link_output1.set_css_classes(["link_textview"])
        vbox1_output.append(self.link_output1)
        output_grid.attach(frame1_output, 0, 0, 1, 1)

        # Data Output
        frame2_output = Gtk.Frame(label="Detecção e Correção de Erro")
        frame2_output.set_css_classes(["link_frame"])
        vbox2_output = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame2_output.set_child(vbox2_output)
        self.link_output2 = Gtk.TextView()
        self.link_output2.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_output2.set_editable(False)
        self.link_output2.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_output2.set_cursor_visible(False)
        self.link_output2.set_monospace(True)
        self.link_output2.set_hexpand(True)
        self.link_output2.set_vexpand(False)
        self.link_output2.set_css_classes(["link_textview"])
        vbox2_output.append(self.link_output2)
        output_grid.attach(frame2_output, 0, 1, 1, 1)

        # EDC Output
        frame3_output = Gtk.Frame(label="Desenquadramento")
        frame3_output.set_css_classes(["link_frame"])
        vbox3_output = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame3_output.set_child(vbox3_output)
        self.link_output3 = Gtk.TextView()
        self.link_output3.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_output3.set_editable(False)
        self.link_output3.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_output3.set_cursor_visible(False)
        self.link_output3.set_monospace(True)
        self.link_output3.set_hexpand(True)
        self.link_output3.set_vexpand(False)
        self.link_output3.set_css_classes(["link_textview"])
        vbox3_output.append(self.link_output3)
        output_grid.attach(frame3_output, 0, 2, 1, 1)

        # Bit Enviados Output
        frame4_output = Gtk.Frame(label="Bit Recebidos")
        frame4_output.set_css_classes(["link_frame"])
        vbox4_output = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        frame4_output.set_child(vbox4_output)
        self.link_output4 = Gtk.TextView()
        self.link_output4.set_size_request(size[0]//2 - 30, size[1]//4)
        self.link_output4.set_editable(False)
        self.link_output4.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.link_output4.set_cursor_visible(False)
        self.link_output4.set_monospace(True)
        self.link_output4.set_hexpand(True)
        self.link_output4.set_vexpand(False)
        self.link_output4.set_css_classes(["link_textview"])
        vbox4_output.append(self.link_output4)
        output_grid.attach(frame4_output, 0, 3, 1, 1)

        

        main_container.append(output_column)

    # Setters
    def set_data_input(self, data:str):
        self.link_input1.get_buffer().set_text(data)

    def set_data_output(self, data:str):
        self.link_output1.get_buffer().set_text(data)

    def set_edc_input(self, edc:str):
        self.link_input2.get_buffer().set_text(edc)

    def set_edc_output(self, edc:str):
        self.link_output2.get_buffer().set_text(edc)

    def set_frame_input(self, frame:str):
        self.link_input3.get_buffer().set_text(frame)

    def set_frame_output(self, frame:str):
        self.link_output3.get_buffer().set_text(frame)

    def set_sent_bits_input(self, bits:str):
        self.link_input4.get_buffer().set_text(bits)

    def set_received_bits_output(self, bits:str):
        self.link_output4.get_buffer().set_text(bits)