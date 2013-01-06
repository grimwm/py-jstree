import dictobj
import collections
import os

class Node(dictobj.MutableDictionaryObject):
  """
  This class mainly exists for its "json" method so it can help
  generate JSON without putting a lot of logic in the JSTree for it.
  """
  def __init__(self, data):
    super(Node, self).__init__()
    self._items['data'] = data
    self._items['children'] = dictobj.MutableDictionaryObject()

  def jsonData(self):
    children = [self.children[k].jsonData() for k in sorted(self.children)]
    return {'data':self.data, 'children':children}
  
class JSTree(dictobj.MutableDictionaryObject):
  def __init__(self, paths=None, tree=None):
    """
    Examples:
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
      super(JSTree, self).__init__()
      
      root = Node('')
      for path in paths:
        curr = root
        for subpath in path.split(os.path.sep):
          if subpath not in curr.children:
            curr.children[subpath] = Node(subpath)
          curr = curr.children[subpath]
      self._items['_root'] = root

    if tree is not None:
      super(JSTree, self).__init__(tree)

    # if tree is not None:
    #   if isinstance(tree, JSTree):
    #     self._root = dictobj.MutableDictionaryObject(tree._root)
    #   else:
    #     raise TypeError("'%tree' is not an instance of '%s'" % (JSTree.__name__))

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

  def jsonData(self):
    """
    Returns a copy of the internal tree with the root replaced
    by a new type of "data" node that is represented as a list
    of dictionaries, each of which are our internal nodes.

    The logic behind this data-representation decision is due
    to a funny behavior in the jQuery jsTree requiring that the
    top-level "data" node be a list, while all the items
    underneath is may be dictionaries containing "data" as a string
    and "children" as a list of yet more dictionaries of the
    same recursive structure as the top-level "data" node.

    Examples:
    >>> import jstree
    >>> paths = ["editor/2012-07/31/.classpath", "editor/2012-07/31/.project"]
    >>> t = jstree.JSTree(paths)
    >>> d = t.jsonData()
    >>> d['data']
    [{'data': 'editor', 'children': [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}]}]}]
    >>> d['data'][0]
    {'data': 'editor', 'children': [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}]}]}
    >>> d['data'][0]['children']
    [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}]}]
    >>> d['data'][0]['children'][0]
    {'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}]}
    >>> d['data'][0]['children'][0]['children']
    [{'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}]
    >>> d['data'][0]['children'][0]['children'][0]
    {'data': '31', 'children': [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]}
    >>> d['data'][0]['children'][0]['children'][0]['children']
    [{'data': '.classpath', 'children': []}, {'data': '.project', 'children': []}]
    >>> d['data'][0]['children'][0]['children'][0]['children'][0]
    {'data': '.classpath', 'children': []}
    >>> d['data'][0]['children'][0]['children'][0]['children'][1]
    {'data': '.project', 'children': []}
    """
    data = [self._root.children[k].jsonData() for k in sorted(self._root.children)]
    return {'data':data}
