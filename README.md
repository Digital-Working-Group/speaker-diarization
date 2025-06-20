# Speaker Diarization

This repo evalutates the [pyannote-audio](https://github.com/pyannote/pyannote-audio) diarization tool on an audio file.

| Table of Contents |
|---|
| [Installation and Setup](#installation-and-setup)|
| [Usage Example](#usage-example) |
| [Citations](#citations) |

## Installation and Setup

###  Hugging Face Setup
If you are not already logged into the Hugging Face CLI from your machine, you will need to provide a user token. To create and access your user token, follow the steps below:
1. Go to [Hugging Face's user token page](https://huggingface.co/settings/tokens).
2. Create a new token.
3. Select the token type **Read**, enter a token name, and then create the token.
4. Copy the token into a text file.
5. Create a new file called `scripts/pii-masking-300k/read_token.py` and copy the contents of `scripts/pii-masking-300k/read_token_template.py` into it.
6. Copy them contents of [templates/read_token_template.py](templates/read_token_template.py) into a new file `read_token.py`.
6. Edit the `token_loc` variable in the `read_token.py` script to point to the text file holding your token.

### Without Docker
Check your Python version:
```sh
python --version
```
Note that one of the packages, [sentencepiece](https://github.com/google/sentencepiece), does not support Python3.13.1 yet. If you See [Anaconda](https://www.anaconda.com/download/success) as an option to switch between Python versions.

Install requirements:
```sh
pip install -r python3-13-1_requirements.txt
```

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

## Usage Example
See [main.main()](main.py) for usage examples. The `prep_and_diarize()` function takes in a Hugging Face token and a list of audio filepaths to diarize. For each file passed into `prep_and_diarize()`, there will be a resulting RTTM file and CSV.

```python
from pyannote_diarize import prep_and_diarize
from read_token import read_token
audio_list = [YOUR LIST]
prep_and_diarize(read_token(), audio_list)
```


Or to run our preset example, you could run:
```python
from main import main
main()
```

This would output four files: a CSV continaing and a RTTM file containing for each of the sample audio input files.

### Sample Input and Output Files
The sample hierarchy shows files created by running `main()` using Docker. Each of the input audio files results in a CSV and RTTM file with the same base name.

```
input_audio
├── short_wav
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
```