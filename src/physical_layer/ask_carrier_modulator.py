from .carrier_modulator import CarrierModulator
import numpy as np

class ASKCarrierModulator(CarrierModulator):
  """Carrier modulator for Amplitude Shift Keying (ASK).
  This class implements the ASK modulation scheme.
  """
  def __init__(self, carrier_frequency: float, bit_rate: float, sample_rate: float):
    super().__init__(carrier_frequency, bit_rate, sample_rate)

  def modulate(self, bits: np.ndarray) -> np.ndarray:
    """
    Modulate a signal using the ASK modulation scheme.
    Usa o mapeamento de possíveis finais para converter os sinais em amplitudes.
    """
    expanded = np.repeat(bits, self.samples_per_bit)
    return expanded * np.sin(2 * np.pi * self.carrier_frequency * np.linspace(0, bits.size * self.sample_rate, expanded.size))

  def demodulate(self, signal: np.ndarray) -> np.ndarray:
    """
    Demodulate a signal using the ASK modulation scheme.
    Envelope detection com mapeamento reverso para os sinais originais.
    """
    # Calcula a energia do sinal em janelas do tamanho de um bit
    energy = np.zeros(len(signal) // self.samples_per_bit)
    
    for i in range(len(energy)):
        start_idx = i * self.samples_per_bit
        end_idx = start_idx + self.samples_per_bit
        
        if end_idx <= len(signal):
            # Calcula a energia da janela atual
            window_energy = np.sum(signal[start_idx:end_idx] ** 2)
            energy[i] = window_energy
    
    # Normaliza a energia e mapeia para bits (0 ou 1)
    # Usa um limiar baseado na média da energia
    threshold = np.mean(energy)
    demodulated_bits = (energy > threshold).astype(int)
    print(demodulated_bits)
    return demodulated_bits
