import json
from pathlib import Path
import torch

import torchaudio
from torch.utils.data import Dataset
from torch.nn import functional as F


class GANSynthDataset(Dataset):
    """
    Dataset class for NSynth [json/wav] - download from
    https://magenta.tensorflow.org/datasets/nsynth
    Dataset used for GANSynth model training
    dataset folder should have structure "example.json" with metadata about
    audio files and directory audio containing audio files with .wav file extension
    """

    def __init__(self, train_data_dir: Path):
        super().__init__()
        with (train_data_dir / "examples.json").open() as f:
            self.metadata = json.load(f)

        self.filepaths = list((train_data_dir / "audio").glob("*.wav"))

    def __getitem__(self, idx):
        filepath = self.filepaths[idx]
        audio_tensor, _ = torchaudio.load(filepath)
        audio_tensor = torch.squeeze(audio_tensor, 0)
        spectrogram = torch.view_as_real(
            torch.stft(audio_tensor, 2048, 512, return_complex=True)
        )
        spectrogram = spectrogram.narrow(0, 0, 1024)
        spectrogram = F.pad(spectrogram, (0, 0, 0, 2))
        spectrogram = torch.movedim(spectrogram, (2, 0), (0, 2))

        filename = filepath.name.replace(".wav", "")
        pitch = 0
        if filename in self.metadata:
            pitch = self.metadata[filename]["pitch"] % 61

        return (spectrogram, pitch)

    def __len__(self):
        return len(self.filepaths)
