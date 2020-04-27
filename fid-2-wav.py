import wave
import struct
import numpy as np
import nmrglue as ng
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk
from tkinter import ttk


# Constants
DARK_THEME_COLOR = '#3E4149'
LIGHT_THEME_COLOR = '#E7E7E7'
FRAMERATE = 8000

# Global variables
dir_path = ''
y = []


def plot():
    """
    Plots a graph given the y vector.
    This is a callback function.
    :return: void
    """
    global y
    if y.size == 0:
        print("Load FID file first!")
        return
    times = np.arange(0, y.size, 1)
    x = np.true_divide(times, np.max(np.abs(times)))
    plt.plot(x, y, 'ko', color="blue", markersize=1)
    plt.show()
    print("Plot is ready!")


def load_directory_path():
    """
    Loads a path to directory.
    This is a callback function.
    :return: void
    """
    global dir_path
    dir_path = filedialog.askdirectory()
    text = "Selected path: " + dir_path
    # filepath_label = tk.Label(text=text, bg=THEME_COLOR, fg="white").pack()
    print(text)


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


def parse_file(producer):
    """
    Given a producer name, return appropriate parse function.
    :param producer: NMR machine producer.
    :return: function that reads file.
    """
    global dir_path

    print("Parsing using producer: " + producer)
    return {
        "Agilent": (lambda: ng.agilent.read(dir=dir_path)),
        "Bruker": (lambda: ng.bruker.read(dir=dir_path)),
        "Varian": (lambda: ng.varian.read(dir=dir_path)),
    }.get(producer)


def generate_wav_from():
    """
    Generates the wav given the path to FID raw files.
    If path was not set, it will return. This is a callback function.
    :return: void
    """
    global y, dir_path

    # Check that directory was set
    if dir_path == '':
        print("Directory was not specified!")
        return

    # Parse file according to machine producer
    dic, data = parse_file(machine_producer.get())()

    # Translate data into curve
    transposed_data = data.transpose()
    converted_re = np.ascontiguousarray(transposed_data.real, dtype=np.float32)
    converted_im = np.ascontiguousarray(transposed_data.imag, dtype=np.float32)
    data = (converted_re + converted_im)

    # Normalize data
    y = np.true_divide(data, np.max(np.abs(data)))

    # Write .wav and plot curve
    write_wav(y, dir_path + "/sound.wav", FRAMERATE, 32700)


# GUI
root = Tk()
root.title("FID2WAV")
root.geometry("240x240")
root.configure(bg=LIGHT_THEME_COLOR)
root.resizable(width=False, height=False)

b1 = ttk.Button(root, text="Select FID directory", command=load_directory_path).pack(pady=20)

choice_label = ttk.Label(root, text="Choose your NMR producer")
choice_label.pack()
machine_producer = ttk.Combobox(root, state="readonly", values=["Agilent", "Bruker", "Varian"])
machine_producer.pack(pady=8)

b2 = ttk.Button(root, text="Generate wav", command=generate_wav_from)
b2.pack(pady=8)
b3 = ttk.Button(root, text="Plot", command=plot)
b3.pack(pady=8)

root.mainloop()
