"""
pyannote_diarize.py
generate pyannote diarization
"""
import torch
import torchaudio
import pandas as pd
from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
from scripts.speaker_diarization.read_token import read_token

def prep_and_diarize(token, audio_fps, **kwargs):
    """
    Takes in a Hugging Face token and a list of filepaths and diarizes each one
    """
    kwargs['num_speakers'] = kwargs.get('num_speakers', 2)
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
    if torch.cuda.is_available():
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    pipeline.to(device)
    for audio_fp in audio_fps:
        rttm_out = audio_fp.replace('.wav', '.rttm')
        csv_out = rttm_out.replace('.rttm', '.csv')
        diarize_file(pipeline, audio_fp, rttm_out, csv_out, **kwargs)

def read_rttm_line(line):
    """
    read line
    """
    segment_type, file_id, channel_id, turn_onset, turn_duration, ortho_field,\
        speaker_type, speaker_name, confidence_score, signal_lookahead_time = line.split()
    return {'segment_type': segment_type, 'file_id': file_id, 'channel_id': channel_id,
        'turn_onset': turn_onset, 'turn_duration': turn_duration, 'ortho_field': ortho_field,
        'speaker_type': speaker_type, 'speaker_name': speaker_name,
        'confidence_score': confidence_score, 'signal_lookahead_time': signal_lookahead_time}

def rttm_to_csv(rttm_in, csv_out):
    """
    type: segment type (speaker)
    file_id: filename (waveform when preloaded)
    channel_id: is always 1
    turn_onset: onset of turn in seconds from beginning of the recording
    turn_duration: duration of turn in seconds
        turn_end: turn_onset + turn_duration
            (calculated, not included in RTTM)
    orthography field: always NA
    speaker_type: always NA
    speaker_name: string for speaker
    confidence score: always NA
    signal_lookahead_time: always Na

    irrelevant RTTM components are ignored in the CSV;
    """
    keep_headers = ['turn_onset', 'turn_end', 'turn_duration', 'speaker_name']
    to_write = []
    with open(rttm_in, "r", encoding="utf-8") as infile:
        for line in infile.readlines():
            row = read_rttm_line(line)
            row['turn_end'] = round(float(row['turn_onset']) + float(row['turn_duration']), 3)
            row = {k: row[k] for k in keep_headers}
            to_write.append(row)
    pd.DataFrame(to_write).to_csv(csv_out, index=False)
    print(csv_out)

def diarize_file(pipeline, audio_fp, rttm_out, csv_out, **kwargs):
    """
    diarize one file
    """
    print(audio_fp)
    waveform, sample_rate = torchaudio.load(audio_fp)
    with ProgressHook() as hook:
        diarization = pipeline({'waveform': waveform, 'sample_rate': sample_rate}, hook=hook,
            **kwargs)
        with open(rttm_out, 'w') as outfile:
            diarization.write_rttm(outfile)
        print(rttm_out)
    rttm_to_csv(rttm_out, csv_out)

def check_params():
    """
    check hyperparameters
    """
    token = read_token()
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=token)
    print(pipeline.parameters(instantiated=True))

if __name__ == '__main__':
    check_params()
