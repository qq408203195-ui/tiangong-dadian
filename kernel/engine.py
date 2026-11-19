"""Minimal engine-independent quarterly inventory operations; values are game design, not historical claims."""
from copy import deepcopy


def apply_recipe(inventory, recipe):
    """Execute one recipe atomically, rejecting invalid amounts and shortages."""
    result = deepcopy(inventory)
    for key, value in result.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f'invalid inventory: {key}')
    for field in ('inputs', 'outputs'):
        if not isinstance(recipe.get(field), dict) or not recipe[field]:
            raise ValueError(f'missing {field}')
        for key, value in recipe[field].items():
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise ValueError(f'invalid amount: {key}')
    for key, value in recipe['inputs'].items():
        if result.get(key, 0) < value:
            raise ValueError(f'insufficient inventory: {key}')
    for key, value in recipe['inputs'].items():
        result[key] -= value
    for key, value in recipe['outputs'].items():
        result[key] = result.get(key, 0) + value
    return result
