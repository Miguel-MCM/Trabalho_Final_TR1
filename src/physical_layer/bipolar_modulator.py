import numpy as np
from .digital_modulator import DigitalModulator

class BipolarModulator(DigitalModulator):
    """Bipolar Modulator."""
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modulate a sequence of bits into a Bipolar signal.
        
        Parameters:
        bits (np.ndarray): Array of bits to modulate.
        
        Returns:
        np.ndarray: Bipolar modulated signal.
        """
        bipolar_signal = np.array([])
        inverted = False
        for bit in bits:
            if bit == 1:
                bipolar_signal = np.append(bipolar_signal, 1 if not inverted else -1)
                inverted = not inverted
            else:
                bipolar_signal = np.append(bipolar_signal, 0)

        return np.repeat(bipolar_signal, self.samples_per_bit).astype(np.float32)

    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Demodulate a Bipolar signal back into a sequence of bits.
        Uses energy-based detection by calculating the energy of each bit period.
        
        Parameters:
        signal (np.ndarray): Bipolar signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        num_bits = len(signal) // self.samples_per_bit
        demodulated_bits = np.zeros(num_bits, dtype=int)
        
        for i in range(num_bits):
            start_idx = i * self.samples_per_bit
            end_idx = start_idx + self.samples_per_bit
            bit_period = signal[start_idx:end_idx]
            
            # Calculate energy of the bit period
            energy = np.sum(bit_period ** 2)
            
            # For bipolar encoding:
            # - Bit '0' has zero amplitude (energy ≈ 0)
            # - Bit '1' has non-zero amplitude (energy > 0)
            # Use energy threshold to distinguish between 0 and 1
            threshold = 0.5 * self.samples_per_bit  # Energy threshold
            demodulated_bits[i] = 1 if energy > threshold else 0
            
        return demodulated_bits