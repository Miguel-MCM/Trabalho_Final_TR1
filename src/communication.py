import numpy as np

class Comunication:
    def __init__(self, snr: float, std_dev: float = 0.4):
        self.snr = snr
        self.data = np.array([], dtype=np.float32)
        self.std_dev = std_dev

    def send(self, data: np.ndarray) -> None:
        """Send data with a specified SNR."""
        if not isinstance(data, np.ndarray):
            raise ValueError("Data must be a numpy array.")
        self.data = data.copy()
        noise = np.random.normal(0, self.std_dev, size=data.shape) * 1/self.snr
        self.data += noise

    def receive(self) -> np.ndarray:
        """Receive data with noise added."""
        return self.data.copy()