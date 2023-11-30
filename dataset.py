import os
import torchaudio
from torch.utils.data import Dataset

# Requires this format for the data directory:
# Two subdirectories: val and train
# Each of the above contains vocal samples (.wav files) and a metadata.csv file with entries formatted like so:
# filename(no extension)|sentence|normalized sentence
class VocalData(Dataset):
  def __init__(self, path, train=True, transform=None):
    self.dir = os.path.join(path, ('train' if train else 'val'))
    self.transform = transform
    self.data = self.load_data()

  def load_data(self):
    # create and return an array of tuples with these elements:
    # [0]: the non-normalized text as a string
    # [1]: the normalized text as a string
    # [2]: the raw waveform data loaded by torchaudio.load()

    data = []
    with open(os.path.join(self.dir, 'metadata.csv'), 'r') as file:
      for line in file:
        parts = line.split('|')
        waveform, _ = torchaudio.load(os.path.join(self.dir, parts[0] + '.wav'))
        data.append((parts[1], parts[2], waveform))

    return data

  def __len__(self):
    return len(self.data)

  def __getitem__(self, idx):
    return self.data[idx]