Changes
=======

v0.4
====
* Removed the 'id' tag from general data.
* Renamed 'metadata' to 'li_attr'.

v0.3
====
* Enhanced JSTree so it can add IDs to leaf nodes for selection in
  a jsTree.  Although, this may need more work after testing in
  a jsTree application.
* Updated all the doctests to handle the additional burden
  of users being able to pass in arbitrary attributes and
  "path object ids".
* Removed ability to copy JSTrees directly in __init__ since it's
  not actually a use-case right now.  Trying to avoid code smells.

v0.2
====
* Started updating the changelog, finally.
* Simplified the tree data structure by removing the insertion of
  "data" at the top-level.  This means JS clients will have to add
  it themselves when doing full-loads of data off the server, but
  it also means that AJAX-based jsTrees should work properly.  More
  testing on this is required, however.
* Started enhancing the in-code documentation so devs get a better
  sense of how to use the code.
* Hardened jstree.Node to be "as immutable as possible" right now
  without a lot of major code changes.
* Enhanced jstree.Node for advanced usage.  Users can now pass
  additional attributes directly into it if they're managing
  a set of Nodes themselves.

v0.1.2
======
* Fixed 'dictobj' as a requirement of jstree.

v0.1.1
======
* Changed dev status to alpha.  Was incorrectly set to beta.
* Fixed setup.py for users of Python pre-2.7.
* Added Node class to make creation of JSON more manageable.

v0.1
------
* First release.
