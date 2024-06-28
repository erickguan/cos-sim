"""Helpers to either demo in REPL or utility functions"""

from sim.models import Song, User, FriendList
from sim.data import save, find_by_name


# When accept dictionary to create a model, use a simplified sets of attributes
ALLOWED_SONG_ATTRIBUTES = frozenset(['name', 'genre', 'tempo', 'singer', 'popularity_score', 'release_year'])
ALLOWED_USER_ATTRIBUTES = frozenset(['name', 'genre', 'tempo', 'singer', 'popularity_score', 'release_year'])

def add_song(attrs: dict) -> Song:
  filtered = {}

  for k, v in attrs.items():
    if k not in ALLOWED_SONG_ATTRIBUTES:
      continue

    filtered[k] = v
  
  song = Song(**filtered)
  save(song)

  return find_by_name('song', song.name) # refresh instance

def add_user(attrs: dict, playlist: list[str]=lambda: []) -> User:
  """Add user into library.

  Optionally add user playlist with a list of song names.

  :param attrs: user attributes
  :param playlist: song list by name
  """
  filtered = {}

  for k, v in attrs.items():
    if k not in ALLOWED_USER_ATTRIBUTES:
      continue

    filtered[k] = v
  
  for song_name in playlist:
    if song := find_by_name('song', song_name):
      filtered.song_ids.append(song.id_)

  user = User(**filtered)
  save(user) 

  return find_by_name('user', user.name) # refresh instance

def add_friend(user: User, friends: list[str]):
  """Add users' friends into library.

  Optionally add user friends with a list of friends' name.

  :param attrs: user attributes
  :param friends: friend list by name
  """

  # remember validation
  for song_name in playlist:
    if song := find_by_name('song', song_name):
      filtered.song_ids.append(song.id_)

  user = User(**filtered)
  save(user) 
