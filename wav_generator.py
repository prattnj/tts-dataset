# Adapted from https://github.com/padmalcom/ttsdatasetcreator

from rich import print
from rich.console import Console
import os
import time
import pyaudio
import keyboard
from rich.progress import Progress
from rich.table import Table
import wave
import librosa
import numpy as np
import soundfile
import sys
import csv
import matplotlib.pyplot as plt

# File info
wav_dir = 'raw-wav'
metadata_csv_file = 'metadata.csv'

# Audio processing
chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
frame_rate = 22050 # LJ Speech (used to train Tacotron) uses 22050
timeout = 60

# Audio trimming
db_threshold = -20
start_buffer = 10
end_buffer = 30

# Takes audio and trims the beginning and end (by a certain buffer) based on a preset decibel threshold
def trim_audio(wav):
	
	rms_db = librosa.amplitude_to_db(librosa.feature.rms(y=wav), ref=np.max)[0]

	first, last = None, None
	for i, sample in enumerate(rms_db):
		if sample > db_threshold:
			if first is None:
				first = i
			last = i

	first = first - start_buffer
	last = last + end_buffer
	mask = np.array([(i >= first and i <= last) for i in range(len(rms_db))])

	mask = np.repeat(mask, len(wav) // len(mask))
	for _ in range(len(wav) % len(mask)):
		mask = np.append(mask, False)

	return wav[mask == True]

if __name__ == '__main__':

	console = Console()
		
	table = Table()
	table.add_column("TSS Dataset Creator", style="cyan")
	table.add_row("2021 - padmalcom")
	table.add_row("www.stonedrum.de")	
	
	console.print(table)
	
	console.print("\nPlease select your [red]microphone[/red] (enter the device number).")
	
	pyaudio = pyaudio.PyAudio()
	
	# select input device
	info = pyaudio.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')
	for i in range(0, numdevices):
		if (pyaudio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
			print ("Input Device id ", i, " - ", pyaudio.get_device_info_by_host_api_device_index(0, i).get('name'))
	in_mic_id = int(input())
	console.print("You have selected [red]%s[/red] as input device." % pyaudio.get_device_info_by_host_api_device_index(0, in_mic_id).get('name'))
	
	console.print("wavs will be saved in [red]%s" % wav_dir)
				
	# load csv
	with open(metadata_csv_file, encoding = "utf-8") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter='|')
		csv_data = list(csv_reader)
		
	console.print("Found %d sentences." % len(csv_data))

	if len(csv_data) == 0:
		console.print("You need to add some sentences to your text files first. Exiting.")
		sys.exit(0)
	
	console.print("[green]n[/green] = next sentence, [yellow]d[/yellow] = discard and repeat last recording, [red]e[/red] = exit recording.")
	
	console.print("Ready?", style="green")
	input("Press Enter to start")
	
	i = 0
	cancelled = False
	while i < len(csv_data):
		console.clear()
		
		current_sentence = csv_data[i][1]
		current_sentence = current_sentence.replace("\n", " ")
		current_sentence = current_sentence.replace("\t", " ")
		
		# If this wav file has been recorded before, continue
		wav_file_name = csv_data[i][0] + '.wav'
		if os.path.exists(os.path.join(wav_dir, wav_file_name)):
			i += 1
			continue
		
		console.print("\n\n" + current_sentence + "\n\n", style = "black on white", justify="center", highlight=False)
		console.print("(%d/%d) [green]n[/green] = next sentence, [yellow]d[/yellow] = discard and repeat last recording, [blue]s[/blue] = skip, [red]e[/red] = exit recording." % ((i+1), len(csv_data)))
		
		start_time = time.time()
		current_time = time.time()
		frames = []
		stream = pyaudio.open(input_device_index = in_mic_id, format=sample_format, channels=channels, rate=frame_rate, frames_per_buffer=chunk, input=True)
		
		with Progress() as recording_progress:
			recording_task = recording_progress.add_task("[red]Recording...", total=timeout)
						
			while not recording_progress.finished:
				recording_progress.update(recording_task, completed = current_time - start_time)
							
				data = stream.read(chunk)
				frames.append(data)
				current_time = time.time()
					
				if keyboard.is_pressed('n'):
					while keyboard.is_pressed('n'):
						time.sleep(0.1)
		
					# Write the wav file
					data = stream.read(chunk)
					frames.append(data)
					stream.close()
					wf = wave.open(os.path.join(wav_dir, wav_file_name), 'wb')
					wf.setnchannels(channels)
					wf.setsampwidth(pyaudio.get_sample_size(sample_format))
					wf.setframerate(frame_rate)										
					wf.writeframes(b''.join(frames))
					wf.close()
					
					# trim silence
					wav, source_sr = librosa.load(str(os.path.join(wav_dir, wav_file_name)), sr=None)
					wav = trim_audio(wav)
					soundfile.write(str(os.path.join(wav_dir, wav_file_name)), wav, source_sr)
					
					i += 1
					break
				elif keyboard.is_pressed("s"):
					while keyboard.is_pressed('s'):
						time.sleep(0.1)
					i += 1
					stream.close()
					break
				elif keyboard.is_pressed("d"):
					while keyboard.is_pressed('d'):
						time.sleep(0.1)
					stream.close()
					break
				elif keyboard.is_pressed("e"):
					while keyboard.is_pressed('e'):
						time.sleep(0.1)
					stream.close()
					cancelled = True
					break
					
			if cancelled:
				break		

	pyaudio.terminate()