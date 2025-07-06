import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    from data_link_layer.parity_error_detector import ParityErrorDetector
    from data_link_layer.crc_error_detector import CRCErrorDetector

    from data_link_layer.char_counting_framer import CharCountingFramer
    from data_link_layer.byte_flag_framer import ByteFlagFramer
    from data_link_layer.bits_flag_framer import BitsFlagFramer

    # Generate a random sequence of bits    
    bytes = np.random.randint(0, 256, size=1)
    #bytes = np.array([126, 1, 125 ,126])

    bits = CharCountingFramer.uint8_to_bits(bytes)

    error_detector = None
    #error_detector = ParityErrorDetector(to_byte=True)
    #error_detector = CRCErrorDetector()

    framer = CharCountingFramer(counter_size=1, error_detector=error_detector)
    #framer = ByteFlagFramer(error_detector=error_detector)
    #framer = BitsFlagFramer(error_detector=error_detector)

    framed_bits = framer.frame_data(bits)

    # Example usage of the NRZ modulator
    from physical_layer.nrz_modulator import NRZModulator
    from physical_layer.manchester_modulator import ManchesterModulator
    from physical_layer.bipolar_modulator import BipolarModulator

    # Create an instance of the NRZ modulator
    #modulator = NRZModulator(bit_rate=1e6, sample_rate=10e8)
    modulator = ManchesterModulator(bit_rate=1e6, sample_rate=10e8)
    #modulator = BipolarModulator(bit_rate=1e6, sample_rate=10e8)

    # Modulate the bits
    modulated_signal = modulator.modulate(framed_bits)

    from physical_layer.ask_carrier_modulator import ASKCarrierModulator
    #ask_modulator = ASKCarrierModulator(carrier_frequency=2e6, signals=np.array([-1, 1]))
    ask_modulator = ASKCarrierModulator(carrier_frequency=2e6, signals=np.array([0, 1]))
    #ask_modulator = ASKCarrierModulator(carrier_frequency=2e6, signals=np.array([0, 1, -1]))
    ask_modulated_signal = ask_modulator.modulate(modulated_signal, modulator.get_time(modulated_signal))

    from communication import CommunicationChannel
    # Create a communication channel with a specified SNR
    comm_channel = CommunicationChannel(snr=10)
    comm_channel.send(ask_modulated_signal)

    received = comm_channel.receive()

    demodulated_received_signal = ask_modulator.demodulate(received, modulator.get_time(received), kernel_size=modulator.samples_per_bit//10)
    demodulated_received_bit = modulator.demodulate(demodulated_received_signal)
    #demodulated_received_bit[2] = 0
    #demodulated_received_bit[-10] = 0

    try:
        deframed_received_bits = framer.deframe_data(demodulated_received_bit)
    except ValueError as e:
        print("Error: ",e)
        deframed_received_bits = None

    # Print results
    print("Original Bytes: ", bytes)
    print("Original Bits: ", bits)
    #print("Framed Bytes: ", framer.bits_to_uint8(framed_bits))
    print("Framed Bits: ", framed_bits)
    print("Demodulated Received Bits: ", demodulated_received_bit)
    print("Deframed Received Bits: ", deframed_received_bits)
    print("Deframed Received Bytes: ", framer.bits_to_uint8(deframed_received_bits) if deframed_received_bits is not None else None)


    plt.plot(modulator.get_time(received), received, color='red', )

    plt.plot(modulator.get_time(ask_modulated_signal), ask_modulated_signal, color='green')
    plt.show()
    plt.plot(modulator.get_time(demodulated_received_signal), demodulated_received_signal, color='yellow')
    plt.plot(modulator.get_time(modulated_signal), modulated_signal, color='blue')
    plt.grid(axis='x')
    #plt.xticks(np.arange(0, 1/ modulator.bit_rate, step=1/modulator.bit_rate))
    #plt.xticks(modulator.get_time(modulated_signal))
    plt.title("NRZ Modulated Signal")
    plt.ylabel("Amplitude")
    plt.xlabel("Time (s)")
    plt.show()