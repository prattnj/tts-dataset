import librosa
import soundfile
import os

### SETTINGS ###
wav_dir = 'raw-wav'
new_rate = 22050 # LJ Speech (used to train Tacotron) uses 22050
################

if __name__ == '__main__':

  print('Updating sampling rates...')
  for filename in os.listdir(wav_dir):

    full_path = os.path.join(wav_dir, filename)

    # continue if this is not a wav file
    if not os.path.isfile(full_path) or filename[-4:] != '.wav':
      continue

    wav, original_rate = librosa.load(full_path, sr=None)
    wav = librosa.resample(wav, orig_sr=original_rate, target_sr=new_rate)
    soundfile.write(full_path, wav, new_rate)
  print('Done. Remember to recompile the .zip if applicable.')
