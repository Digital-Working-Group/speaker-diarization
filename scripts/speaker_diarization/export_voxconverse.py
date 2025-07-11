"""export_hf.py"""
import os
from itertools import islice
from datasets import load_dataset
import soundfile as sf
from read_token import read_token

def write_rttm(data, outpath, file_id):
    """
    Write an RTTM file from the diarization data dictionary
    """
    rttm_out = outpath.replace('.wav', '.rttm')
    with open(rttm_out, 'w', encoding="utf-8") as f:
        for start, end, speaker in zip(data['timestamps_start'],
                                       data['timestamps_end'],
                                       data['speakers']):
            duration = end - start
            line = f"SPEAKER {file_id} 1 {start:.3f} {duration:.3f} <NA> <NA> {speaker} <NA> <NA>\n"
            f.write(line)

def load_hugging_face_dataset(set_size=10):
    """Load VoxConverse dataset from hugging face"""
    print("Loading VoxConverse dataset...")
    try:
        dataset = load_dataset("diarizers-community/voxconverse", split="dev", streaming=True)
    except FileNotFoundError:
        token = read_token()
        dataset = load_dataset("diarizers-community/voxconverse", split="dev",
                               streaming=True, use_auth_token=token)
    print("Loaded VoxConverse dataset..")
    return list(islice(dataset, set_size))

def export_hf_voxconverse():
    """Write VoxConverse dataset wav files and rttm ground truth files"""
    dataset = load_hugging_face_dataset()
    out_root = "hf_voxconverse_data"
    for i, sample in enumerate(dataset):
        audio = sample["audio"]
        file_id = f"sample_{i}"
        out_dir = os.path.join(out_root, file_id)
        os.makedirs(out_dir, exist_ok=True)
        outpath = os.path.join(out_dir, f"{file_id}.wav")
        print(f'writing {outpath}')
        sf.write(outpath, audio["array"], audio["sampling_rate"])
        write_rttm(sample, outpath, file_id)

if __name__ == "__main__":
    export_hf_voxconverse()
