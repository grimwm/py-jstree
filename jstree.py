import dictobj
import collections
import os

class Node(dictobj.DictionaryObject):
  """
  This class exists as a helper to the JSTree.  Its "jsonData" method can
  generate sub-tree JSON without putting the logic directly into the JSTree.

  This data structure is only semi-immutable.  The JSTree uses a directly
  iterative (i.e. no stack is managed) builder pattern to construct a
  tree out of paths.  Therefore, the children are not known in advance, and
  we have to keep the children attribute mutable.
  """
  def __init__(self, data, **kwargs):
    """
    kwargs allows users to pass arbitrary information into a Node that
    will later be output in jsonData().  It allows for more advanced
    configuration than the default path handling that JSTree currently allows.
    For example, users may want to pass "attr" or "metadata" or some other
    valid jsTree options.
    
    Example:
      >>> import jstree
      >>> node = jstree.Node('a')
      >>> print node
      Node({'data': 'a', 'children': MutableDictionaryObject({})})

      >>> import jstree
      >>> node = jstree.Node('a', attr={'id':23})
      >>> print node
      Node({'data': 'a', 'children': MutableDictionaryObject({}), 'attr': DictionaryObject({'id': 23})})
    """
    super(Node, self).__init__()

    children = kwargs.get('children', {})
    if len(filter(lambda key: not isinstance(children[key], Node), children)):
      raise TypeError("One or more children were not instances of '%s'" % Node.__name__)
    if 'children' in kwargs:
      del kwargs['children']
    self._items['children'] = dictobj.MutableDictionaryObject(children)
      
    self._items.update(dictobj.DictionaryObject(**kwargs))
    self._items['data'] = data

  def jsonData(self):
    children = [self.children[k].jsonData() for k in sorted(self.children)]
    if len(children):
      return {'data':self.data, 'children':children}
    else:
      return {'data':self.data}
    
class JSTree(dictobj.DictionaryObject):
  """
  An immutable dictionary-like object that converts a list of "paths"
  into a tree structure suitable for jQuery's jsTree.
  """
  def __init__(self, paths=None, tree=None):
    """
    Example (basic usage):
      >>> import jstree
      >>> paths = ["editor/2012-07/31/.classpath", "editor/2012-07/31/.project"]
      >>> t1 = jstree.JSTree(paths)
      >>> t2 = jstree.JSTree(tree=t1)
      >>> print t1 == t2
      True
    """
    if paths is None and tree is None:
      raise TypeError("Either 'paths' or 'tree' must be passed to '%s'" % JSTree.__name__)
    if paths is not None and tree is not None:
      raise TypeError("Only one of 'paths' or 'tree' may be passed to '%s'" % JSTree.__name__)

    if paths is not None:
      """
      Take a list of paths and put them into a tree.  Paths with the same prefix should
      be at the same level in the tree.
      """
      super(JSTree, self).__init__()
      
      root = Node('')
      for path in sorted(set(paths)):
        curr = root
        for subpath in path.split(os.path.sep):
          if subpath not in curr.children:
            curr.children[subpath] = Node(subpath)
          curr = curr.children[subpath]
      self._items['_root'] = root

    if tree is not None:
      if isinstance(tree, JSTree):
        """
        Since our internal data structure is quite specific,
        only allow initialization by other JSTrees.
        """
        # super(JSTree, self).__init__(tree)
        super(JSTree, self).__init__()
        self._items['_root'] = dictobj.DictionaryObject(tree._root)
      else:
        raise TypeError("'%tree' is not an instance of '%s'" % (JSTree.__name__))

  def pretty(self, root=None, depth=0, spacing=2):
    """
    Create a "pretty print" represenation of the tree with customized indentation at each
    level of the tree.
    
    Example:
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
    Returns a copy of the internal tree in a JSON-friendly format,
    ready for consumption by jsTree.  The data is represented as a
    list of dictionaries, each of which are our internal nodes.

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
    >>> d[0]
    {'data': 'editor', 'children': [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath'}, {'data': '.project'}]}]}]}
    >>> d[0]['children']
    [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath'}, {'data': '.project'}]}]}]
    >>> d[0]['children'][0]
    {'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath'}, {'data': '.project'}]}]}
    >>> d[0]['children'][0]['children']
    [{'data': '31', 'children': [{'data': '.classpath'}, {'data': '.project'}]}]
    >>> d[0]['children'][0]['children'][0]
    {'data': '31', 'children': [{'data': '.classpath'}, {'data': '.project'}]}
    >>> d[0]['children'][0]['children'][0]['children']
    [{'data': '.classpath'}, {'data': '.project'}]
    >>> d[0]['children'][0]['children'][0]['children'][0]
    {'data': '.classpath'}
    >>> d[0]['children'][0]['children'][0]['children'][1]
    {'data': '.project'}
    """
    return [self._root.children[k].jsonData() for k in sorted(self._root.children)]
