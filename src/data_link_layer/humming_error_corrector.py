import numpy as np

class HummingErrorCorrector:

    def add_error_detection(self, bits: np.ndarray) -> np.ndarray:
        """
        Add Hamming error detection bits to the input data.
        
        Args:
            bits: Input data bits as numpy array
            
        Returns:
            numpy array with original data + parity bits
        """
        # Calculate number of parity bits needed
        m = len(bits)
        r = 0
        while 2**r < m + r + 1:
            r += 1
        
        # Create result array with space for parity bits
        n = m + r
        result = np.zeros(n, dtype=int)
        
        # Fill data bits (skip positions that are powers of 2)
        data_idx = 0
        for i in range(n):
            if not self._is_power_of_2(i + 1) and data_idx < m:
                result[i] = bits[data_idx]
                data_idx += 1
        
        # Calculate and set parity bits
        for i in range(r):
            parity_pos = 2**i - 1
            result[parity_pos] = self._calculate_parity(result, i)
        
        return result.astype(int)
    
    def remove_error_detection(self, bits: np.ndarray) -> np.ndarray:
        """
        Remove Hamming parity bits and return original data.
        
        Args:
            bits: Data with parity bits as numpy array
            
        Returns:
            numpy array with original data (parity bits removed)
        """
        # Find positions that are not powers of 2 (data bits)
        data_bits = []
        for i in range(len(bits)):
            if not self._is_power_of_2(i + 1):
                data_bits.append(bits[i])
        
        return np.array(data_bits, dtype=int)
    
    def correct_errors(self, bits: np.ndarray) -> np.ndarray:
        """
        Detect and correct single-bit errors using Hamming code.
        
        Args:
            bits: Data with parity bits as numpy array
            
        Returns:
            numpy array with corrected data
        """
        # Calculate syndrome
        syndrome = self._calculate_syndrome(bits)
        
        # If syndrome is zero, no errors
        if syndrome == 0:
            return bits
        
        # Correct single-bit error
        error_pos = syndrome - 1
        if 0 <= error_pos < len(bits):
            bits[error_pos] = 1 - bits[error_pos]  # Flip the bit
        
        return bits
    
    def check_errors(self, bits: np.ndarray) -> bool:
        """
        Check if there are errors in the data.
        
        Args:
            bits: Data with parity bits as numpy array
            
        Returns:
            True if errors detected, False otherwise
        """
        syndrome = self._calculate_syndrome(bits)
        return syndrome != 0
    
    def _is_power_of_2(self, n: int) -> bool:
        """Check if n is a power of 2."""
        return n > 0 and (n & (n - 1)) == 0
    
    def _calculate_parity(self, bits: np.ndarray, parity_index: int) -> int:
        """Calculate parity bit for given position."""
        parity_pos = 2**parity_index - 1
        parity = 0
        
        for i in range(len(bits)):
            if i != parity_pos and (i + 1) & (2**parity_index):
                parity ^= bits[i]
        
        return parity
    
    def _calculate_syndrome(self, bits: np.ndarray) -> int:
        """Calculate syndrome to detect errors."""
        syndrome = 0
        r = 0
        
        # Find number of parity bits
        while 2**r < len(bits) + 1:
            r += 1
        
        # Calculate syndrome
        for i in range(r):
            parity_pos = 2**i - 1
            if parity_pos < len(bits):
                expected_parity = self._calculate_parity(bits, i)
                if bits[parity_pos] != expected_parity:
                    syndrome += 2**i
        
        return syndrome