import random
import os
import shutil

##### SETTINGS #####

raw_wav_dir = 'raw-wav'
base_metadata_file = 'metadata.csv'
audio_file_type = '.wav'
n_val_files = 100
dataset_dir = 'audio-dataset'
val_metadata_file = 'metadata-val.csv'
train_metadata_file = 'metadata-train.csv'
val_dir = 'val'
train_dir = 'train'

####################

if __name__ == '__main__':  

  # sort existing files
  lines = []
  with open(base_metadata_file, 'r') as file:
    for line in file:
      filename = line.split('|')[0] + audio_file_type
      audio_filepath = os.path.join(raw_wav_dir, filename)
      if os.path.exists(audio_filepath):
        lines.append(line)

  # randomly separate validation and training data
  random.shuffle(lines)
  val_lines = lines[:n_val_files]  
  train_lines = lines[n_val_files:]

  # create temporary metadata files
  with open(val_metadata_file, 'w') as file:
    for line in val_lines:
      file.write(line)
  with open(train_metadata_file, 'w') as file:
    for line in train_lines:
      file.write(line)

  # create directories
  os.mkdir(dataset_dir)
  os.mkdir(os.path.join(dataset_dir, val_dir))
  os.mkdir(os.path.join(dataset_dir, train_dir))

  # create validation files
  shutil.move(val_metadata_file, os.path.join(dataset_dir, val_dir, val_metadata_file))
  for line in val_lines:
    filename = line.split('|')[0] + audio_file_type
    source_path = os.path.join(raw_wav_dir, filename)
    dest_path = os.path.join(dataset_dir, val_dir, filename)
    shutil.copy2(source_path, dest_path)

  # create training files
  shutil.move(train_metadata_file, os.path.join(dataset_dir, train_dir, train_metadata_file))
  for line in train_lines:
    filename = line.split('|')[0] + audio_file_type
    source_path = os.path.join(raw_wav_dir, filename)
    dest_path = os.path.join(dataset_dir, train_dir, filename)
    shutil.copy2(source_path, dest_path)
