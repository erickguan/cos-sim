"""A simple data layer that builds, save models.

Of course, use a library is better.
"""

from sim.data_store import store, retrieve, clear_store
import re

pattern = re.compile(r"(?<!^)(?=[A-Z])")

SUPPORTED_MODEL_TYPES = frozenset(["song", "user", "friend_list"])
OPERATION_SAVE = "save"
OPERATION_REMOVE = "remove"


def _index(model_type, instance, operation):
  """Store index of a model"""

  index_key = f"{model_type}_id_index"

  # keep index as a hash in the beginning of the list
  _index_data = retrieve(index_key)
  index = _index_data[0] if len(_index_data) > 0 else {}

  if operation == OPERATION_SAVE:
    index[instance.id_] = instance
  elif operation == OPERATION_REMOVE:
    if instance.id_ in index:
      del index[instance.id_]
  else:
    pass  # should not happen

  store(index_key, index)


def _camel_case_to_smoke_case(name):
  return pattern.sub("_", name).lower()


def _inflect_class_name(instance):
  """Find `instance` class name"""

  return _camel_case_to_smoke_case(type(instance).__name__)


def save(instance):
  if instance is None:
    raise ValueError("Trying to save a `None` instance")

  model_type = _inflect_class_name(instance)

  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  store(model_type, instance)
  _index(model_type, instance, OPERATION_SAVE)


def _find_from_index(model_type, id_):
  index_key = f"{model_type}_id_index"

  _index_data = retrieve(index_key)
  index = _index_data[0] if len(_index_data) > 0 else {}

  return index.get(id_)


def find(model_type, id_):
  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  instance = _find_from_index(model_type, id_)
  if instance is None:
    return

  # Note
  # Because I have only 3 models, I will write the "association" manually.
  if model_type == "user":
    instance.song_ids = list(filter(lambda x: find("song", x), instance.song_ids))
    instance.playlist = list(map(lambda x: find("song", x), instance.song_ids))
    print(retrieve("song"))
  elif model_type == "friend_list":
    instance.user = find("user", instance.user_id)
    instance.friend_ids = list(filter(lambda x: find("user", x), instance.friend_ids))
    instance.friends = list(map(lambda x: find("user", x), instance.friend_ids))

  return instance


def clear():
  clear_store()
