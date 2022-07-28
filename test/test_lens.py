import unittest
import json
import re
from pathlib import Path

from patent.lens import Lens

class TestLens(unittest.TestCase):

    test_dir = Path(__file__).parent

    def test_read_lens(self):
        print(f"parent {self.test_dir}")
        json_path = Path(self.test_dir, "resources", "p_1_100.json")

        lens = Lens()
        lens.read_write(json_path)
        # assert False

