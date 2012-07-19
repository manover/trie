#!/usr/bin/env python

import re
import string
import array

class Node(object):
    __slots__ = ["table", "value"]

    def __init__(self, key, val):
        self.table = {}
        self.insert(key, val)

    def __repr__(self):
        return "%s object at 0x%x: value = %s" % (self.__class__, id(self),
                        self.value if self.has_value else "<EMPTY>")

    def __iter__(self):
        if self.has_value:
            yield self
        for n in self.table.itervalues():
            for i in n.__iter__():
                yield i

    @property
    def has_value(self):
        return hasattr(self, "value")

    def insert(self, key, val):
        if key:
            # Parent node
            sub = key[0]
            suffix = key[1:]
            if sub in self.table:
                # Child node exists
                self.table[sub].insert(suffix, val)
            else:
                # Create a new child for this table entry
                self.table[sub] = Node(suffix, val)
        elif key is None:
            # Special case - root node
            pass
        else:
            # Leaf node
            self.value = val

class Trie(object):
    def __init__(self):
        self.root = Node(None, None)

    def __getitem__(self, key):
        suffix, node = self.get_node(key)
        if suffix:
            raise KeyError("Key not found '%s'" % key)
        else:
            if node.has_value:
                return node.value
            else:
                raise KeyError("Key not found '%s'" % key)

    def get_node(self, key):
        """
            Returns (zero key, node) containing key if present,
            (key leftover (suffix), last known node) otherwise
        """
        node = self.root
        while key:
            if key[0] in node.table:
                node = node.table[key[0]]
            else:
                return key, node
            key = key[1:]
        return key, node

    def __delitem__(self, key):
        suffix, node = self.get_node(key)
        if suffix:
            raise KeyError("Key not found: '%s'" % key)
        else:
            if node.has_value:
                val = node.value
                del node.value
                return val
            else:
                raise KeyError("Key not found: '%s'" % key)
    delete = __delitem__

    def delete_all(self, key):
        suffix, parent = self.get_node(key[:-1])
        if suffix:
            return []

        if key:
            k = key[-1]
            node = parent.table[k]
            if node:
                del parent.table[k]
        else:
            # Special case (empty key) - delete the whole tree
            node = self.root
            self.root = Node(None, None)

        if node:
            vals = (ii.value for ii in iter(node))
        else:
            vals = []

        return vals

    def __setitem__(self, key, val):
        self.root.insert(key, val)

    def setdefault(self, key, default=None):
        suffix, node = self.get_node(key)

        if not suffix:
            if node.has_value:
                return node.value
            else:
                node.insert(suffix, default)
                return default
        else:
            node.insert(suffix, default)
            return default

    def find_all(self, key):
        suffix, node = self.get_node(key)

        if suffix:
            return []
        else:
            return [ii.value for ii in iter(node)]

    def __contains__(self, key):
        suffix, node = self.get_node(key)

        return not bool(suffix)

    def __iter__(self):
        return (ii.value for ii in self.root)
