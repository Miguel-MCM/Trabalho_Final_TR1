from .digital_modulator import DigitalModulator
import numpy as np

class NRZModulator(DigitalModulator):
    """Polar Non-Return-to-Zero (NRZ) Modulator."""
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modulate a sequence of bits into a Polar Non-Return-to-Zero (NRZ) signal.
        
        Parameters:
        bits (np.ndarray): Array of bits to modulate.
        
        Returns:
        np.ndarray: Polar NRZ modulated signal.
        """
        bits = np.where(bits == 0, -1, 1)
        signal = np.repeat(bits, self.samples_per_bit)
        return signal.astype(np.float32)

    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Demodulate a Polar Non-Return-to-Zero (NRZ) signal back into a sequence of bits.
        Uses energy-based detection by calculating the energy of each bit period.
        
        Parameters:
        signal (np.ndarray): NRZ signal to demodulate.
        
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
            
            # For NRZ, positive energy indicates bit '1', negative energy indicates bit '0'
            # Since we map 0->-1 and 1->1, we can use the sign of the average value
            avg_value = np.mean(bit_period)
            demodulated_bits[i] = 1 if avg_value > 0 else 0
            
        return demodulated_bits