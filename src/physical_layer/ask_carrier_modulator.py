from .carrier_modulator import CarrierModulator
import numpy as np

class ASKCarrierModulator(CarrierModulator):
  """Carrier modulator for Amplitude Shift Keying (ASK).
  This class implements the ASK modulation scheme.
  """
  def __init__(self, carrier_frequency: float, signals: np.ndarray = np.array([0, 1])):
    # Mapeamento de possíveis finais: cada sinal é mapeado para uma amplitude específica
    self.amplitude_signals = np.arange(len(signals))/len(signals)
    super().__init__(carrier_frequency, signals)

  def modulate(self, signal: np.ndarray, time: np.ndarray) -> np.ndarray:
    """
    Modulate a signal using the ASK modulation scheme.
    Usa o mapeamento de possíveis finais para converter os sinais em amplitudes.
    """
    # Para cada valor no sinal, encontra o índice mais próximo nos sinais possíveis
    modulated_signal = np.zeros_like(signal)
    
    for i, sig_val in enumerate(signal):
      # Encontra o índice do sinal mais próximo
      distances = np.abs(self.signals - sig_val)
      closest_idx = np.argmin(distances)
      # Mapeia para a amplitude correspondente
      amplitude = self.amplitude_signals[closest_idx]
      modulated_signal[i] = amplitude
    
    # Aplica a modulação ASK: amplitude * sin(2π * fc * t)
    return modulated_signal * np.sin(2 * np.pi * self.carrier_frequency * time)

  def demodulate(self, signal: np.ndarray, time: np.ndarray, kernel_size: int = 10) -> np.ndarray:
    """
    Demodulate a signal using the ASK modulation scheme.
    Envelope detection com mapeamento reverso para os sinais originais.
    """
    # Detecção de envelope: divide pelo sinal portador
    wave_signal = np.sin(2 * np.pi * self.carrier_frequency * time)
    
    # Evita divisão por zero
    wave_signal = np.where(np.abs(wave_signal) < 1e-10, 
                          np.sign(wave_signal) * 1e-10, wave_signal)
    
    # Demodulação por divisão
    demodulated = signal / wave_signal
    
    # Aplica filtro de média móvel para suavizar
    kernel = np.ones(kernel_size) / kernel_size
    demodulated = np.convolve(demodulated, kernel, mode='same')
    
    # Mapeamento reverso: converte amplitudes de volta para os sinais originais
    final_signal = np.zeros_like(demodulated)
    
    for i, amp_val in enumerate(demodulated):
      # Encontra a amplitude mais próxima
      distances = np.abs(self.amplitude_signals - amp_val)
      closest_idx = np.argmin(distances)
      # Mapeia de volta para o sinal original
      final_signal[i] = self.signals[closest_idx]
    
    return final_signal
