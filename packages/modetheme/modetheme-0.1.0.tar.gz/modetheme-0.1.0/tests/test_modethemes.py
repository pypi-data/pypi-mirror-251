import unittest
from modethemes.itermode import *
from modethemes.sorthemes import *

class TestModeThemes(unittest.TestCase):
  def test_asc(self):
    self.assertEqual(asc([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]), [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9])
  def test_desc(self):
    self.assertEqual(desc([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]), [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1])

if __name__ == "__main__":
  unittest.main()