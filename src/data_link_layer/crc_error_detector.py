import numpy as np
from .error_detector import ErrorDetector

class CRCErrorDetector(ErrorDetector):
    """
    Implements a CRC (Cyclic Redundancy Check) error detection mechanism.
    This class extends the ErrorDetector abstract base class and uses
    a specified generator polynomial to compute and verify CRC trailers.
    """
    def __init__(self, poly:int=0x82608EDB, trailer_size=32) -> None:
        """
        Initialize the CRC detector.
        
        Parameters:
        poly (int):     The generator polynomial, represented as an integer.
                        Default is 0x82608EDB.
        trailer_size (int): The number of bits in the CRC trailer.
                        Default is 32 bits.
        """
        super().__init__()
        self.trailer_size = trailer_size
        self.poly = poly

    def crc(self, data: np.ndarray) -> np.int64:
        """
        Compute the CRC value over the input bitstream.
        
        The algorithm performs a bitwise division by the generator polynomial.
        
        Parameters:
        data (np.ndarray): Bit array (uint8) containing both message and trailer bits.
        
        Returns:
        np.int64: The computed CRC value as a signed 64-bit integer.
        """
        # Initialize CRC from the first trailer_size bits as integer
        crc =  np.int64(
            data[:self.trailer_size]
            .dot(2**np.arange(self.trailer_size, dtype=np.uint64)[::-1])
            )
        # Process the rest of the bits
        for b in data[self.trailer_size:]:
            if crc & (1 << (self.trailer_size-1)):
                crc ^= self.poly
            crc <<= 1
            crc |= b
        # Final reduction step
        if crc & (1 << (self.trailer_size-1)):
            crc ^= self.poly
        return crc

    def add_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Append a CRC trailer to the input data.
        
        Computes the CRC over the message bits and appends the trailer bits
        (derived from the CRC value) to the end of the message.
        
        Parameters:
        data (np.ndarray): Input data as a binary array. Must be at least
                           trailer_size bits long.
        
        Returns:
        np.ndarray: New array containing the original data followed by the
                    CRC trailer bits.
        
        Raises:
        ValueError: If the input data has fewer bits than trailer_size.
        """
        if data.size < self.trailer_size:
            raise ValueError(f"Data must be at least {self.trailer_size} bits long")
        
        bits = np.concatenate((data, np.zeros(self.trailer_size))).astype(np.uint8)
        crc = self.crc(bits)
        bits[-self.trailer_size:] += np.unpackbits(np.array([ b for b in crc.tobytes()[::-1] ], dtype=np.uint8))[-self.trailer_size:]
        return bits
    
    def check(self, data: np.ndarray) -> str:
        """
        Verify the CRC of a received data block.
        
        Recomputes the CRC over the entire block (message + trailer). If the
        result is non-zero, an error is detected.
        
        Parameters:
        data (np.ndarray): Data array with CRC trailer bits at the end.
        
        Returns:
        str: Empty string if no error detected; otherwise, an error message
             containing the computed CRC in binary.
        """
        if data.size < self.trailer_size:
            return f"Data must be at least {self.trailer_size} bits long"
        
        if (crc := self.crc(data)) != 0:
            return f"CRC is not equal zero. CRC: {crc:b}b"
        return ""
    
    def remove_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Remove the CRC trailer bits from the data.
        
        Parameters:
        data (np.ndarray): Data array with CRC trailer bits at the end.
        
        Returns:
        np.ndarray: Original message data without the CRC trailer.
        
        Raises:
        ValueError: If the input data has fewer bits than trailer_size.
        """
        if data.size < self.trailer_size:
            raise ValueError("No data given.")
        return data[:-self.trailer_size]