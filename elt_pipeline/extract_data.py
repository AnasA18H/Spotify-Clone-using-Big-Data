import os
import zipfile


def extract_data(zip_file_path, extract_to):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def extract_audio_files(zip_file_path, extract_to):
    extract_data(zip_file_path, extract_to)


# Example usage
if __name__ == "__main__":
    extract_audio_files("fma_large.zip", "fma_large")
    extract_data("fma_metadata.zip", "fma_metadata")
