from abc import ABC, abstractmethod
import numpy as np


class CarrierModulator:
  """Abstract base class for carrier modulators.
  This class defines the interface for carrier modulation schemes.
  It includes methods for modulation and demodulation of signals.
  """
  def __init__(self, carrier_frequency: float, signals: np.ndarray = np.array([0, 1])):
    """
    Initialize the carrier modulator.

    Parameters:
    carrier_frequency (float): Frequency of the carrier signal.
    signals (list[float]): List of signals to use for modulation.
    """
    self.carrier_frequency = carrier_frequency
    self.signals = signals

  @abstractmethod
  def modulate(self, signal: np.ndarray, time: np.ndarray) -> np.ndarray:
    """
    Modulate a signal using the carrier modulation scheme.

    Parameters:
    signal (np.ndarray): Signal to modulate.

    Returns:
    np.ndarray: Modulated signal.
    """
    pass

  @abstractmethod
  def demodulate(self, signal: np.ndarray, time: np.ndarray) -> np.ndarray:
    """
    Demodulate a signal using the carrier modulation scheme.

    Parameters:
    signal (np.ndarray): Signal to demodulate.

    Returns:
    np.ndarray: Demodulated signal.
    """
    pass