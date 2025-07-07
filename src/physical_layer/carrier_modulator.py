from abc import ABC, abstractmethod
import numpy as np


class CarrierModulator:
  """Abstract base class for carrier modulators.
  This class defines the interface for carrier modulation schemes.
  It includes methods for modulation and demodulation of signals.
  """
  def __init__(self, carrier_frequency: float, bit_rate: float, sample_rate: float):
    """
    Initialize the carrier modulator.

    Parameters:
    carrier_frequency (float): Frequency of the carrier signal.
    signals (list[float]): List of signals to use for modulation.
    """
    self.carrier_frequency = carrier_frequency
    self.bit_rate = bit_rate
    self.sample_rate = sample_rate
    self.samples_per_bit = int(sample_rate / bit_rate)

  @abstractmethod
  def modulate(self, bits: np.ndarray) -> np.ndarray:
    """
    Modulate a signal using the carrier modulation scheme.

    Parameters:
    signal (np.ndarray): Signal to modulate.

    Returns:
    np.ndarray: Modulated signal.
    """
    pass

  @abstractmethod
  def demodulate(self, signal: np.ndarray) -> np.ndarray:
    """
    Demodulate a signal using the carrier modulation scheme.

    Parameters:
    signal (np.ndarray): Signal to demodulate.

    Returns:
    np.ndarray: Demodulated signal.
    """
    pass

  def get_time(self, signal: np.ndarray) -> np.ndarray:
    return np.arange(len(signal)) / self.sample_rate