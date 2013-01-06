from dictobj import *

import unittest
import doctest

class TestJSTree(unittest.TestCase):
  def setUp(self):
    pass

def load_tests(loader, tests, pattern):
  import jstree
  suite = unittest.TestSuite()
  suite.addTests(tests)
  suite.addTest(doctest.DocTestSuite(jstree))
  return suite

if '__main__' == __name__:
  unittest.main()
