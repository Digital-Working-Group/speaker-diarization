import os
from enum import Enum
from typing import *

import torch
from pyannote.audio import Pipeline
from pyannote.core import Annotation

NUM_THREADS = 1
os.environ["OMP_NUM_THREADS"] = str(NUM_THREADS)
os.environ["MKL_NUM_THREADS"] = str(NUM_THREADS)
torch.set_num_threads(NUM_THREADS)
torch.set_num_interop_threads(NUM_THREADS)

class Engines(Enum):
    PYANNOTE = "PYANNOTE"

class Engine:
    def diarization(self, path: str) -> "Annotation":
        raise NotImplementedError()

    def cleanup(self) -> None:
        raise NotImplementedError()

    def is_offline(self) -> bool:
        raise NotImplementedError()

    def __str__(self) -> str:
        raise NotImplementedError()

    @classmethod
    def create(cls: Engines, **kwargs: Any) -> "Engine":
        x = kwargs.get('engine')
        try:
            subclass = {
                Engines.PYANNOTE: PyAnnoteEngine,
            }[x]
        except KeyError:
            raise ValueError(f"cannot create `{cls.__name__}` of type `{x.value}`")
        kwargs.pop('engine')
        return subclass(**kwargs)
    
class PyAnnoteEngine(Engine):
    def __init__(self, auth_token, use_gpu: bool = False) -> None:
        if use_gpu and torch.cuda.is_available():
            torch_device = torch.device("cuda")
        else:
            torch_device = torch.device("cpu")
        token = auth_token()
        self._pretrained_pipeline = Pipeline.from_pretrained(
            checkpoint_path="pyannote/speaker-diarization-3.1",
            use_auth_token=token,
        )
        self._pretrained_pipeline.to(torch_device)
        super().__init__()

    def diarization(self, path: str) -> "Annotation":
        return self._pretrained_pipeline(path)

    def cleanup(self) -> None:
        self._pretrained_pipeline = None

    def is_offline(self) -> bool:
        return True

    def __str__(self) -> str:
        return Engines.PYANNOTE.value