from pymongo import MongoClient
import matplotlib.pyplot as plt
import os

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["fma_dataset"]
collection = db["audio_features"]

# Retrieve data from MongoDB
cursor = collection.find()

# Initialize lists to store extracted features
mfcc_list = []
spectral_centroid_list = []
zero_crossing_rate_list = []

# Iterate over the cursor and extract features
for document in cursor:
    mfcc_list.append(document["mfcc"])
    spectral_centroid_list.append(document["spectral_centroid"])
    zero_crossing_rate_list.append(document["zero_crossing_rate"])

# Directory to save plots
plots_dir = "plots"
os.makedirs(plots_dir, exist_ok=True)

# Plotting MFCC
plt.figure(figsize=(10, 6))
plt.plot(mfcc_list[0])  # Plotting MFCC of the first audio file as an example
plt.title("MFCC")
plt.xlabel("Frame")
plt.ylabel("Value")
plt.grid()
plt.savefig(os.path.join(plots_dir, "mfcc_plot.png"))
plt.close()

# Plotting Spectral Centroid
plt.figure(figsize=(10, 6))
plt.plot(
    spectral_centroid_list[0]
)  # Plotting spectral centroid of the first audio file as an example
plt.title("Spectral Centroid")
plt.xlabel("Frame")
plt.ylabel("Value")
plt.grid()
plt.savefig(os.path.join(plots_dir, "spectral_centroid_plot.png"))
plt.close()

# Plotting Zero-Crossing Rate
plt.figure(figsize=(10, 6))
plt.plot(
    zero_crossing_rate_list[0]
)  # Plotting zero-crossing rate of the first audio file as an example
plt.title("Zero-Crossing Rate")
plt.xlabel("Frame")
plt.ylabel("Value")
plt.grid()
plt.savefig(os.path.join(plots_dir, "zero_crossing_rate_plot.png"))
plt.close()
