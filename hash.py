
from hashlib import sha256
from base64 import b64encode

def hash(s):
    return b64encode(sha256(s.encode("utf-8")).digest()).decode("utf-8")


