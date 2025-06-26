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
        
        Parameters:
        signal (np.ndarray): Manchester signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        bits = signal[self.samples_per_bit//4::self.samples_per_bit]
        return np.where( bits - 0.5 < 0, 0, 1 ) .astype(int)
        