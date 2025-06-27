import numpy as np
from abc import ABC, abstractmethod

class DigitalModulator:
    """Abstract base class for digital modulators.
    This class defines the interface for digital modulation schemes.
    It includes methods for modulation and demodulation of bit sequences.
    """
    def __init__(self, bit_rate:float=1e6, sample_rate:float=10e6):
        self.bit_rate = bit_rate
        self.sample_rate = sample_rate
        self.samples_per_bit = int(self.sample_rate / self.bit_rate)

    @abstractmethod
    def modulate(self, bits: np.ndarray) -> np.ndarray:
        """
        Modulate a sequence of bits into a signal.
        
        Parameters:
        bits (np.ndarray): Array of bits to modulate.
        
        Returns:
        np.ndarray: Modulated signal.
        """
        pass

    @abstractmethod
    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """
        Demodulate a signal back into a sequence of bits.
        
        Parameters:
        signal (np.ndarray): Signal to demodulate.
        
        Returns:
        np.ndarray: Demodulated bits.
        """
        pass

