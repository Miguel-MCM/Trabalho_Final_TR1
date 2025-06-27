import numpy as np
from .error_detector import ErrorDetector

class ParityErrorDetector(ErrorDetector):
    """
    Implements a simple parity error detection mechanism.
    This class extends the ErrorDetector abstract base class and uses 
    XOR-based parity checking to detect single-bit errors.
    """
    def __init__(self, to_byte = False) -> None:
        """
        Initialize the parity detector.
        
        Parameters:
        to_byte (bool): If True, the parity trailer will be 8 bits (a full byte).
                        If False, the trailer will be a single bit.
        """
        super().__init__()
        self.to_byte = to_byte
        self.trailer_size = 8 if to_byte else 1

    def add_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Add a parity bit to the end of the data.
        The parity bit is the XOR of all bits in the data.
        
        Parameters:
        data (np.ndarray): Input data as a binary array.
        
        Returns:
        np.ndarray: New array with the parity bit appended.
        """
        data_with_detection = data.copy()
        if self.to_byte:
            data_with_detection.resize(data.size + 8)
        else:
            data_with_detection.resize(data.size + 1)

        data_with_detection[data.size] = np.logical_xor.reduce(data)
        return data_with_detection

    def check(self, data: np.ndarray) -> str:
        """
        Check if the parity of the data is correct.
        
        Parameters:
        data (np.ndarray): Data array with a parity bit at the end.
        
        Returns:
        str: "" if no error detected, error message otherwise
        """
        if data.size < 1:
            raise ValueError("No data given.")
        
        calculated = np.logical_xor.reduce(data)
        if calculated:
            return f"Calculated parity bit is incorrect: {calculated} != 0"
        return ""

    def remove_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Remove the parity bit from the data.
        
        Parameters:
        data (np.ndarray): Data array with a parity bit at the end.
        
        Returns:
        np.ndarray: Data array without the parity bit.
        """
        if self.to_byte:
            if data.size < 8:
                raise ValueError("No data given.")
            return data[:-8]
        else:
            if data.size < 1:
                raise ValueError("No data given.")
            return data[:-1]
