import wave
import struct
import numpy as np
import nmrglue as ng
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import Tk
from tkinter import ttk
from tkinter import TOP

# Constants - global settings
LIGHT_THEME_COLOR = '#E7E7E7'
FILE_NAME = 'sound.wav'
FRAMERATE = 8000
AMPLITUDE = 32700

# Global variables
path_to_directory = ''
data = []


def load_path():
    """
    Loads the path to the FID raw files directory.
    This is a callback function.
    :return: void
    """
    global path_to_directory
    path_to_directory = filedialog.askdirectory()
    # Check that directory was set
    if path_to_directory == '':
        print("Directory was not specified!")
    else:
        print("Selected path: " + path_to_directory)


def write_wav():
    """
    Writes the .wav file.
    This is a callback function.
    :param data: to be written.
    :param filename: to be written.
    :param framerate: wav conversion parameter.
    :param amplitude: wav conversion parameter.
    :return:
    """
    global data
    file_path = (path_to_directory + '/' + FILE_NAME)
    file_wav = wave.open(file_path, "w")
    number_of_channels = 1
    sample_width = 2
    number_of_frames = len(data)
    compression_type = "NONE"
    compression_name = "not compressed"
    file_wav.setparams((number_of_channels,
                        sample_width,
                        FRAMERATE,
                        number_of_frames,
                        compression_type,
                        compression_name))

    print("Writing .wav file...")
    for value in data:
        file_wav.writeframes(struct.pack('i', int(value * AMPLITUDE)))
    file_wav.close()
    print("Done!")


def plot():
    """
    Plots a graph given the y vector.
    This is a callback function.
    :return: void
    """
    global data
    if data.size == 0:
        print("Load FID file first!")
        return
    times = np.arange(0, data.size, 1)
    x = np.true_divide(times, np.max(np.abs(times)))
    plt.plot(x, data, 'ko', color="blue", markersize=1)
    plt.show()
    print("Plot is ready!")


def parse_file(producer):
    """
    Given a producer name, return appropriate parse function.
    :param producer: NMR machine producer.
    :return: function that reads file.
    """
    global path_to_directory
    print("Parsing using producer: " + producer)
    return {
        "Agilent": (lambda: ng.agilent.read(dir=path_to_directory)),
        "Bruker": (lambda: ng.bruker.read(dir=path_to_directory)),
        "Varian": (lambda: ng.varian.read(dir=path_to_directory)),
    }.get(producer)


def parse():
    global data
    producer = machine_producer.get()

    if producer == '':
        print("Please, specify a producer before parsing.")
        return
    try:
        # Parse file according to machine producer
        dic, data = parse_file(producer)()
    except (FileNotFoundError, AttributeError):
        print("Your FID files do not match the producer specified. Try with a different producer.")
        # clear the data
        data = []
        return

    # Translate data into curve
    transposed_data = data.transpose()
    converted_re = np.ascontiguousarray(transposed_data.real, dtype=np.float32)
    converted_im = np.ascontiguousarray(transposed_data.imag, dtype=np.float32)
    data = (converted_re + converted_im)

    # Normalize data
    data = np.true_divide(data, np.max(np.abs(data)))


# GUI
root = Tk()
root.title("FID2WAV")
root.geometry("260x240")
root.configure(bg=LIGHT_THEME_COLOR)
root.resizable(width=False, height=False)

# Define frames
frame_1 = ttk.Frame(root)
frame_2 = ttk.Frame(root)
frame_3 = ttk.Frame(root)
frame_4 = ttk.Frame(root)

# Stack the frames on top of each other
frame_1.pack(side=TOP, pady=20)
frame_2.pack(side=TOP, pady=10)
frame_3.pack(side=TOP, pady=10)
frame_4.pack(side=TOP, pady=10)

# Objects in frame 1
path_button = ttk.Button(frame_1, text="Select FID directory", command=load_path)
path_button.pack()

# Objects in frame 2
choice_label = ttk.Label(frame_2, text="Choose your NMR producer")
choice_label.pack()
machine_producer = ttk.Combobox(frame_2, state="readonly", values=["Agilent", "Bruker", "Varian"])
machine_producer.pack()

# Objects in frame 3
parse_button = ttk.Button(frame_3, text="Parse FID", command=parse)
parse_button.pack()

# Objects in frame 4
write_wav_button = ttk.Button(frame_4, text="Generate wav", command=write_wav)
plot_button = ttk.Button(frame_4, text="Plot", command=plot)
frame_4.columnconfigure(0, weight=1)
frame_4.columnconfigure(1, weight=1)
write_wav_button.grid(row=0, column=0)
plot_button.grid(row=0, column=1)

root.mainloop()
