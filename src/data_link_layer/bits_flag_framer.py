import numpy as np
from .framer import Framer

class BitsFlagFramer(Framer):
    """Bits Flag Framer for encapsulating data into frames with bits flag."""

    def __init__(self, flag_bits: np.ndarray = np.array([0, 1, 1, 1, 1, 1, 1, 0])):
        """
        Initialize the BitsFlagFramer with a specified flag bit.
        
        Parameters:
        flag_bit (int): Bit used as a flag to indicate frame boundaries.
        """
        if not isinstance(flag_bits, np.ndarray):
            raise ValueError("Flag bits must be a np.ndarray.")
        
        self.flag_bits = flag_bits.copy()

    def frame_data(self, data: np.ndarray) -> np.ndarray:
        """
        Frame the input data into frames with bits flags.
        
        Parameters:
        data (np.ndarray): Input bits to be framed.
        
        Returns:
        np.ndarray: Framed data.
        """
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        
        if data.shape[0] > len(self.flag_bits) - 1:
            # Add the inverse of the last flag bit where data matches the flag bits
            windows = np.lib.stride_tricks.sliding_window_view(data, window_shape=len(self.flag_bits)-1)
            matches = np.all(windows == self.flag_bits[:-1], axis=1)
            indices = np.nonzero(matches)[0] + len(self.flag_bits)
            data = np.insert(data, indices, (not self.flag_bits[-1]))

        framed_data = np.concatenate((self.flag_bits, data, self.flag_bits))
        
        return framed_data

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
        
        # Remove the first and last flag bits
        if len(framed_data) < 2 or not np.all(framed_data[:len(self.flag_bits)] == self.flag_bits) or not np.all(framed_data[-len(self.flag_bits):] == self.flag_bits):
            raise ValueError("Invalid framed data format.")
        
        deframed_data = framed_data[len(self.flag_bits):-len(self.flag_bits)]

        if deframed_data.shape[0] > len(self.flag_bits) - 1:
            # Add the inverse of the last flag bit where data matches the flag bits
            windows = np.lib.stride_tricks.sliding_window_view(deframed_data, window_shape=len(self.flag_bits)-1)
            matches = np.all(windows == self.flag_bits[:-1], axis=1)
            indices = np.nonzero(matches)[0] + len(self.flag_bits)
            deframed_data = np.delete(deframed_data, indices)
        
        return deframed_data