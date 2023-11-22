import random
import os
import zipfile

### SETTINGS ###
raw_wav_dir = 'raw-wav'
base_metadata_file = 'metadata.csv'
audio_file_type = '.wav'
n_val_files = 100
zip_filename = 'audio_dataset.zip'
val_metadata_file = 'metadata-val.csv'
train_metadata_file = 'metadata-train.csv'
################

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

  # create zip file
  with zipfile.ZipFile(zip_filename, 'w') as zip_file:
    val_dir = 'val'
    train_dir = 'train'
    # validation files
    zip_file.write(val_metadata_file, os.path.join(val_dir, val_metadata_file))
    for line in val_lines:
      filename = line.split('|')[0] + audio_file_type
      current_path = os.path.join(raw_wav_dir, filename)
      zipped_path = os.path.join(val_dir, filename)
      zip_file.write(current_path, zipped_path)
    # training files
    zip_file.write(train_metadata_file, os.path.join(train_dir, train_metadata_file))
    for line in train_lines:
      filename = line.split('|')[0] + audio_file_type
      current_path = os.path.join(raw_wav_dir, filename)
      zipped_path = os.path.join(train_dir, filename)
      zip_file.write(current_path, zipped_path)

  # remove temporary metadata files
  os.remove(val_metadata_file)
  os.remove(train_metadata_file)