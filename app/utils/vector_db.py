import faiss
import numpy as np
import os
import hashlib
import yaml
from app.utils.data_extraction import extract_text_segments
from app.utils.openai_client import get_embedding

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

DIM = config['vector_store']['dimension']
INDEX_PATH = config['vector_store']['index_path']
HASH_PATH = config['vector_store']['file_hash_path']

index = None
_segments_global = []

def update_index(file_path):
    global index, _segments_global
    file_hash = _compute_file_hash(file_path)
    if os.path.exists(HASH_PATH):
        with open(HASH_PATH, "r") as f:
            saved_hash = f.read().strip()
        if saved_hash == file_hash:
            if os.path.exists(INDEX_PATH):
                index = faiss.read_index(INDEX_PATH)
            return False
    segments = extract_text_segments(file_path)
    embeddings = []
    for segment in segments:
        emb = get_embedding(segment)
        embeddings.append(emb)
    embeddings = np.array(embeddings).astype('float32')
    index = faiss.IndexFlatL2(DIM)
    index.add(embeddings)
    faiss.write_index(index, INDEX_PATH)
    with open(HASH_PATH, "w") as f:
        f.write(file_hash)
    _segments_global = segments
    return True

def search(query, k=3):
    global index, _segments_global
    if index is None:
        return []
    query_emb = np.array([get_embedding(query)]).astype('float32')
    distances, indices = index.search(query_emb, k)
    results = []
    for idx in indices[0]:
        if idx < len(_segments_global):
            results.append(_segments_global[idx])
    return results

def _compute_file_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
