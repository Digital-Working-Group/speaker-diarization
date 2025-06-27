"""speaker_diarization_evaluate.py"""
import json

from pyannote.metrics.diarization import (
    DiarizationErrorRate,
    JaccardErrorRate,
)
from tqdm import tqdm

from dataset import *
from engine import *
from util import load_rttm, rttm_to_annotation
from read_token import read_hf_token

DEFAULT_CACHE_FOLDER = os.path.join(os.path.dirname(__file__), "cache")
RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")


def _process_accuracy(engine: Engine, dataset: Dataset, **kwargs) -> None:
    verbose = kwargs.get('verbose', False)
    metric_der = DiarizationErrorRate(detailed=True, skip_overlap=True)
    metric_jer = JaccardErrorRate(detailed=True, skip_overlap=True)
    metrics = [metric_der, metric_jer]

    cache_folder = os.path.join(DEFAULT_CACHE_FOLDER, str(dataset), str(engine))
    print(f"Cache folder: {cache_folder}")
    os.makedirs(cache_folder, exist_ok=True)
    os.makedirs(os.path.join(RESULTS_FOLDER, str(dataset)), exist_ok=True)
    try:
        for index in tqdm(range(dataset.size)):
            audio_path, audio_length, ground_truth = dataset.get(index)
            if verbose:
                print(f"Processing {audio_path}...")

            cache_path = os.path.join(cache_folder, f"{os.path.basename(audio_path)}_cached.rttm")

            if os.path.exists(cache_path):
                hypothesis = rttm_to_annotation(load_rttm(cache_path))
            else:
                hypothesis = engine.diarization(audio_path)

                with open(cache_path, "w") as f:
                    f.write(hypothesis.to_rttm())

            for metric in metrics:
                print("GT segments:", list(ground_truth.itersegments()))
                print("HYP segments:", list(hypothesis.itersegments()))
                res = metric(ground_truth, hypothesis, detailed=True)
                if verbose:
                    print(f"{metric.name}: {res}")
    except KeyboardInterrupt:
        print("Stopping benchmark...")

    results = dict()
    for metric in metrics:
        results[metric.name] = abs(metric)
    results_path = os.path.join(RESULTS_FOLDER, str(dataset), f"{str(engine)}.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    results_details_path = os.path.join(RESULTS_FOLDER, str(dataset), f"{str(engine)}.log")
    with open(results_details_path, "w") as f:
        for metric in metrics:
            f.write(f"{metric.name}:\n{str(metric)}")
            f.write("\n")


def main() -> None:

    dataset_kwargs = {
        "dataset": Datasets.VOX_CONVERSE,
        "data_folder": "voxconverse_data/dev/audio",
        "label_folder":"voxconverse_labels/dev",
        "num_samples": 2

    }

    engine_kwargs = {
        "engine": Engines.PYANNOTE,
        "auth_token": read_hf_token
    }

    # could change this 
    process_kwargs = {
        "verbose": "True"
    }

    dataset = Dataset.create(**dataset_kwargs)
    print(f"Dataset: {dataset}")

    engine = Engine.create(**engine_kwargs)
    print(f"Engine: {engine}")

    _process_accuracy(engine, dataset, **process_kwargs)

if __name__ == "__main__":
    main()

__all__ = [
    "RESULTS_FOLDER",
]