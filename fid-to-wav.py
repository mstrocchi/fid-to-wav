import wave
import struct
import numpy as np
import nmrglue as ng
import matplotlib.pyplot as plt


DIR_NAME = "2-ketobutyric_acid"
RESOURCES = "./resources/"
OUTPUT = "./output/"
FRAMERATE = 44100


def data_to_csv(data):
    """
    Convert the input data to .csv
    :param data: 1D vector.
    :return: void
    """
    np.savetxt(OUTPUT + DIR_NAME + ".csv", data, delimiter=',')


def plot(x, y):
    """
    Plots x and y values
    :param x: coordinates vector.
    :param y: coordinates vector.
    :return: void
    """
    plt.plot(x, y, 'ko', color="blue", markersize=1)
    plt.show()


def read(directory):
    """
    Reads the files in Directory
    :param directory: where the files are expected to be.
    :return: data as x, y vectors.
    """
    dic, data = ng.varian.read(dir=directory)
    transposed_data = data.transpose()

    re = transposed_data.real
    im = transposed_data.imag
    converted_re = np.ascontiguousarray(re, dtype=np.float32)
    converted_im = np.ascontiguousarray(im, dtype=np.float32)

    y = (converted_re + converted_im)
    x = np.arange(0, y.size, 1)

    return x, y


def write_wav(data, filename, framerate, amplitude):
    """
    Writes the .wav file
    :param data: to be written.
    :param filename: to be written.
    :param framerate: wav conversion parameter.
    :param amplitude: wav conversion parameter.
    :return:
    """
    file_wav = wave.open(filename, "w")
    number_of_channels = 1
    sample_width = 2
    framerate = framerate
    number_of_frames = len(data)
    compression_type = "NONE"
    compression_name = "not compressed"
    file_wav.setparams((number_of_channels,
                        sample_width,
                        framerate,
                        number_of_frames,
                        compression_type,
                        compression_name))

    print("Writing .wav file...")
    for value in data:
        file_wav.writeframes(struct.pack('i', int(value * amplitude)))
    file_wav.close()
    print("Done!")


def main():
    # Get the data from file
    times, data = read("./resources/" + DIR_NAME)

    # Normalize data
    x = np.true_divide(times, np.max(np.abs(times)))
    y = np.true_divide(data, np.max(np.abs(data)))

    # Write .wav and plot curve
    write_wav(y, OUTPUT + DIR_NAME + ".wav", FRAMERATE, 32700)
    data_to_csv(y)
    plot(x, y)


if __name__ == "__main__":
    main()
