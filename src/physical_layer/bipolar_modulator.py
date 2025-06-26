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
        
        Parameters:
        signal (np.ndarray): Bipolar signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        bits = signal[self.samples_per_bit//2::self.samples_per_bit]
        return np.where( np.abs(bits) < 0.5, 0, 1 ).astype(int)