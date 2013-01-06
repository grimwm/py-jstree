import dictobj
import collections
import os

class JSTree(object):
  @staticmethod
  def _node(data, children={}):
    d = {'data':data}
    if children is not None:
      d['children'] = children
    return dictobj.MutableDictionaryObject(d)
  
  def __init__(self, paths=None, tree=None):
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
    if paths is None and tree is None:
      raise TypeError("Either 'paths' or 'tree' must be passed to '%s'" % JSTree.__name__)
    if paths is not None and tree is not None:
      raise TypeError("Only one of 'paths' or 'tree' may be passed to '%s'" % JSTree.__name__)

    if paths is not None:
      root = JSTree._node('')
      for path in paths:
        curr = root
        for subpath in path.split(os.path.sep):
          if subpath not in curr.children:
            curr.children[subpath] = JSTree._node(subpath)
          curr = curr.children[subpath]
      self._root = root

    if tree is not None:
      if isinstance(tree, JSTree):
        self._root = dictobj.MutableDictionaryObject(tree._root)
      else:
        raise TypeError("'%tree' is not an instance of '%s'" % (JSTree.__name__))

  def pretty(self, root=None, depth=0, spacing=2):
    """
    Create a "pretty print" represenation of the tree.
    """
    if root is None:
      root = self._root
    fmt = "%s%s/" if root.children else "%s%s"
    s = fmt % (" "*depth*spacing, root.data)
    for child in root.children:
      child = root.children[child]
      s += "\n%s" % self.pretty(child, depth+1, spacing)
    return s

  @property
  def data(self):
    return self._root

  def __str__(self):
    return str(self.asdict())
