from abc import ABC, abstractmethod
import numpy as np

class Framer:
    """Framer for encapsulating data into frames."""

    @abstractmethod
    def frame_data(self, data: np.ndarray) -> np.ndarray:
        """
        Frame the input data into fixed-size frames.
        
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