py-jstree
=========

An introduction will be proposed later.

Installation
------------

If you have Python installed and wish to get the package directly from the
[Python Package Index](http://pypi.python.org/pypi/jstree), just run
`pip install jstree` from the command-line.  If you already have a prior
version installed, just run `pip install jstree -U` instead.

Contribute
----------

Please help contribute to this project by going to the
[GitHub Project Repository](https://github.com/grimwm/py-jstree) and doing one
of a few things:

 * send me pull requests through the github interface
 * point me directly to your git repo so I can pull changes
 * send bug reports and feature requests by filing them under the __Issues__ tab at the top

Examples
--------
    >>> import jstree
    >>> node = jstree.Node('a', None)
    >>> print node
    Node({'data': 'a', 'children': MutableDictionaryObject({})})

    >>> import jstree
    >>> node = jstree.Node('a', None, metadata={'id':23})
    >>> print node
    Node({'data': 'a', 'children': MutableDictionaryObject({}), 'metadata': DictionaryObject({'id': 23})})

    >>> import jstree
    >>> node = jstree.Node('a', 200, metadata={'id':23})
    >>> print node
    Node({'data': 'a', 'children': MutableDictionaryObject({}), 'metadata': DictionaryObject({'id': 200})})
    
    >>> import jstree
    >>> paths = [jstree.Path("editor/2012-07/31/.classpath", 1), jstree.Path("editor/2012-07/31/.project", 2)]
    >>> print jstree.JSTree(paths).pretty()
    /
      editor/
        2012-07/
          31/
            .classpath
            .project
            
    >>> import jstree
    >>> paths = [jstree.Path("editor/2012-07/31/.classpath", 1), jstree.Path("editor/2012-07/31/.project", 2)]
    >>> t = jstree.JSTree(paths)
    >>> d = t.jsonData()
    >>> print d
    [{'data': 'editor', 'children': [{'data': '2012-07', 'children': [{'data': '31', 'children': [{'data': '.classpath', 'metadata': {'id': 1}}, {'data': '.project', 'metadata': {'id': 2}}]}]}]}]
    >>> print d[0]['children'][0]['children'][0]['children'][1]
    {'data': '.project', 'metadata': {'id': 2}}
    >>> print d[0]['children'][0]['children'][0]['children'][1]['data']
    .project
    >>> print d[0]['children'][0]['children'][0]['children'][1]['metadata']['id']
    2
