import os

def extract_text_segments(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        segments = [line.strip() for line in lines if line.strip()]
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        segments = [seg.strip() for seg in content.split("\n") if seg.strip()]
    return segments
