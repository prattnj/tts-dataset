import torch
import torch.nn as nn

class VocalData(nn.Dataset):
  def __init__(self, zip_path='audio_dataset.zip'):
    super(VocalData, self).__init__()
    pass