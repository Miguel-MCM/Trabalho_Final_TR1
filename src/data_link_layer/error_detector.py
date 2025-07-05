from abc import ABC, abstractmethod
import numpy as np

class ErrorDetector:
    """Abstract base class for error detectors.
    This class defines the interface for error detection.
    It includes methods for adding, checking and removing error detection trailers.
    """
    def __init__(self) -> None:
        self.trailer_size:int = 0

    @abstractmethod
    def add_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Add an error detection trailer to the input data.
        
        Parameters:
        data (np.ndarray): Input data to which the error detection trailer will be added.
        
        Returns:
        np.ndarray: Data with the error detection trailer appended.
        """
        pass

    @abstractmethod
    def check(self, data: np.ndarray) -> str:
        """
        Check the data for errors using the trailer.
        
        Parameters:
        data (np.ndarray): Data with an error detection trailer to be checked.
        
        Returns:
        string: "" if no errors else the error message
        """
        pass

    @abstractmethod
    def remove_trailer(self, data: np.ndarray) -> np.ndarray:
        """
        Remove the error detection trailer from the data.
        
        Parameters:
        data (np.ndarray): Data with an error detection trailer.
        
        Returns:
        np.ndarray: Original data with the trailer removed.
        """
        pass
