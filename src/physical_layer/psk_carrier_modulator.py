from .carrier_modulator import CarrierModulator
import numpy as np

class PSKCarrierModulator(CarrierModulator):
  """Carrier modulator for Phase Shift Keying (PSK).
  This class implements the PSK modulation scheme.
  """
  def __init__(self, carrier_frequency: float, bit_rate: float, sample_rate: float):
    super().__init__(carrier_frequency, bit_rate, sample_rate)

  def modulate(self, bits: np.ndarray) -> np.ndarray:
    """
    Modulate a signal using the PSK modulation scheme.
    Maps bits to different phases of the carrier signal.
    """
    expanded = np.repeat(bits, self.samples_per_bit)
    
    # Create time array for the signal
    time = np.linspace(0, bits.size / self.bit_rate, expanded.size, endpoint=False)
    
    # Map bits to phases: 0 -> 0°, 1 -> 180°
    phases = np.where(expanded == 1, np.pi, 0)
    
    return np.sin(2 * np.pi * self.carrier_frequency * time + phases)

  def demodulate(self, signal: np.ndarray) -> np.ndarray:
    """
    Demodulate a PSK signal by correlating with reference signals at different phases.
    
    Parameters:
    signal (np.ndarray): Received PSK signal to demodulate.
    
    Returns:
    np.ndarray: Demodulated bits (0s and 1s).
    """
    # Calculate the number of bits based on signal length and samples per bit
    num_bits = len(signal) // self.samples_per_bit
    
    # Create time array for the signal
    t = np.arange(len(signal)) / self.sample_rate
    
    # Create reference signals for both phases
    ref_signal_0 = np.sin(2 * np.pi * self.carrier_frequency * t)  # 0° phase
    ref_signal_1 = np.sin(2 * np.pi * self.carrier_frequency * t + np.pi)  # 180° phase
    
    # Initialize output bits array
    bits = np.zeros(num_bits, dtype=int)
    
    # Demodulate each bit by correlating with reference signals
    for i in range(num_bits):
        start_idx = i * self.samples_per_bit
        end_idx = start_idx + self.samples_per_bit
        
        # Extract the signal segment for this bit
        signal_segment = signal[start_idx:end_idx]
        ref_0_segment = ref_signal_0[start_idx:end_idx]
        ref_1_segment = ref_signal_1[start_idx:end_idx]
        
        # Calculate correlation with both reference signals
        corr_0 = np.corrcoef(signal_segment, ref_0_segment)[0, 1]
        corr_1 = np.corrcoef(signal_segment, ref_1_segment)[0, 1]
        
        # Determine which phase was more likely transmitted
        # Higher correlation indicates the transmitted phase
        bits[i] = 1 if corr_1 > corr_0 else 0
    
    return bits 