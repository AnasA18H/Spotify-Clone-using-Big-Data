# load_data.py
import pandas as pd


def load_metadata(file_path):
    metadata = pd.read_csv(file_path)
    return metadata


def load_audio_features(directory):
    # Code to load audio features
    pass
