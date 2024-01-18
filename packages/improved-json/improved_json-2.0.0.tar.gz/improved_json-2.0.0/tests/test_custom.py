from pathlib import Path
import unittest

from improved_json.code import PATH_PREFIX, BYTES_PREFIX_TXT, BYTES_PREFIX_ENC
import improved_json


class TestDecode(unittest.TestCase):
    """
    Test improved_json's json encoding/decoding of types not in normal json
    """

    def _test_both(self, o, s: str) -> None:
        s = f'"{s}"'
        self.assertEqual(improved_json.dumps(o), s)
        self.assertEqual(improved_json.loads(s), o)

    def test_path(self):
        self._test_both(Path("/a/b/c"), f"{PATH_PREFIX}/a/b/c")

    def test_bytes_txt(self):
        self._test_both(b"simple", f"{BYTES_PREFIX_TXT}simple")

    def test_bytes_enc(self):
        self._test_both(b"\x81", f"{BYTES_PREFIX_ENC}JH")


if __name__ == "__main__":
    unittest.main()
