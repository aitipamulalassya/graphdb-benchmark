from pathlib import Path
from urllib.request import urlretrieve


# Project root
BASE_DIR = Path(__file__).resolve().parent

# Raw dataset directory
RAW_DIR = BASE_DIR / "raw"

# Create raw directory if it does not exist
RAW_DIR.mkdir(parents=True, exist_ok=True)


# SNAP Wiki-Vote dataset
DATASET_URL = "https://snap.stanford.edu/data/wiki-Vote.txt.gz"

# Where we will save it
DATASET_FILE = RAW_DIR / "wiki-Vote.txt.gz"


def download_dataset():

    if DATASET_FILE.exists():

        print("Dataset already exists.")
        print(f"Location: {DATASET_FILE}")

        return

    print("Downloading Wiki-Vote dataset...")
    print(f"URL: {DATASET_URL}")

    urlretrieve(
        DATASET_URL,
        DATASET_FILE
    )

    print()
    print("Download completed.")
    print(f"Saved to: {DATASET_FILE}")


if __name__ == "__main__":

    download_dataset()