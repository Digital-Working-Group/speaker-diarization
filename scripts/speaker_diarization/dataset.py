import glob
import os.path
from enum import Enum
from typing import *
from pathlib import Path

from pyannote.core import Annotation

from util import load_rttm, rttm_to_annotation, get_audio_length

Sample = Tuple[str, str, float]


class Datasets(Enum):
    VOX_CONVERSE = "VoxConverse"


class Dataset:
    @property
    def size(self) -> int:
        raise NotImplementedError()

    @property
    def samples(self) -> Sequence[Sample]:
        raise NotImplementedError()

    def get(self, index: int) -> Tuple[str, float, Annotation]:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def create(cls, **kwargs: Any) -> "Dataset":
        x = kwargs.get("dataset")
        data_folder = kwargs.get("data_folder")

        try:
            subclass = {
                Datasets.VOX_CONVERSE: VoxConverse,
            }[x]
        except KeyError:
            raise ValueError(f"cannot create `{cls.__name__}` of type `{x.value}`")
        
        kwargs.pop('dataset')
        return subclass(**kwargs)


class VoxConverse(Dataset):
    def __init__(self, data_folder: str, **kwargs: Any) -> None:
        self._samples = list()
        data_folder_path = Path(data_folder).resolve()
        for folder in data_folder_path.iterdir():
            if not folder.is_dir():
                continue

            wav_file = None
            audio_length = None
            rttm_file = None

            for item in folder.iterdir():
                if item.suffix == ".wav":
                    if wav_file is not None:
                        raise ValueError(f"Multiple .wav files in {folder}")
                    wav_file = item
                    audio_length = get_audio_length(wav_file)
                elif item.suffix == ".rttm":
                    if rttm_file is not None:
                        raise ValueError(f"Multiple .rttm files in {folder}")
                    rttm_file = item 
            self._samples.append((wav_file, rttm_file, audio_length))

    @property
    def size(self) -> int:
        return len(self._samples)

    @property
    def samples(self) -> Sequence[Sample]:
        return self._samples

    def get(self, index: int) -> Tuple[str, float, Annotation]:
        audio_path, label_path, audio_length = self._samples[index]
        rttm = load_rttm(label_path)
        label = rttm_to_annotation(rttm)
        label.uri = os.path.basename(audio_path)
        return audio_path, audio_length, label

    def __str__(self) -> str:
        return "VoxConverse"


__all__ = [
    "Datasets",
    "Dataset",
    "Sample"
]