from physical_layer import BipolarModulator, ManchesterModulator, NRZModulator, ASKCarrierModulator, FSKCarrierModulator, PSKCarrierModulator, QAMCarrierModulator
from data_link_layer import ByteFlagFramer, BitsFlagFramer, CharCountingFramer, ParityErrorDetector, CRCErrorDetector, HummingErrorCorrector
from communication import CommunicationChannel

class BaseWindow:
    def __init__(self):
        self.input_text = ""

        self.coding = None
        self.error_detector = None
        self.error_corrector = None
        self.modulator = NRZModulator(bit_rate=1000, sample_rate=10000)
        self.carrier_modulator = None
        self.use_carrier_modulation = False

        # Inicializar configurações
        self._init_configurations()

        self.communication = CommunicationChannel(snr=self.snr)

        # Criar funções de configuração
        self._create_set_functions()
        self._create_update_functions()
        
        # Configurar objetos baseados nas configurações
        self._setup_objects()

    def _init_configurations(self):
        """Inicializa todas as configurações padrão"""
        
        self.snr = 10

        # Configurações de enquadramento
        self.coding_index = 0
        self.coding_options = [None, CharCountingFramer, ByteFlagFramer, BitsFlagFramer]
        self.coding_options_names = ["Nenhum", "Contagem de Caracteres", "Byte Flag", "Bits Flag"]
        self.max_frame_size = 10
        
        # Configurações de detecção de erro
        self.error_detection_index = 0
        self.error_detection_options = [None, ParityErrorDetector, CRCErrorDetector]
        self.error_detection_options_names = ["Nenhum", "Paridade", "CRC"]
        
        # Configurações de correção de erro
        self.error_correction_index = 0
        self.error_correction_options = [None, HummingErrorCorrector]
        self.error_correction_options_names = ["Nenhum", "Hamming"]
        
        # Configurações de modulação
        self.modulation_index = 0
        self.modulation_options = [NRZModulator, BipolarModulator, ManchesterModulator]
        self.modulation_options_names = ["NRZ", "Bipolar", "Manchester"]
        self.bit_rate = 1000
        self.sample_rate = 10000
        
        # Configurações de modulação analógica
        self.analog_modulation_index = 0
        self.analog_modulation_options = [ASKCarrierModulator, FSKCarrierModulator, PSKCarrierModulator, QAMCarrierModulator]
        self.analog_modulation_options_names = ["ASK", "FSK", "PSK", "8-QAM"]
        self.analog_frequency = 1000
        self.analog_sample_rate = 1000000

    def _create_set_functions(self):
        """Cria as funções set para atualizar configurações"""
        def set_input_text(x: str):
            self.input_text = x

        def set_max_frame_size(x: str):
            self.max_frame_size = int(x)
            self._update_coding()
        
        def set_coding(x: int):
            self.coding_index = x
            self._update_coding()
        
        def set_error_detection(x: int):
            self.error_detection_index = x
            self._update_error_detection()
        
        def set_error_correction(x: int):
            self.error_correction_index = x
            self._update_error_correction()
        
        def set_modulation(x: int):
            self.modulation_index = x
            self._update_modulator()
        
        def set_bit_rate(x: str):
            self.bit_rate = float(x.replace(',', '.'))
            self._update_modulator()
        
        def set_sample_rate(x: str):
            self.sample_rate = float(x.replace(',', '.'))
            self._update_modulator()

        def set_snr(x: str):
            self.snr = float(x.replace(',', '.'))
            self.communication = CommunicationChannel(snr=self.snr)

        def set_use_carrier_modulation(x: bool):
            self.use_carrier_modulation = x
            self._update_carrier_modulator()

        def set_analog_modulation(x: int):
            self.analog_modulation_index = x
            self._update_carrier_modulator()

        def set_analog_frequency(x: str):
            self.analog_frequency = float(x.replace(',', '.'))
            self._update_carrier_modulator()

        def set_analog_sample_rate(x: str):
            self.analog_sample_rate = float(x.replace(',', '.'))
            self._update_carrier_modulator()
        
        # Atribuir as funções como métodos da classe
        self.set_max_frame_size = set_max_frame_size
        self.set_coding = set_coding
        self.set_error_detection = set_error_detection
        self.set_error_correction = set_error_correction
        self.set_modulation = set_modulation
        self.set_bit_rate = set_bit_rate
        self.set_sample_rate = set_sample_rate
        self.set_snr = set_snr
        self.set_input_text = set_input_text
        self.set_use_carrier_modulation = set_use_carrier_modulation
        self.set_analog_modulation = set_analog_modulation
        self.set_analog_frequency = set_analog_frequency
        self.set_analog_sample_rate = set_analog_sample_rate

    def _create_update_functions(self):
        """Cria as funções update para recriar objetos baseados nas configurações"""
        def update_coding():
            if self.coding_options[self.coding_index] is not None:
                if self.error_detection_index == 1 and (self.coding_index in [1, 2]):
                    self.error_detector = self.error_detection_options[self.error_detection_index](to_byte=True)
                self.coding = self.coding_options[self.coding_index](error_detector=self.error_detector)
            else:
                self.coding = None
        
        def update_error_detection():
            if self.error_detection_options[self.error_detection_index] is not None:
                if self.error_detection_index == 1 and (self.coding_index in [1, 2]):
                    self.error_detector = self.error_detection_options[self.error_detection_index](to_byte=True)
                else:
                    self.error_detector = self.error_detection_options[self.error_detection_index]()
            else:
                self.error_detector = None
            self._update_coding()
        
        def update_error_correction():
            if self.error_correction_options[self.error_correction_index] is not None:
                self.error_corrector = self.error_correction_options[self.error_correction_index]()
            else:
                self.error_corrector = None
        
        def update_modulator():
            self.modulator = self.modulation_options[self.modulation_index](
                bit_rate=self.bit_rate, 
                sample_rate=self.sample_rate
            )

        def update_carrier_modulator():
            if self.use_carrier_modulation:
                if self.analog_modulation_index == 1:
                    self.carrier_modulator = self.analog_modulation_options[self.analog_modulation_index](
                        carrier_frequency=self.analog_frequency,
                        bit_rate=self.bit_rate, 
                        sample_rate=self.sample_rate,
                        delta_frequency=self.analog_frequency
                    )
                else:
                    self.carrier_modulator = self.analog_modulation_options[self.analog_modulation_index](
                        carrier_frequency=self.analog_frequency,
                        bit_rate=self.bit_rate,
                        sample_rate=self.analog_sample_rate
                )
            else:
                self.carrier_modulator = None

        
        # Atribuir as funções como métodos da classe
        self._update_coding = update_coding
        self._update_error_detection = update_error_detection
        self._update_error_correction = update_error_correction
        self._update_modulator = update_modulator
        self._update_carrier_modulator = update_carrier_modulator

    def _setup_objects(self):
        """Configura os objetos iniciais baseados nas configurações padrão"""
        # Configurar codificador
        self._update_coding()
        
        # Configurar detector de erro
        self._update_error_detection()
        
        # Configurar corretor de erro
        self._update_error_correction()
        
        # Configurar modulador
        self._update_modulator()

        # Configurar modulador de portadora
        self._update_carrier_modulator()