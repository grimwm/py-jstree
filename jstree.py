import json
import collections
import os

Node = collections.namedtuple('Node', ['name', 'children'])

class JSTree(object):
  def __init__(self, paths):
    """
    >>> import jstree
    >>> paths = ["editor/2012-07/31/.classpath", "editor/2012-07/31/.project"]
    >>> print jstree.JSTree(paths)
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

  def _treeStr(self, root, depth):
    fmt = "%s%s/" if root.children else "%s%s"
    s = fmt % (" "*depth*2, root.name)
    for child in root.children:
      child = root.children[child]
      s += "\n%s" % self._treeStr(child, depth+1)
    return s
  
  def __str__(self):
    return self._treeStr(self._root, 0)
