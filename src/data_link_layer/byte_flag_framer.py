import numpy as np
from .framer import Framer, ErrorDetector

class ByteFlagFramer(Framer):
    """Byte Flag Framer for encapsulating data into frames with byte flagging."""

    def __init__(self, flag_byte: int = 0x7E, escape_byte: int = 0x7D,  error_detector:ErrorDetector|None = None):
        """
        Initialize the ByteFlagFramer with a specified flag byte.
        
        Parameters:
        flag_byte (int): Byte used as a flag to indicate frame boundaries.
        escape_byte (int): Byte used as escape flag to indicate that the next byte of data is not a flag
        """
        if not (0 <= flag_byte <= 255 ):
            raise ValueError("Flag byte must be between 0 and 255.")
        
        if not (0 <= escape_byte <= 255 ):
            raise ValueError("Escape byte must be between 0 and 255.")
                
        if error_detector is not None and error_detector.trailer_size % 8 != 0:
            raise ValueError("Error detector trailer size must be a multiple of 8.") 
        
        super().__init__(error_detector)
        self.flag_byte = flag_byte
        self.flag_bits = self.uint8_to_bits(np.array([flag_byte]))
        self.escape_byte = escape_byte

    def frame_data(self, data: np.ndarray) -> np.ndarray:
        """
        Frame the input data into frames with byte flags.
        
        Parameters:
        data (np.ndarray): Input bits to be framed.
        
        Returns:
        np.ndarray: Framed data.
        """
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        
        bytes_data = self.bits_to_uint8(data)
        
        if self.error_detector is not None:
            bits_data = self.uint8_to_bits(bytes_data)
            bits_data = self.error_detector.add_trailer(bits_data)
            bytes_data = self.bits_to_uint8(bits_data)

        bytes_data = np.insert(bytes_data, np.nonzero(bytes_data == self.escape_byte)[0], self.escape_byte)
        bytes_data = np.insert(bytes_data, np.nonzero(bytes_data == self.flag_byte)[0], self.escape_byte)


        # Add flag bytes at the start and end
        framed_data = np.concatenate(([self.flag_byte], bytes_data, [self.flag_byte]))

        return self.uint8_to_bits(framed_data)

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
        
        bytes_data = self.bits_to_uint8(framed_data)
        
        # Remove flag bytes
        if bytes_data.size < 2:
            raise ValueError("Invalid frame: too small.")
        
        #bytes_data = bytes_data[1:-1]  # Exclude the flag bytes

        # Remove escape bytes that follow escape or flag bytes
        deframed = np.zeros(bytes_data.size - 2)

        initialized = False
        finished = False
        was_escape = False
        counter = 0
        for i, byte in enumerate(bytes_data):
            if not initialized:
                if byte == self.flag_byte:
                    initialized = True
                continue
            if not was_escape:
                if byte == self.escape_byte:
                    was_escape = True
                    continue
                if byte == self.flag_byte:
                    finished = True
                    deframed = deframed[:counter]
                    break
            deframed[counter] = byte
            counter += 1
            was_escape = False
        
        if not finished or not initialized:
            raise ValueError("Framed data does not include flags.")
        
        deframed_bits = self.uint8_to_bits(deframed)
        if self.error_detector is not None:
            if  (error := self.error_detector.check(deframed_bits)):
                raise ValueError(error)
            deframed_bits = self.error_detector.remove_trailer(deframed_bits)

        return deframed_bits