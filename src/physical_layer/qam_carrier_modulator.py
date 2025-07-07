from .carrier_modulator import CarrierModulator
import numpy as np

class QAMCarrierModulator(CarrierModulator):
  """
  Carrier modulator for 8-Quadrature Amplitude Modulation (8-QAM).
  This class implements the 8-QAM modulation scheme.
  """
  
  # 8-QAM constellation mapping: (amplitude, phase) for each 3-bit symbol
  # Format: '000': (amplitude, phase_radians)
  QAM_CONSTELLATION = {
    '000': (1.0, 0),           # 0°
    '001': (1.0, np.pi/4),     # 45°
    '010': (1.0, np.pi/2),     # 90°
    '011': (1.0, 3*np.pi/4),  # 135°
    '100': (1.0, np.pi),       # 180°
    '101': (1.0, 5*np.pi/4),  # 225°
    '110': (1.0, 3*np.pi/2),  # 270°
    '111': (1.0, 7*np.pi/4),  # 315°
  }
  
  def __init__(self, carrier_frequency: float, bit_rate: float, sample_rate: float):
    super().__init__(carrier_frequency, bit_rate, sample_rate)
    # Create reverse mapping for demodulation
    self.symbol_to_bits = {v: k for k, v in self.QAM_CONSTELLATION.items()}

  def modulate(self, bits: np.ndarray) -> np.ndarray:
    """
    Modulate bits using 8-QAM modulation.
    
    Parameters:
    bits (np.ndarray): Array of bits (0s and 1s)
    
    Returns:
    np.ndarray: Modulated signal
    """
    # Ensure number of bits is multiple of 3 for 8-QAM
    if len(bits) % 3 != 0:
      # Pad with zeros if necessary
      padding_length = 3 - (len(bits) % 3)
      bits = np.append(bits, np.zeros(padding_length))
    
    # Group bits into 3-bit symbols
    num_symbols = len(bits) // 3
    symbols = []
    
    for i in range(num_symbols):
      # Extract 3 bits and convert to string
      symbol_bits = bits[i*3:(i+1)*3]
      symbol_key = ''.join(map(str, symbol_bits.astype(int)))
      
      # Get constellation point
      amplitude, phase = self.QAM_CONSTELLATION[symbol_key]
      
      # Generate carrier signal for this symbol
      symbol_duration = 3 * self.samples_per_bit  # 3 bits per symbol
      t = np.arange(symbol_duration) / self.sample_rate
      
      # Create modulated signal: amplitude * cos(2π*fc*t + phase)
      symbol_signal = amplitude * np.cos(2 * np.pi * self.carrier_frequency * t + phase)
      symbols.append(symbol_signal)
    
    # Concatenate all symbol signals
    modulated_signal = np.concatenate(symbols)
    return modulated_signal

  def demodulate(self, signal: np.ndarray) -> np.ndarray:
    """
    Demodulate 8-QAM signal back to bits.
    
    Parameters:
    signal (np.ndarray): Modulated signal
    
    Returns:
    np.ndarray: Demodulated bits
    """
    symbol_duration = 3 * self.samples_per_bit
    num_symbols = len(signal) // symbol_duration
    
    demodulated_bits = []
    
    for i in range(num_symbols):
      # Extract symbol signal
      start_idx = i * symbol_duration
      end_idx = start_idx + symbol_duration
      symbol_signal = signal[start_idx:end_idx]
      
      # Generate time array for this symbol
      t = np.arange(symbol_duration) / self.sample_rate
      
      # Try to detect the phase by correlating with different phase references
      max_correlation = -float('inf')
      best_symbol = None
      
      for symbol_key, (ref_amplitude, ref_phase) in self.QAM_CONSTELLATION.items():
        # Create reference signal with this phase
        ref_signal = ref_amplitude * np.cos(2 * np.pi * self.carrier_frequency * t + ref_phase)
        
        # Correlate with received signal
        correlation = np.sum(symbol_signal * ref_signal)
        
        if correlation > max_correlation:
          max_correlation = correlation
          best_symbol = symbol_key
      
      # Convert symbol back to bits
      if best_symbol is not None:
        symbol_bits = np.array([int(bit) for bit in best_symbol])
        demodulated_bits.extend(symbol_bits)
      else:
        # Fallback: assume all zeros if no valid symbol found
        demodulated_bits.extend([0, 0, 0])
    
    return np.array(demodulated_bits)
