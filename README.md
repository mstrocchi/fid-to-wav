# FID to .wav
A Simple tool to convert Varian/Agilent FID files to both .wav and .csv.

!["Plot"](resources/images/plot.png)

## Usage

1) Open a shell window and clone the project.
    ```bash
    $ git clone https://github.com/mstrocchi/fid-to-wav.git
    ```

2) Put your FID files into the `resources` directory.

3) Get into the project's directory.
    ```bash
    $ cd fid-to-wav
    ``` 

4) Install the required packages.
    ```bash
    $ pip install -r requirements.txt 
    ``` 
5) Change the name of `DIR` variable at the top of `fid-to-wav.py` to the name of directory you just added.

6) Make `fid-to-wav.py` executable.
    ```bash
    $ chmod +x fid-to-wav.py
    ```

7) Run it.
    ```bash
    $ python fid-to-wav.py
    ```


#### You're done!