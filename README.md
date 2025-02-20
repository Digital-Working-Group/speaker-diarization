# Speaker Diarization
This repository contains example workflows, READMEs, sample data, and [Docker](https://www.docker.com/) files that facilitate the usage of various open-source voice feature extraction packages, tools, datasets, and models for speaker diarization.

It is a part of a larger [toolkit](https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/) was developed to support scientific research surrounding investigations of relationships between brain aging and voice features, although the extraction of voice features does have wider applicability. We invite others to please offer their questions, ideas, feedback, and improvements on this repository.

## Overview
| Name | Description |
| - |-|
| **diarization-benchmark** | Evaluate several speaker diarization tools on the [VoxConverse](https://github.com/joonson/voxconverse) dataset.
| **diarization-pyannote-audio** | Evaluate the [pyannote-audio](https://github.com/pyannote/pyannote-audio) diarization tool on an audio file.
| **diarization-whisperx** | Evaluate ASR via [whisperx](https://github.com/m-bain/whisperX) and optionally align speaker diarization via [pyannote-audio](https://github.com/pyannote/pyannote-audio) on an audio file.