"""A simple data storage using only linear memory"""

_arena = {}


def store(model_type, instance):
  if model_type not in _arena:
    _arena[model_type] = []
  _arena[model_type].append(instance)


def overwrite(model_type, data):
  _arena[model_type] = data


def retrieve(model_type):
  return _arena.get(model_type, [])


def clear_store():
  global _arena
  _arena = {}
