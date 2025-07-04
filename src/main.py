import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Example usage of the NRZ modulator
    #from physical_layer.nrz_modulator import NRZModulator
    #from physical_layer.manchester_modulator import ManchesterModulator
    from physical_layer.bipolar_modulator import BipolarModulator

    # Create an instance of the NRZ modulator
    #modulator = NRZModulator(bit_rate=1e6, sample_rate=10e8)
    #modulator = ManchesterModulator(bit_rate=1e6, sample_rate=10e8)
    modulator = BipolarModulator(bit_rate=1e6, sample_rate=10e8)

    # Generate a random sequence of bits
    bits = np.random.randint(0, 2, size=10)

    # Modulate the bits
    modulated_signal = modulator.modulate(bits)

    from communication import Comunication
    # Create a communication channel with a specified SNR
    comm_channel = Comunication(snr=2)
    comm_channel.send(modulated_signal)

    received = comm_channel.receive()

    # Demodulate the signal back to bits
    demodulated_bits = modulator.demodulate(modulated_signal)

    demodulated_received_bit = modulator.demodulate(received)

    # Print results
    print("Original Bits: ", bits)
    print("Modulated Signal: ", modulated_signal)
    print("Demodulated Bits: ", demodulated_bits)
    print("Received Signal: ", received)
    print("Demodulated Received Bits: ", demodulated_received_bit)


    plt.plot(np.linspace(0, len(received) / modulator.sample_rate, num=len(received)), received, color='red', )
    plt.plot(np.linspace(0, len(modulated_signal) / modulator.sample_rate, num=len(modulated_signal)), modulated_signal)
    plt.grid(axis='x')
    #plt.xticks(np.arange(0, 1/ modulator.bit_rate, step=1/modulator.bit_rate))
    plt.xticks(np.linspace(0, len(modulated_signal) / modulator.sample_rate, num=len(bits)+1))
    plt.title("NRZ Modulated Signal")
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.show()