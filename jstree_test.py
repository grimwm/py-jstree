import jstree

import unittest
import doctest

class TestJSTree(unittest.TestCase):
  def setUp(self):
    self.tree = jstree.JSTree([jstree.Path("editor/2012-07/31/.classpath", 1), jstree.Path("editor/2012-07/31/.project", 2)])

  def test_pretty(self):
    output = '/\n  editor/\n    2012-07/\n      31/\n        .classpath\n        .project'
    self.tree.pretty()
    self.assertEqual(output, self.tree.pretty())

def load_tests(loader, tests, pattern):
  suite = unittest.TestSuite()
  suite.addTests(tests)
  suite.addTest(doctest.DocTestSuite(jstree))
  return suite

if '__main__' == __name__:
  unittest.main()
