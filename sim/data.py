"""A simple data layer that builds, save models and maintain indices.

Of course, use a library is better.
"""

from sim.data_store import store, retrieve, clear_store, overwrite
import re

pattern = re.compile(r"(?<!^)(?=[A-Z])")

SUPPORTED_MODEL_TYPES = frozenset(["song", "user", "friend_list"])
SUPPORTED_MODEL_TYPES_FINDABLE_BY_NAME = SUPPORTED_MODEL_TYPES
OPERATION_SAVE = "save"
OPERATION_REMOVE = "remove"


def _index(model_type, instance, operation):
  """Store index of a model"""

  # store id index
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

  overwrite(index_key, [index])

  # store name index
  if model_type not in SUPPORTED_MODEL_TYPES_FINDABLE_BY_NAME:
    return
  index_key = f"{model_type}_name_index"

  # keep index as a hash in the beginning of the list
  _index_data = retrieve(index_key)
  index = _index_data[0] if len(_index_data) > 0 else {}

  if operation == OPERATION_SAVE:
    index[instance.name] = instance
  elif operation == OPERATION_REMOVE:
    if instance.name in index:
      del index[instance.name]
  else:
    pass  # should not happen

  overwrite(index_key, [index])


def _camel_case_to_smoke_case(name):
  return pattern.sub("_", name).lower()


def _inflect_class_name(instance):
  """Find `instance` class name"""

  return _camel_case_to_smoke_case(type(instance).__name__)


def _retrieve_id_index(model_type):
  index_key = f"{model_type}_id_index"

  _index_data = retrieve(index_key)
  index = _index_data[0] if len(_index_data) > 0 else {}
  return index


def _find_from_id_index(model_type, id_):
  index = _retrieve_id_index(model_type)

  return index.get(id_)


def _find_from_name_index(model_type, name):
  index_key = f"{model_type}_name_index"

  _index_data = retrieve(index_key)
  index = _index_data[0] if len(_index_data) > 0 else {}

  return index.get(name)


def _validate_unique(model_type, instance):
  """Raise if uniqueness violation."""

  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  if _find_from_id_index(model_type, instance.id_) is not None:
    raise ValueError("Should not have the same id as another object in data store.")

  if model_type in SUPPORTED_MODEL_TYPES_FINDABLE_BY_NAME:
    if _find_from_name_index(model_type, instance.name) is not None:
      from pprint import pp
      from sim.data_store import _arena

      pp(_arena)
      # pp(retrieve("friend_list_id_index"))
      # pp(retrieve("friend_list_name_index"))
      raise ValueError("Should not have the same name as another object in data store.")


def save(instance):
  if instance is None:
    raise ValueError("Trying to save a `None` instance")

  model_type = _inflect_class_name(instance)

  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  index = _retrieve_id_index(model_type)
  last_id = max(index.keys() or [0])  # 0 is a sensible default because we only use last_id+1
  exist_ids = frozenset(index.keys())

  # overwrite id when invalid or not set
  if instance.id_ is None or instance.id_ not in exist_ids or instance.id_ < 1:
    instance.id_ = last_id + 1
    _validate_unique(model_type, instance)

    store(model_type, instance)
    _index(model_type, instance, OPERATION_SAVE)
  elif instance.id_ in exist_ids:  # update existing instance
    instances = retrieve(model_type)
    for idx, persisted_instance in enumerate(instances):
      if persisted_instance.id_ == instance.id_:
        instances[idx] = instance
        _index(model_type, instance, OPERATION_SAVE)
        break  # update done, no need to continue


def _build_associations(model_type, instance):
  # Note
  # Because I have only 3 models, I will write the "association" manually.
  if model_type == "user":
    instance.song_ids = list(filter(lambda x: find("song", x), instance.song_ids))
    instance.playlist = list(map(lambda x: find("song", x), instance.song_ids))
  elif model_type == "friend_list":
    instance.user = find("user", instance.user_id)
    instance.friend_ids = list(filter(lambda x: find("user", x), instance.friend_ids))
    instance.friends = list(map(lambda x: find("user", x), instance.friend_ids))


def find(model_type, id_):
  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  instance = _find_from_id_index(model_type, id_)
  if instance is None:
    return

  _build_associations(model_type, instance)

  return instance


def find_by_name(model_type, name):
  if model_type not in SUPPORTED_MODEL_TYPES_FINDABLE_BY_NAME:
    raise ValueError(f"Not supported model type {model_type}")

  instance = _find_from_name_index(model_type, name)
  if instance is None:
    return

  _build_associations(model_type, instance)

  return instance


def clear():
  clear_store()


def find_all(model_type):
  if model_type not in SUPPORTED_MODEL_TYPES:
    raise ValueError(f"Not supported model type {model_type}")

  return retrieve(model_type)
