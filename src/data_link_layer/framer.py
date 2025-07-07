from abc import ABC, abstractmethod
import numpy as np
from .error_detector import ErrorDetector

class Framer:
    """Abstract base class for data framers.
    This class defines the interface for framing tecniques.
    It includes methods for framing and deframing bit sequences."""
    def __init__(self, error_detector:ErrorDetector|None = None):
        """
        Initialize the framer with an optional error detector.
        
        Parameters:
        error_detector (ErrorDetector | None): An optional error detector instance
                                               used to add/check trailers during
                                               framing and deframing.
        """
        self.error_detector = error_detector

    def add_edc(self, data: np.ndarray) -> np.ndarray:
        """
        Add error detection code to the data.
        """
        if self.error_detector is not None:
            return self.error_detector.add_trailer(data)
        return data

    def check_edc(self, data: np.ndarray) -> str:
        """
        Check if the data has an error detection code.
        """
        if self.error_detector is not None:
            return self.error_detector.check(data)
        return ""

    def remove_edc(self, data: np.ndarray) -> np.ndarray:
        """
        Remove error detection code from the data.
        """
        if self.error_detector is not None:
            return self.error_detector.remove_trailer(data)
        return data

    @abstractmethod
    def frame_data(self, data: np.ndarray) -> np.ndarray:
        """
        Frame the input data into frames.
        
        Parameters:
        data (np.ndarray): Input data to be framed.
        
        Returns:
        np.ndarray: Framed data.
        """
        pass

    @abstractmethod
    def deframe_data(self, framed_data: np.ndarray) -> np.ndarray:
        """
        Deframe the input framed data back into a single array.
        
        Parameters:
        framed_data (np.ndarray): Framed data to be deframed.
        
        Returns:
        np.ndarray: Deframed data.
        """
        pass
    
    @staticmethod
    def uint8_to_bits(data: np.ndarray) -> np.ndarray:
        """
        Convert an array of uint8 values to a bit sequence.
        
        Parameters:
        data (np.ndarray): Array of uint8 values.
        
        Returns:
        np.ndarray: Bit sequence.
        """
        return np.unpackbits(data.astype(np.uint8))
    
    @staticmethod
    def bits_to_uint8(bits: np.ndarray) -> np.ndarray:
        """
        Convert a bit sequence to an array of uint8 values.
        
        Parameters:
        bits (np.ndarray): Bit sequence.
        
        Returns:
        np.ndarray: Array of uint8 values.
        """
        if len(bits) % 8 != 0:
            raise ValueError("Bit sequence length must be a multiple of 8.")
        return np.packbits(bits.reshape(-1, 8)).astype(np.uint8)