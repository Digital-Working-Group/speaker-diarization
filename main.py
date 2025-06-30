"""
main.py
Provides and example run of the speaker diarization
"""
from scripts.speaker_diarization.read_token import read_token
from pyannote_diarize import prep_and_diarize

def main():
    """
    Runs speaker diarization using Pyannote.audio speaker diar 3.1
    """
    token = read_token()
    sample_audio_fps = ['sample_files/short_wav/first_ten_Sample_HV_Clip.wav', 
                        'sample_files/short_wav/Sample_HV_Clip.wav']
    prep_and_diarize(token, sample_audio_fps)


if __name__ == '__main__':
    main()