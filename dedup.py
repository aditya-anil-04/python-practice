import hashlib
import os
from pathlib import Path

class DuplicateRemover:
    def __init__(self, folder):
        self.folder = Path(folder)
        self.seen = {}

    def hash_file(self, path):
        h = hashlib.sha256()
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def scan_and_remove(self):
        for root, _, files in os.walk(self.folder):
            for file in files:
                filepath = Path(root) / file
                file_hash = self.hash_file(filepath)
                if file_hash in self.seen:
                    filepath.unlink()
                else:
                    self.seen[file_hash] = filepath

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python dedup.py <folder>")
        sys.exit(1)
    remover = DuplicateRemover(sys.argv[1])
    remover.scan_and_remove()
