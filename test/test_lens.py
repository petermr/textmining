import unittest
import json
import re
from pathlib import Path

from patent.lens import Lens

TEST_DIR = Path(__file__).parent
RESOURCE_DIR = Path(TEST_DIR, "resources")

class TestLens(unittest.TestCase):


    def test_read_lens(self):
        print(f"parent {TEST_DIR}")

        json_path = Path(RESOURCE_DIR, "p_1_100.json")

        lens = Lens()
        lens.read_write(json_path)

