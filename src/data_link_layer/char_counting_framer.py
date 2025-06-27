from .framer import Framer
import numpy as np

class CharCountingFramer(Framer):
    """Character Counting Framer for encapsulating data into frames with character count."""

    def __init__(self, counter_size: int = 1):
        """
        Initialize the CharCountingFramer with a specified counter size.
        
        Parameters:
        counter_size (int): Size of the character count field in bytes.
        """
        if counter_size <= 0:
            raise ValueError("Counter size must be a positive integer.")
        self.counter_size = counter_size

    def frame_data(self, data: np.ndarray) -> np.ndarray:
        """
        Frame the input data into frames with character count.
        
        Parameters:
        data (np.ndarray): Input bits to be framed.
        
        Returns:
        np.ndarray: Framed data.
        """
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        
        # Convert data to bits
        bytes = self.bits_to_uint8(data)
        
        # Create frame with character count
        frame = np.concatenate(([len(bytes)], bytes))
        
        return self.uint8_to_bits(frame)

    def deframe_data(self, framed_data: np.ndarray) -> np.ndarray:
        """
        Deframe the input framed data back into a single array.
        
        Parameters:
        framed_data (np.ndarray): Framed data to be deframed.
        
        Returns:
        np.ndarray: Deframed data.
        """
        if not isinstance(framed_data, np.ndarray):
            raise ValueError("Framed data must be a numpy array.")
        
        bytes = self.bits_to_uint8(framed_data)
        # Extract character count and bits
        char_count = bytes[0]
        deframed = bytes[1:1 + char_count]
        
        return self.uint8_to_bits(deframed)