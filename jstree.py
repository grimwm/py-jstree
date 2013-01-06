import json
import collections
import os

Node = collections.namedtuple('Node', ['data', 'children'])

class JSTree(object):
  def __init__(self, paths):
    """
    >>> import jstree
    >>> paths = ["editor/2012-07/31/.classpath", "editor/2012-07/31/.project"]
    >>> print jstree.JSTree(paths).pretty()
    /
      editor/
        2012-07/
          31/
            .classpath
            .project
    """
    root = Node('', {})
    for path in paths:
      curr = root
      for subpath in path.split(os.path.sep):
        if subpath not in curr.children:
          curr.children[subpath] = Node(subpath, {})
        curr = curr.children[subpath]
    self._root = root

  def pretty(self, root=None, depth=0, spacing=2):
    if root is None:
      root = self._root
    fmt = "%s%s/" if root.children else "%s%s"
    s = fmt % (" "*depth*spacing, root.data)
    for child in root.children:
      child = root.children[child]
      s += "\n%s" % self.pretty(child, depth+1, spacing)
    return s
  
  def __str__(self):
    return str(self._root)
