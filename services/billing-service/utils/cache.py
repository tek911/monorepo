"""
Cache utilities using pickle
VULNERABILITY: Insecure deserialization
"""

import pickle
import base64
import os
import hashlib


class PickleCache:
    """
    VULNERABILITY: Pickle-based cache (RCE via deserialization)
    CWE-502: Deserialization of Untrusted Data
    """

    def __init__(self, cache_dir: str = "/tmp/billing_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _get_key_path(self, key: str) -> str:
        # VULNERABILITY: Path traversal possible
        return os.path.join(self.cache_dir, f"{key}.pickle")

    def set(self, key: str, value) -> None:
        """Store value using pickle (VULNERABLE)"""
        path = self._get_key_path(key)
        with open(path, 'wb') as f:
            # VULNERABILITY: Pickle serialization
            pickle.dump(value, f)

    def get(self, key: str):
        """Retrieve value using pickle (VULNERABLE)"""
        path = self._get_key_path(key)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                # VULNERABILITY: Pickle deserialization RCE
                return pickle.load(f)
        return None

    def get_from_string(self, data: str):
        """
        Deserialize from base64 string (VULNERABLE)
        Attack payload can be created with:
        import pickle, base64, os
        class Exploit:
            def __reduce__(self):
                return (os.system, ('id',))
        base64.b64encode(pickle.dumps(Exploit()))
        """
        # VULNERABILITY: Deserializing user-provided data
        return pickle.loads(base64.b64decode(data))

    def set_to_string(self, value) -> str:
        """Serialize to base64 string"""
        return base64.b64encode(pickle.dumps(value)).decode()


# Global cache instance
cache = PickleCache()


def hash_key(key: str) -> str:
    """
    VULNERABILITY: MD5 for hashing
    """
    return hashlib.md5(key.encode()).hexdigest()
