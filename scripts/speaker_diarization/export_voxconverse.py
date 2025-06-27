"""export_voxconverse.py"""
import subprocess
import requests
import zipfile
from pathlib import Path


def get_voxconverse_data(dev=True, extract_dir=Path(__file__).parent / "voxconverse_data"):
    """Load spearker-diarization dataset from VoxConverse v0.3"""
    extract_dir.mkdir(parents=True, exist_ok=True)
    url = (
        "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip"
        if dev else
        "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip"
    )
    zip_path = extract_dir / ("dev.zip" if dev else "test.zip")

    if not zip_path.exists():
        print("Downloading dataset...")
        response = requests.get(url)
        zip_path.write_bytes(response.content)

    wav_dir = extract_dir / ("dev" if dev else "test")
    if not wav_dir.exists():
        print("Extracting zip...")
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(wav_dir)

def get_voxconverse_labels(dst=Path(__file__).parent / "voxconverse_labels"):
    """Clone VoxConverse repo to get labels"""
    if isinstance(dst, str):
        dst = Path(dst)
    destination = dst.resolve()
    if destination.exists():
        print(f"Directory {destination} already exists. Skipping download.")
        return
    
    url = "https://github.com/joonson/voxconverse.git"
    subprocess.run([
        "git", "clone", "--depth=1", url, str(destination)
    ], check=True)
    print(f"Cloned VoxConverse labels to {destination}")


if __name__ == "__main__":
    get_voxconverse_data()
    get_voxconverse_labels()
