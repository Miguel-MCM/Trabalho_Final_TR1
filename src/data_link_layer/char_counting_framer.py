from .framer import Framer, ErrorDetector
import numpy as np

class CharCountingFramer(Framer):
    """Character Counting Framer for encapsulating data into frames with character count."""

    def __init__(self, counter_size: int = 1, error_detector:ErrorDetector|None = None):
        """
        Initialize the CharCountingFramer with a specified counter size.
        
        Parameters:
        counter_size (int): Size of the character count field in bytes.
        error_detector (ErrorDetector | None): An optional error detector instance
                                               used to add/check trailers during
                                               framing and deframing.
        """

        if error_detector is not None and error_detector.trailer_size % 8 != 0:
            raise ValueError("Error detector trailer size must be a multiple of 8.") 

        super().__init__(error_detector)
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
        
        if self.error_detector is not None:
            bits = self.uint8_to_bits(bytes)
            bits = self.error_detector.add_trailer(bits)
            bytes = self.bits_to_uint8(bits)

        # Create frame with character count
        frame = np.concatenate(([bytes.size], bytes))
        
        
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
        if char_count > bytes.size - 1:
            bytes.resize(char_count+1)
        deframed = bytes[1:1 + char_count]

        deframed_bits = self.uint8_to_bits(deframed)

        return deframed_bits