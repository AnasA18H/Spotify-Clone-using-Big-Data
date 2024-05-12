import os
import librosa
from pymongo import MongoClient
from tqdm import tqdm  # For progress bar
import logging

log_file_path = "audio_processing.log"

# Open the log file in write mode, which truncates the file
with open(log_file_path, "w"):
    pass  # This is a no-op, but it ensures the file is truncated
# Setup logging
logging.basicConfig(filename=log_file_path, level=logging.ERROR)

# Initialize counters
successful_executions = 0
failed_executions = 0


def extract_audio_features(audio_file):
    """
    Extracts audio features (MFCC, spectral centroid, zero-crossing rate) from an audio file.

    Parameters:
        audio_file (str): Path to the audio file.

    Returns:
        tuple: Tuple containing MFCC, spectral centroid, and zero-crossing rate features.
               Returns None if an error occurs during feature extraction.
    """
    try:
        y, sr = librosa.load(audio_file, duration=30)  # Load audio file
        mfcc = librosa.feature.mfcc(y=y, sr=sr)  # Extract MFCC features
        spectral_centroid = librosa.feature.spectral_centroid(
            y=y, sr=sr
        )  # Extract spectral centroid
        zero_crossing_rate = librosa.feature.zero_crossing_rate(
            y
        )  # Extract zero-crossing rate
        return mfcc, spectral_centroid, zero_crossing_rate
    except Exception as e:
        logging.error(f"Error extracting features from {audio_file}: {e}")
        failed_executions += 1
        return None


def insert_data_bulk(collection, data):
    """
    Inserts data into MongoDB collection in bulk.

    Parameters:
        collection: MongoDB collection to insert data into.
        data (list): List of data to be inserted.

    Returns:
        None
    """
    try:
        collection.insert_many(data)
    except Exception as e:
        logging.error(f"Error inserting data into MongoDB: {e}")
        failed_executions += 1


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fma_dataset"]
collection = db["audio_features"]

# Path to the directory containing audio files
audio_dir = "/home/anas/Spotify_i22-1987/data/sample_Small"

# Initialize variables
batch_size = 1000  # Number of files to process in each batch
data_batch = []

# Iterate over subdirectories within the audio directory
print("\n\n")
for subdir in os.listdir(audio_dir):
    subdir_path = os.path.join(audio_dir, subdir)
    if os.path.isdir(subdir_path):
        # Iterate over audio files in each subdirectory
        print("\n")
        for audio_file in tqdm(os.listdir(subdir_path), desc=f"Processing {subdir}: "):
            if audio_file.endswith(".mp3"):  # Assuming audio files are in MP3 format
                audio_file_path = os.path.join(subdir_path, audio_file)
                try:
                    features = extract_audio_features(
                        audio_file_path
                    )  # Extract features
                    if features is not None:
                        data = {
                            "file_name": os.path.basename(
                                audio_file
                            ),  # Include the file name
                            "track_id": os.path.splitext(audio_file)[0],
                            "mfcc": features[0].tolist(),
                            "spectral_centroid": features[1].tolist(),
                            "zero_crossing_rate": features[2].tolist(),
                        }

                        data_batch.append(data)
                        successful_executions += 1
                        # Insert data into MongoDB in batches to save memory
                        if len(data_batch) == batch_size:
                            insert_data_bulk(collection, data_batch)
                            data_batch = []
                except Exception as e:
                    logging.error(f"Error processing {audio_file}: {e}")
                    failed_executions += 1

# Insert any remaining data into MongoDB
if data_batch:
    insert_data_bulk(collection, data_batch)

# Output the results
print(f"Number of files properly executed: {successful_executions}")
print(f"Number of files failed: {failed_executions}")
