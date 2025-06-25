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
        return signal

    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Demodulate a Polar Non-Return-to-Zero (NRZ) signal back into a sequence of bits.
        
        Parameters:
        signal (np.ndarray): NRZ signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        bits = signal[::self.samples_per_bit]
        return (bits > 0).astype(int)  # Convert to binary representation