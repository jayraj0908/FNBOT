import os
from typing import Optional, Dict

CACHE_DIR = "files/reference_cache"
_in_memory_cache: Dict[str, str] = {}

os.makedirs(CACHE_DIR, exist_ok=True)

def set_cache(name: str, file_path: str):
    """Cache a reference file by name (in-memory and disk)."""
    _in_memory_cache[name] = file_path
    # Copy to disk cache
    dest = os.path.join(CACHE_DIR, name)
    if os.path.abspath(file_path) != os.path.abspath(dest):
        with open(file_path, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())

def get_cache(name: str) -> Optional[str]:
    """Get cached file path by name (check in-memory, then disk)."""
    if name in _in_memory_cache:
        return _in_memory_cache[name]
    disk_path = os.path.join(CACHE_DIR, name)
    if os.path.exists(disk_path):
        _in_memory_cache[name] = disk_path
        return disk_path
    return None

def list_cache() -> Dict[str, str]:
    """List all cached reference files (name: path)."""
    files = {}
    for fname in os.listdir(CACHE_DIR):
        files[fname] = os.path.join(CACHE_DIR, fname)
    files.update(_in_memory_cache)
    return files 