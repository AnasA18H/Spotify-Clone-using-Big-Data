# feature_extraction.py
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def normalize_features(features):
    scaler = StandardScaler()
    normalized_features = scaler.fit_transform(features)
    return normalized_features


def reduce_dimensionality(features, n_components):
    pca = PCA(n_components=n_components)
    reduced_features = pca.fit_transform(features)
    return reduced_features
