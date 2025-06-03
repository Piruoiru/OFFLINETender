import hashlib

def generate_hash(url: str) -> str:
    """
    Generate a SHA-256 hash for the contents of a file.

    :param file_path: Path to the file to hash.
    :return: SHA-256 hash of the file contents as a hexadecimal string.
    """
    return hashlib.sha256(url.encode("utf-8")).hexdigest()