#!/usr/bin/env python

import unittest
from array import array

from trie import translate, Node, Trie, TLEN

class TestCase(unittest.TestCase):
    def test_01_translate(self):
        k = translate("abc123")

        self.assertEqual(k, array("b", [0, 1, 2, 26, 27, 28]))

    def test_02_trie_calc_key(self):
        key = "abc123"
        k = translate(key)

        t = Trie()
        self.assertEqual(t.calc_key(key), k)
        self.assertRaises(ValueError, t.calc_key, "abc*&^")

    def test_03_trie_insert_get(self):
        t = Trie()
        key = "spam"

        t[key] = "spam"
        k = translate(key)

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
        self.assertEqual(n4.table, [None] * TLEN)
        self.assertEqual(n4.value, "spam")

        self.assertEqual(t[key], "spam")
        self.assertRaises(KeyError, t.__getitem__, "spa")
        self.assertRaises(KeyError, t.__getitem__, "bacon")

        key = "bacon"
        t[key] = "bacon"
        k = translate(key)

        n1 = t.root.table[k[0]] # s
        self.assertIsInstance(n1, Node)
        self.assertFalse(n1.has_value)

        n5 = n1.table[k[1]].table[k[2]].table[k[3]].table[k[4]]
        self.assertIsInstance(n5, Node)
        self.assertEqual(n5.table, [None] * TLEN)
        self.assertEqual(n5.value, "bacon")
        self.assertEqual(t[key], "bacon")

        t[key] = "coffee"
        self.assertEqual(t[key], "coffee")


    def test_05_trie_contains(self):
        t = Trie()
        t["spam"] = "eggs"

        self.assertIn("spam", t)
        self.assertNotIn("bacon", t)

    def test_05_get_node(self):
        key = "spam"
        k = translate(key)

        key2 = "spammer"
        k2 = translate(key2)

        t = Trie()
        t["spam"] = "egg"

        suffix, n = t.get_node(key)
        self.assertFalse(suffix)
        self.assertEqual(n.value, "egg")

        suffix, n = t.get_node(key2)
        self.assertEqual(suffix, k2[-3:])
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

        self.assertEqual(sorted(t.delete_all("spam")), sorted(l[-3:]))
        self.assertEqual(t.find_all("spam"), [])
        self.assertEqual(len(list(t)), 4)

        self.assertEqual(sorted(t.delete_all("o")), sorted(["one", "onesee"]))
        self.assertEqual(t.find_all("o"), [])
        self.assertEqual(len(list(t)), 2)

        self.assertEqual(t.delete_all("four"), [])
        self.assertEqual(len(list(t)), 2)

        self.assertEqual(sorted(t.delete_all("")), sorted(l[1:3]))
        self.assertEqual(list(t), [])
