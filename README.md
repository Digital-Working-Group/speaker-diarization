# Speaker Diarization

This repository evaluates the [pyannote-audio](https://github.com/pyannote/pyannote-audio) diarization tool on an audio file.

| Table of Contents |
|---|
| [Speaker Diarization: Installation and Setup](#installation-and-setup)|
| [Speaker Diarization: Usage Example](#usage-example) |
| [Calculate Performance Metrics](#calculate-performance-metrics) |
| [Calculate Performance Metrics: Installation and Setup](#installation-and-setup-1) |
| [Calculate Performance Metrics: Usage Example](#usage-example-1) |
| [Citations](#citations) |

## Installation and Setup

### Hugging Face Setup
If you are not already logged into the Hugging Face CLI from your machine, you will need to provide a user token. To create and access your user token, follow the steps below:
1. Go to [Hugging Face's user token page](https://huggingface.co/settings/tokens).
2. Create a new token.
3. Select the token type **Read**, enter a token name, and then create the token.
4. Copy the token into a text file.
5. Copy them contents of [templates/read_token_template.py](templates/read_token_template.py) into a new file `scripts/speaker_diarization/read_token.py`.
6. Edit the `token_loc` variable in the `read_token.py` script to point to the text file holding your token.

### Without Docker
Check your Python version:
```sh
python --version
```
Note that one of the packages, [sentencepiece](https://github.com/google/sentencepiece), does not support Python 3.13.1 yet. See [Anaconda](https://www.anaconda.com/download/success) as an option to switch between Python versions. This repository has been tested with Python 3.9.6 and Python 3.12.11

Install requirements for Python 3.9.6:
```sh
pip install -r py3-9-6_requirements.txt
```

Install requirements for Python 3.12.11:
```sh
pip install -r py3-12-11_requirements.txt
```

Note: you may use one of the pip install commands described above even if you are working with a different Python version, but you may need to adjust the requirements.txt file to fit any dependencies specific to that Python version.

## With Docker
[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the `build_docker.sh` and `run_docker.sh` scripts. These .sh scripts were tested on Linux (CentOS 7).

```sh
./build_docker.sh
./run_docker.sh
```

The Docker commands included in the .sh scripts are:
```sh
docker build -t $docker_name .
## build the container image under the name 'docker_name' based on the Dockerfile specifications
docker run -v $(pwd):/scripts -it --rm --gpus all --name $container_name $docker_name bash
## run the built container image ('docker_name') under the container name ('container_name')
## mounts the current working directory $(pwd) as a volume to /scripts within the container
```

Please see Docker's documentation for more information ([docker build](https://docs.docker.com/build/), [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/), [docker run](https://docs.docker.com/reference/cli/docker/container/run/)).

## Jupyter Notebook Examples

Please run [jupyter notebook](https://docs.jupyter.org/en/latest/running.html) and see [example_usages.ipynb](example_usages.ipynb) for an interactive set of examples. Also, see the usage example sections below.

## Usage Example
See [main.main()](main.py) for usage examples. The `prep_and_diarize()` function takes in a Hugging Face token and a list of audio filepaths to diarize. For each file passed into `prep_and_diarize()`, there will be a resulting RTTM file and CSV.

```python
from pyannote_diarize import prep_and_diarize
from scripts.speaker_diarization.read_token import read_token
audio_list = [YOUR LIST]
kwargs = {'num_speakers': 2}
prep_and_diarize(read_token(), audio_list, **kwargs)
```

Or to run our preset example, you could run:
```python
from main import main
main()
```

This would output six files: a CSV containing speaker turns with timestamps and a RTTM file for each of the sample audio input files.

### Arguments
The `pyannote_diarize.prep_and_diarize()`  function takes in a Hugging Face token, a list of audio files, and a set of keyword arguments. The documentation of the full set of keyword arguments can be found [here](https://github.com/pyannote/pyannote-audio/blob/main/pyannote/audio/pipelines/speaker_diarization.py#L427).

| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| num_speakers | int | The number of speakers to diarize the file by. | 2 |

### Sample Input and Output Files
The sample hierarchy shows files created by running `main()` using Docker. Each of the input audio files results in a CSV and RTTM file with the same base name.

```
sample_files
├── short_wav
│   ├── first_minute_Sample_HV_Clip.csv
│   ├── first_minute_Sample_HV_Clip.rttm
│   ├── first_minute_Sample_HV_Clip.wav
│   ├── first_ten_Sample_HV_Clip.csv
│   ├── first_ten_Sample_HV_Clip.rttm
│   ├── first_ten_Sample_HV_Clip.wav
│   ├── Sample_HV_Clip.csv
│   ├── Sample_HV_Clip.rttm
│   ├── Sample_HV_Clip.wav
```

#### CSV Columns
The CSV file summarizes the information found in the Rich Transcription Time Marked (RTTM) files. 

| Fieldname | Description |
|---|---|
| turn_onset | Timestamp of the start of the speaker turn. |
| turn_end | Timestamp of the end of the speaker turn. |
| turn_duration | Length of the speaker turn. |
| speaker_name | Assigned speaker name. |

# Calculate Performance Metrics
This script evaluates the performance of a speaker diarization tool by comparing a pre-labeled, ground truth RTTM file against a hypothesis RTTM file generated by the speaker diarization tool.

## Installation and Setup

Install requirements:
```sh
pip install pyannote.metrics pyannote.database
```

## Jupyter Notebook Examples
Please run [jupyter notebook](https://docs.jupyter.org/en/latest/running.html) and see [accuracy_evaluation_example.ipynb](accuracy_evaluation_example.ipynb) for an interactive set of examples. Also, see the usage example sections below.

## Usage Example
See speaker_diarization_evaluation.main() for usage examples. The process_accuracy() function takes in a ground truth RTTM file, a hypothesis RTTM file, and the optional KWARG verbose (bool, default is False). The evaluation script results in a JSON and LOG file summarizing the two types of error calculated:
- [DiarizationErrorRate](https://pyannote.github.io/pyannote-metrics/_modules/pyannote/metrics/diarization.html#DiarizationErrorRate)
- [JaccardErrorRate](https://pyannote.github.io/pyannote-metrics/_modules/pyannote/metrics/diarization.html#JaccardErrorRate).

For example, you could run:
```python
from speaker_diarization_evaluate import process_accuracy
process_kwargs = {
        "verbose": "True"
    }
process_accuracy("FILEPATH TO YOUR GT RTTM", "FILEPATH TO YOUR HYP RTTM", **process_kwargs)
```

Or to run our preset example, you could run:
```python
from speaker_diarization_evaluate import main
main()
```

This will output two files: 
- A JSON containing the Diarization Error Rate and the Jaccard Error Rate
- A LOG file a more detailed breakdown of the result from each error rate calculation.

### Arguments
| Keyword Argument | Type | Description | Default Value |
|---|---|---|---|
| verbose | bool | Prints script information to the terminal while running. | False |

### Sample Input and Output Files 
```
ground_truth_files
├── first_minute_Sample_HV_Clip_ground_truth.rttm
├── first_ten_Sample_HV_Clip_ground_truth.rttm
|
sample_files
├── short_wav
│   ├── first_minute_Sample_HV_Clip.rttm
│   ├── first_ten_Sample_HV_Clip.rttm
|
evaluation_results
├── (timestamp)
│   ├── evaluation.json
│   ├── evaluation.log
|
```

### Alternative Performance Metric Calculation: VoxConverse

If you wish to run the performance metrics on a larger dataset, you may use any dataset containing ground truth and hypothesis RTTM files. One possibility is to use [VoxConverse v0.3 dataset](https://github.com/joonson/voxconverse) via [Hugging Face](https://huggingface.co/datasets/diarizers-community/voxconverse). 

## Citations
```bibtex
@inproceedings{Plaquet23,
  author={Alexis Plaquet and Hervé Bredin},
  title={{Powerset multi-class cross entropy loss for neural speaker diarization}},
  year=2023,
  booktitle={Proc. INTERSPEECH 2023},
}
@inproceedings{Bredin23,
  author={Hervé Bredin},
  title={{pyannote.audio 2.1 speaker diarization pipeline: principle, benchmark, and recipe}},
  year=2023,
  booktitle={Proc. INTERSPEECH 2023},
}
@article{chung2020spot,
  title={Spot the conversation: speaker diarisation in the wild},
  author={Chung, Joon Son and Huh, Jaesung and Nagrani, Arsha and Afouras, Triantafyllos and Zisserman, Andrew},
  booktitle={Interspeech},
  year={2020}
}
```
