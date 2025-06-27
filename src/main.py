import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    from data_link_layer.char_counting_framer import CharCountingFramer
    from data_link_layer.byte_flag_framer import ByteFlagFramer
    from data_link_layer.bits_flag_framer import BitsFlagFramer

    # Generate a random sequence of bits
    bytes = np.random.randint(0, 256, size=7)
    bytes = np.array([126, 1, 126 ,126])
    bits = CharCountingFramer.uint8_to_bits(bytes)

    #framer = CharCountingFramer(counter_size=1)
    #framer = ByteFlagFramer()
    framer = BitsFlagFramer()

    framed_bits = framer.frame_data(bits)

    # Example usage of the NRZ modulator
    #from physical_layer.nrz_modulator import NRZModulator
    #from physical_layer.manchester_modulator import ManchesterModulator
    from physical_layer.bipolar_modulator import BipolarModulator

    # Create an instance of the NRZ modulator
    #modulator = NRZModulator(bit_rate=1e6, sample_rate=10e8)
    #modulator = ManchesterModulator(bit_rate=1e6, sample_rate=10e8)
    modulator = BipolarModulator(bit_rate=1e6, sample_rate=10e8)

    # Modulate the bits
    modulated_signal = modulator.modulate(framed_bits)

    from communication import Comunication
    # Create a communication channel with a specified SNR
    comm_channel = Comunication(snr=10)
    comm_channel.send(modulated_signal)

    received = comm_channel.receive()

    demodulated_received_bit = modulator.demodulate(received)

    deframed_received_bits = framer.deframe_data(demodulated_received_bit)

    # Print results
    print("Original Bytes: ", bytes)
    print("Original Bits: ", bits)
    #print("Framed Bytes: ", framer.bits_to_uint8(framed_bits))
    print("Framed Bits: ", framed_bits)
    print("Demodulated Received Bits: ", demodulated_received_bit)
    print("Deframed Received Bits: ", deframed_received_bits)
    print("Deframed Received Bytes: ", framer.bits_to_uint8(deframed_received_bits))


    plt.plot(np.linspace(0, len(received) / modulator.sample_rate, num=len(received)), received, color='red', )
    plt.plot(np.linspace(0, len(modulated_signal) / modulator.sample_rate, num=len(modulated_signal)), modulated_signal)
    plt.grid(axis='x')
    #plt.xticks(np.arange(0, 1/ modulator.bit_rate, step=1/modulator.bit_rate))
    plt.xticks(np.linspace(0, len(modulated_signal) / modulator.sample_rate, num=len(bits)+1))
    plt.title("NRZ Modulated Signal")
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.show()