# Text-to-Speech Dataset Creator
Contents:
* [change_sampling_rate.py](#change_sampling_ratepy)
* [create_zip.py](#create_zip)
* [dataset.py](#dataset)
* [wav_generator.py](#wav_generator)

## change_sampling_rate
[Python file here](change_sampling_rate.py)  
Changes the sampling rate of all the .wav files in the specified directory.
By default, it changes the sampling rate to 22050 Hz because that is the sampling rate used by the
LJ Speech Dataset, which was used to train Tacotron 2. Useful if the vocal samples were recorded
in a different sampling rate.

## create_zip
[Python file here](create_zip.py)  
Sorts the raw .wav data into training and validation sets, then creates a .zip file to be used for the [dataset](dataset.py) class.
By default, the validation data is made up of 100 randomly selected files and the training data is the rest.
Additionally, a metadata CSV file is created for each new directory. Upon completion, there will be a .zip file
created in this directory with this structure:
* 'val' directory
    * metadata.csv
    * (every .wav file randomly selected to be in the validation set)
* 'train' directory
    * metadata.csv
    * (every other .wav file not randomly selected to be in the validation set)

## dataset
[Python file here](dataset.py)  
A Python class representing the dataset to be used with PyTorch.

## wav_generator
[Python file here](wav_generator.py)  
Where all the magic happens. Much of this was adapted from [padmalcom/ttsdatasetcreator](https://github.com/padmalcom/ttsdatasetcreator).
Using the data found in [metadata.csv](metadata.csv), which is the metadata file from the LJ Speech Dataset,
the user selects a microphone and the program prompts the user over and over again for vocal input.
At the top of the screen, the sentence to be read is displayed. The user speaks the sentence, and instructions are given
for keeping the sample and continuing, discarding the sample and repeating, or ending the recording session.
The silence at the beginning and end of the sample is trimmed off, using a certain decibel threshold with a small
buffer to prevent speech getting cut off. Silence in the middle of the sentence is kept. All of the vocal samples
are stored in the raw-wav directory under the filename specified in metadata.csv. After the desired amount of recording
is complete, use [create_zip](#create_zip) to compile the data and [dataset](#dataset) to load the data in PyTorch.