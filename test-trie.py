#!/usr/bin/env python

import unittest
from array import array

from trie import Node, Trie

class TestCase(unittest.TestCase):
    def test_02_trie_insert_get(self):
        t = Trie()
        key = "spam"

        t[key] = "spam"
        k = key

        n1 = t.root.table[k[0]] # s
        self.assertIsInstance(n1, Node)
        self.assertFalse(hasattr(n1, "value"))

        n2 = n1.table[k[1]] # p
        self.assertIsInstance(n2, Node)
        self.assertFalse(hasattr(n2, "value"))

        n3 = n2.table[k[2]] # a
        self.assertIsInstance(n3, Node)
        self.assertFalse(hasattr(n3, "value"))

        n4 = n3.table[k[3]] # m
        self.assertIsInstance(n4, Node)
        self.assertEqual(n4.table, {})
        self.assertEqual(n4.value, "spam")

        self.assertEqual(t[key], "spam")
        self.assertRaises(KeyError, t.__getitem__, "spa")
        self.assertRaises(KeyError, t.__getitem__, "bacon")

        key = "bacon"
        t[key] = "bacon"
        k = key

        n1 = t.root.table[k[0]] # s
        self.assertIsInstance(n1, Node)
        self.assertFalse(n1.has_value)

        n5 = n1.table[k[1]].table[k[2]].table[k[3]].table[k[4]]
        self.assertIsInstance(n5, Node)
        self.assertEqual(n5.table, {})
        self.assertEqual(n5.value, "bacon")
        self.assertEqual(t[key], "bacon")

        t[key] = "coffee"
        self.assertEqual(t[key], "coffee")

        t["spAM"] = "eGGs"
        self.assertEqual(t["spAM"], "eGGs")

    def test_03_trie_contains(self):
        t = Trie()
        t["spam"] = "eggs"

        self.assertIn("spam", t)
        self.assertNotIn("bacon", t)

    def test_05_get_node(self):
        key = "spam"

        key2 = "spammer"

        t = Trie()
        t["spam"] = "egg"

        suffix, n = t.get_node(key)
        self.assertFalse(suffix)
        self.assertEqual(n.value, "egg")

        suffix, n = t.get_node(key2)
        self.assertEqual(suffix, key2[-3:])
        self.assertEqual(n.value, "egg")

    def test_06_trie_setdefault(self):
        t = Trie()

        t.setdefault("spam", []).append("eggs")
        self.assertEqual(t["spam"], ["eggs"])
        t.setdefault("spam", []).append("coffee")
        self.assertEqual(t["spam"], ["eggs", "coffee"])

        self.assertEqual(t.setdefault("spa", "bacon"), "bacon")
        self.assertEqual(t["spa"], "bacon")

    def test_07_trie_iter(self):
        t = Trie()
        l = ["spam", "eggs", "bacon", "coffee", "milk"]
        for i, j in zip(l, xrange(len(l))):
            t[i] = j

        self.assertEqual(range(len(l)), sorted(ii for ii in t))

    def test_08_find_all(self):
        t = Trie()
        l = ["spam", "spammer", "spamhouse", "spammers", "spams", "bacon"]

        for i in l:
            t[i] = i

        self.assertEqual(t.find_all("bac"), ["bacon"])
        self.assertEqual(sorted(t.find_all("spam")), sorted(l[:-1]))
        self.assertEqual(sorted(t.find_all("")), sorted(l))

    def test_09_delete(self):
        t = Trie()
        l = ["one", "two", "three", "onesee", "spam", "spammers", "spamhouse", "spams"]

        for i in l:
            t[i] = i

        self.assertEqual(sorted(t.find_all("spam")), sorted(l[-4:]))
        self.assertEqual(t.delete("spam"), "spam")
        self.assertEqual(sorted(t.find_all("spam")), sorted(l[-3:]))

        self.assertRaises(KeyError, t.delete, "four")

        self.assertEqual(sorted(t.find_all("spam")), sorted(l[-3:]))

        s, n = t.get_node("spam")
        self.assertFalse(n.has_value)



    def test_10_delete_all(self):
        t = Trie()
        l = ["one", "two", "three", "onesee", "spam", "spammers", "spamhouse", "spams"]

        for i in l:
            t[i] = i

        self.assertEqual(sorted(t.delete_all("spam")), sorted(l[-4:]))

        self.assertEqual(t.find_all("spam"), [])
        self.assertEqual(len(list(t)), 4)

        self.assertEqual(sorted(t.delete_all("o")), sorted(["one", "onesee"]))
        self.assertEqual(t.find_all("o"), [])
        self.assertEqual(len(list(t)), 2)

        self.assertEqual(t.delete_all("four"), [])
        self.assertEqual(len(list(t)), 2)

        self.assertEqual(sorted(t.delete_all("")), sorted(l[1:3]))
        self.assertEqual(list(t), [])
