import unittest
from kernel.engine import apply_recipe


class EngineTests(unittest.TestCase):
    def test_atomic_inventory_change(self):
        stock = {'ore': 3, 'fuel': 2}
        self.assertEqual(apply_recipe(stock, {'inputs': {'ore': 2, 'fuel': 1}, 'outputs': {'iron': 1}}), {'ore': 1, 'fuel': 1, 'iron': 1})
        self.assertEqual(stock, {'ore': 3, 'fuel': 2})

    def test_shortage_does_not_change_stock(self):
        stock = {'ore': 1}
        with self.assertRaises(ValueError):
            apply_recipe(stock, {'inputs': {'ore': 2}, 'outputs': {'iron': 1}})
        self.assertEqual(stock, {'ore': 1})

    def test_rejects_invalid_quantities(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(value=value), self.assertRaises(ValueError):
                apply_recipe({'ore': 2}, {'inputs': {'ore': value}, 'outputs': {'iron': 1}})
