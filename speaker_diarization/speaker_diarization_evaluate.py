import os
import json
from datetime import datetime
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate, JaccardErrorRate

def process_accuracy(gt_rttm, hyp_rttm, **kwargs):
    """
    Compare the accuracy of a ground truth rttm and a generated rttm
    """
    verbose = kwargs.get('verbose', False)
    results_folder = os.path.join(os.path.dirname(__file__), "evaluation_results")
    metric_der = DiarizationErrorRate(detailed=True, skip_overlap=True)
    metric_jer = JaccardErrorRate(detailed=True, skip_overlap=True)
    metrics = [metric_der, metric_jer]

    reference = next(iter(load_rttm(gt_rttm).values()))
    hypothesis = next(iter(load_rttm(hyp_rttm).values()))

    ## results folder, timestamp?? maybe adjust where this is going

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(os.path.join(results_folder, timestamp), exist_ok=True)
    try:
        for metric in metrics:
            res = metric(reference, hypothesis, detailed=True)
            if verbose:
                print("GT:", gt_rttm)
                print("HYP segments:", hyp_rttm)
                print(f"{metric.name}: {res}")
    except KeyboardInterrupt:
        print("Stopping benchmark...")
    results = dict()
    for metric in metrics:
        results[metric.name] = abs(metric)
    results_path = os.path.join(results_folder, timestamp, "evaluation.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    results_details_path = os.path.join(results_folder, timestamp, "evaluation.log")
    with open(results_details_path, "w") as f:
        for metric in metrics:
            f.write(f"{metric.name}:\n{str(metric)}")
            f.write("\n")

def main() -> None:
    process_kwargs = {
        "verbose": "True"
    }
    gt_rttm = "ground_truth_files/first_minute_Sample_HV_Clip_ground_truth.rttm"
    hyp_rttm = "sample_files/short_wav/first_minute_Sample_HV_Clip.rttm"
    process_accuracy(gt_rttm, hyp_rttm, **process_kwargs)

if __name__ == "__main__":
    main()