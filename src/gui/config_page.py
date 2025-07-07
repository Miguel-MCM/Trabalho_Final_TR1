import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk # type:ignore

from collections.abc import Callable

class ConfigPage(Gtk.Box):
    def __init__(self, size:tuple[int, int], 
    coding_options:list[str], error_detection_options:list[str], error_correction_options:list[str], modulation_options:list[str], analog_modulation_options:list[str],
    set_variables:dict[str, Callable[[str], None]] = {}):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_margin_start(size[0]//4)
        self.set_margin_end(size[0]//4)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.set_size_request(size[0]//2, size[1])

        self.set_variables = set_variables

        # Título
        title = Gtk.Label(label="Configurações Gerais")
        title.set_markup("<span size='large' weight='bold'>Configurações de Enlace e Erro</span>")
        self.append(title)

        # Grid para organizar os controles
        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_hexpand(True)
        grid.set_vexpand(True)
        self.append(grid)

        # Configurar as colunas para terem tamanho igual
        grid.set_column_homogeneous(True)

        # Frame size
        frame_size_label = Gtk.Label(label="Tamanho máximo do quadro (bytes):")
        frame_size_label.set_hexpand(True)
        frame_size_label.set_halign(Gtk.Align.START)
        grid.attach(frame_size_label, 0, 0, 1, 1)
        
        self.frame_size_entry = Gtk.Entry()
        self.frame_size_entry.set_name("frame_size")
        self.frame_size_entry.set_text("10")
        set_v_id = self.frame_size_entry.connect_after('changed',self.set_variable, self.frame_size_entry.get_text)
        self.frame_size_entry.connect('changed', self.check_numeric_entry, [set_v_id])
        self.frame_size_entry.set_hexpand(True)
        grid.attach(self.frame_size_entry, 1, 0, 1, 1)

        # frame type
        frame_type_label = Gtk.Label(label="Tipo de enquadramento:")
        frame_type_label.set_hexpand(True)
        frame_type_label.set_halign(Gtk.Align.START)
        grid.attach(frame_type_label, 0, 1, 1, 1)
        
        self.coding_dropdown = Gtk.DropDown()
        self.coding_dropdown.set_name("coding")
        self.coding_dropdown.set_model(Gtk.StringList.new(coding_options))
        self.coding_dropdown.set_selected(0)
        self.coding_dropdown.connect_after('notify::selected', lambda *_: self.set_variable(self.coding_dropdown, self.coding_dropdown.get_selected))
        self.coding_dropdown.set_show_arrow(True)
        self.coding_dropdown.set_hexpand(True)
        grid.attach(self.coding_dropdown, 1, 1, 1, 1)


        # Error detection
        error_detection_label = Gtk.Label(label="Detecção de Erro:")
        error_detection_label.set_hexpand(True)
        error_detection_label.set_halign(Gtk.Align.START)
        grid.attach(error_detection_label, 0, 2, 1, 1)
        
        self.error_detection_combo = Gtk.DropDown()
        self.error_detection_combo.set_name("error_detection")
        self.error_detection_combo.set_model(Gtk.StringList.new(error_detection_options))
        self.error_detection_combo.set_selected(0)
        self.error_detection_combo.connect_after('notify::selected', lambda *_: self.set_variable(self.error_detection_combo, self.error_detection_combo.get_selected))
        self.error_detection_combo.set_show_arrow(True)
        self.error_detection_combo.set_hexpand(True)
        grid.attach(self.error_detection_combo, 1, 2, 1, 1)

        # Error correction
        error_correction_label = Gtk.Label(label="Correção de Erro:")
        error_correction_label.set_hexpand(True)
        error_correction_label.set_halign(Gtk.Align.START)
        grid.attach(error_correction_label, 0, 3, 1, 1)
        
        self.error_correction_combo = Gtk.DropDown()
        self.error_correction_combo.set_name("error_correction")
        self.error_correction_combo.set_model(Gtk.StringList.new(error_correction_options))
        self.error_correction_combo.set_selected(0)
        self.error_correction_combo.connect_after('notify::selected', lambda *_: self.set_variable(self.error_correction_combo, self.error_correction_combo.get_selected))
        self.error_correction_combo.set_show_arrow(True)
        self.error_correction_combo.set_hexpand(True)
        grid.attach(self.error_correction_combo, 1, 3, 1, 1)

        # SNR
        snr_label = Gtk.Label(label="SNR:")
        snr_label.set_hexpand(True)
        snr_label.set_halign(Gtk.Align.START)
        grid.attach(snr_label, 0, 4, 1, 1)
        
        self.snr_entry = Gtk.Entry()
        self.snr_entry.set_name("snr")
        self.snr_entry.set_text("10")
        id_set_v = self.snr_entry.connect_after('changed', lambda *_: self.set_variable(self.snr_entry, self.snr_entry.get_text))
        self.snr_entry.connect('changed', self.check_numeric_entry, [id_set_v], True)
        self.snr_entry.set_hexpand(True)
        grid.attach(self.snr_entry, 1, 4, 1, 1)

        # Digital Modulation Config
        dg_title = Gtk.Label(label="Configurações de Modulação Digital")
        dg_title.set_markup("<span size='large' weight='bold'>Configurações de Modulação Digital</span>")
        self.append(dg_title)

        # Grid para organizar os controles
        dg_grid = Gtk.Grid()
        dg_grid.set_row_spacing(10)
        dg_grid.set_column_spacing(10)
        dg_grid.set_hexpand(True)
        dg_grid.set_vexpand(True)
        self.append(dg_grid)

        # Configurar as colunas para terem tamanho igual
        dg_grid.set_column_homogeneous(True)

        # Digital modulation type
        digital_modulation_label = Gtk.Label(label="Tipo de Modulação Digital:")
        digital_modulation_label.set_hexpand(True)
        digital_modulation_label.set_halign(Gtk.Align.START)
        dg_grid.attach(digital_modulation_label, 0, 0, 1, 1)
        
        self.modulation_combo = Gtk.DropDown()
        self.modulation_combo.set_name("modulation")
        self.modulation_combo.set_model(Gtk.StringList.new(modulation_options))
        self.modulation_combo.set_selected(0)
        self.modulation_combo.connect_after('notify::selected', lambda *_: self.set_variable(self.modulation_combo, self.modulation_combo.get_selected))
        self.modulation_combo.set_show_arrow(True)
        self.modulation_combo.set_hexpand(True)
        dg_grid.attach(self.modulation_combo, 1, 0, 1, 1)

        # Bit rate
        bit_rate_label = Gtk.Label(label="Taxa de Bits (bps):")
        bit_rate_label.set_hexpand(True)
        bit_rate_label.set_halign(Gtk.Align.START)
        dg_grid.attach(bit_rate_label, 0, 1, 1, 1)

        # Bit rate entry
        self.bit_rate_entry = Gtk.Entry()
        self.bit_rate_entry.set_name("bit_rate")
        self.bit_rate_entry.set_text("1000")
        id_set_v = self.bit_rate_entry.connect_after('changed', lambda *_: self.set_variable(self.bit_rate_entry, self.bit_rate_entry.get_text))
        self.bit_rate_entry.connect('changed', self.check_numeric_entry, [id_set_v], True)
        self.bit_rate_entry.set_hexpand(True)
        dg_grid.attach(self.bit_rate_entry, 1, 1, 1, 1)

        # Sample rate
        sample_rate_label = Gtk.Label(label="Taxa de Amostragem (Hz):")
        sample_rate_label.set_hexpand(True)
        sample_rate_label.set_halign(Gtk.Align.START)
        dg_grid.attach(sample_rate_label, 0, 2, 1, 1)

        # Sample rate entry
        self.sample_rate_entry = Gtk.Entry()
        self.sample_rate_entry.set_name("sample_rate")
        self.sample_rate_entry.set_text("10000")
        id_set_v = self.sample_rate_entry.connect_after('changed', lambda *_: self.set_variable(self.sample_rate_entry, self.sample_rate_entry.get_text))
        self.sample_rate_entry.connect('changed', self.check_numeric_entry, [id_set_v], True)
        self.sample_rate_entry.set_hexpand(True)
        dg_grid.attach(self.sample_rate_entry, 1, 2, 1, 1)

        # Carrier Modulation Switch
        carrier_switch_label = Gtk.Label(label="Usar Modulação de Portadora:")
        carrier_switch_label.set_hexpand(True)
        carrier_switch_label.set_halign(Gtk.Align.START)
        dg_grid.attach(carrier_switch_label, 0, 3, 1, 1)
        
        self.carrier_switch = Gtk.Switch()
        self.carrier_switch.set_name("use_carrier_modulation")
        self.carrier_switch.set_active(False)
        self.carrier_switch.connect('notify::active', lambda *_: self.set_variable(self.carrier_switch, self.carrier_switch.get_active))
        self.carrier_switch.set_hexpand(True)
        dg_grid.attach(self.carrier_switch, 1, 3, 1, 1)

        # Analog Modulation Config
        title = Gtk.Label(label="Configurações de Modulação Analógica")
        title.set_markup("<span size='large' weight='bold'>Configurações de Modulação Analógica</span>")
        self.append(title)
        
        # Grid para organizar os controles
        an_grid = Gtk.Grid()
        an_grid.set_row_spacing(10)
        an_grid.set_column_spacing(10)
        an_grid.set_hexpand(True)
        an_grid.set_vexpand(True)
        self.append(an_grid)

        # Configurar as colunas para terem tamanho igual
        an_grid.set_column_homogeneous(True)
        
        # Analog modulation type label
        analog_modulation_label = Gtk.Label(label="Tipo de Modulação Analógica:")
        analog_modulation_label.set_hexpand(True)
        analog_modulation_label.set_halign(Gtk.Align.START)
        an_grid.attach(analog_modulation_label, 0, 0, 1, 1)

        # Analog modulation type
        self.analog_modulation_combo = Gtk.DropDown()
        self.analog_modulation_combo.set_name("analog_modulation")
        self.analog_modulation_combo.set_model(Gtk.StringList.new(analog_modulation_options))
        self.analog_modulation_combo.set_selected(0)
        self.analog_modulation_combo.connect_after('notify::selected', lambda *_: self.set_variable(self.analog_modulation_combo, self.analog_modulation_combo.get_selected))
        self.analog_modulation_combo.set_show_arrow(True)
        self.analog_modulation_combo.set_hexpand(True)
        an_grid.attach(self.analog_modulation_combo, 1, 0, 1, 1)

        # Frequency
        frequency_label = Gtk.Label(label="Frequência da Portadora (Hz):")
        frequency_label.set_hexpand(True)
        frequency_label.set_halign(Gtk.Align.START)
        an_grid.attach(frequency_label, 0, 1, 1, 1)
        
        # Frequency entry
        self.analog_frequency_entry = Gtk.Entry()
        self.analog_frequency_entry.set_name("analog_frequency")
        self.analog_frequency_entry.set_text("1000")
        id_set_v = self.analog_frequency_entry.connect_after('changed', lambda *_: self.set_variable(self.analog_frequency_entry, self.analog_frequency_entry.get_text))
        self.analog_frequency_entry.connect('changed', self.check_numeric_entry, [id_set_v], True)
        self.analog_frequency_entry.set_hexpand(True)
        an_grid.attach(self.analog_frequency_entry, 1, 1, 1, 1)

        # Sample rate
        sample_rate_label = Gtk.Label(label="Taxa de Amostragem (Hz):")
        sample_rate_label.set_hexpand(True)
        sample_rate_label.set_halign(Gtk.Align.START)
        an_grid.attach(sample_rate_label, 0, 2, 1, 1)

        # Sample rate entry
        self.analog_sample_rate_entry = Gtk.Entry()
        self.analog_sample_rate_entry.set_name("analog_sample_rate")
        self.analog_sample_rate_entry.set_text("1000000")
        id_set_v = self.analog_sample_rate_entry.connect_after('changed', lambda *_: self.set_variable(self.analog_sample_rate_entry, self.analog_sample_rate_entry.get_text))
        self.analog_sample_rate_entry.connect('changed', self.check_numeric_entry, [id_set_v], True)
        self.analog_sample_rate_entry.set_hexpand(True)
        an_grid.attach(self.analog_sample_rate_entry, 1, 2, 1, 1)
    

    def check_numeric_entry(self, entry:Gtk.Entry, block_ids:list[int] = [], allow_comma:bool = False):
        a:str = entry.get_text()
        if not (a.replace(',','') if allow_comma else a).isnumeric() or a.count(',') > 1:
            entry.handler_block_by_func(self.check_numeric_entry)
            for id in block_ids:
                entry.handler_block(id)
            entry.set_text(entry.get_text()[:-1])
            for id in block_ids:
                entry.handler_unblock(id)
            entry.handler_unblock_by_func(self.check_numeric_entry)
            return False
        return True

    def set_variable(self, obj:Gtk.Widget, get_value:Callable[[], str]):
        if obj.get_name() in self.set_variables:
            self.set_variables[obj.get_name()](get_value())
        else:
            print(f"Variável {obj.get_name()} não encontrada. Valor: {get_value()}")