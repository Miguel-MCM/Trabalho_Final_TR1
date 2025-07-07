import numpy as np
from .digital_modulator import DigitalModulator

class ManchesterModulator(DigitalModulator):
    """Manchester Modulator."""
    
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modulate a sequence of bits into a Manchester signal.
        
        Parameters:
        bits (np.ndarray): Array of bits to modulate.
        
        Returns:
        np.ndarray: Manchester modulated signal.
        """
        manchester_signal = np.array([])
        for bit in bits:
            if bit == 0:
                manchester_signal = np.append(manchester_signal, [0, 1])
            else:
                manchester_signal = np.append(manchester_signal, [1, 0])
        
        return np.repeat(manchester_signal, self.samples_per_bit//2).astype(np.float32)
    
    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Demodulate a Manchester signal back into a sequence of bits.
        Uses energy-based detection by calculating the energy of each half-bit period.
        
        Parameters:
        signal (np.ndarray): Manchester signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        num_bits = len(signal) // self.samples_per_bit
        demodulated_bits = np.zeros(num_bits, dtype=int)
        
        for i in range(num_bits):
            start_idx = i * self.samples_per_bit
            end_idx = start_idx + self.samples_per_bit
            bit_period = signal[start_idx:end_idx]
            
            # Split the bit period into two halves
            half_period = self.samples_per_bit // 2
            first_half = bit_period[:half_period]
            second_half = bit_period[half_period:]
            
            # Calculate energy of each half
            energy_first = np.sum(first_half ** 2)
            energy_second = np.sum(second_half ** 2)
            
            # For Manchester encoding:
            # - Bit '0': low-high (0->1) pattern
            # - Bit '1': high-low (1->0) pattern
            # Compare energy of first half vs second half
            demodulated_bits[i] = 1 if energy_first > energy_second else 0
            
        return demodulated_bits
        