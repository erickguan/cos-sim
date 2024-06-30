"""Helpers to either demo in REPL or utility functions"""

from sim.models import Song, User, FriendList
from sim.data import save, find_by_name, find_all
from sim.song_recommendation import recommend_songs


# When accept dictionary to create a model, use a simplified sets of attributes
ALLOWED_SONG_ATTRIBUTES = frozenset(["name", "genre", "tempo", "singer", "popularity_score", "release_year"])
ALLOWED_USER_ATTRIBUTES = frozenset(["name", "username"])


def add_song(attrs: dict) -> Song:
  """Add song into library.

  :param attrs: user attributes
  """
  filtered = {}

  for k, v in attrs.items():
    if k not in ALLOWED_SONG_ATTRIBUTES:
      continue

    filtered[k] = v

  song = Song(**filtered)
  save(song)

  return find_by_name("song", song.name)  # refresh instance


def add_user(attrs: dict, playlist: list[str] | None = None) -> User:
  """Add user into library.

  Optionally add user playlist with a list of song names.

  :param attrs: user attributes
  :param playlist: song list by name
  """
  playlist = playlist or []
  filtered = {}

  for k, v in attrs.items():
    if k not in ALLOWED_USER_ATTRIBUTES:
      continue

    filtered[k] = v

  for song_name in playlist:
    if song := find_by_name("song", song_name):
      if "song_ids" not in filtered:
        filtered["song_ids"] = []
      filtered["song_ids"].append(song.id_)

  user = User(**filtered)
  save(user)

  return find_by_name("user", user.name)  # refresh instance


def add_friend(user: User, friends: list[str]) -> (User, list[User]):
  """Add users' friends into library.

  Optionally add user friends with a list of friends' name.

  :param user: user (must be saved)
  :param friends: friend list by name
  """

  # find or initialize user's friend list
  user_friend_list = find_by_name("friend_list", user.name)
  if user_friend_list is None:
    user_friend_list = FriendList(
      user_id=user.id_,
      name=user.name,  # a hack to use "index" feature. See more on `FriendList` model
      user=user,
    )

  collated_friends = []

  for friend_name in friends:
    if friend_name == user.name:
      raise ValueError("Can not add oneself as a friend")

    if friend := find_by_name("user", friend_name):
      # find or initialize friend's friend list
      friend_friend_list = find_by_name("friend_list", friend.name)
      if friend_friend_list is None:
        friend_friend_list = FriendList(
          user_id=friend.id_,
          name=friend.name,  # a hack to use "index" feature. See more on `FriendList` model
          user=friend,
        )

      if friend.id_ not in user_friend_list.friend_ids:
        user_friend_list.friend_ids.append(friend.id_)
        save(user_friend_list)

      if user.id_ not in friend_friend_list.friend_ids:
        friend_friend_list.friend_ids.append(user.id_)
        save(friend_friend_list)

      collated_friends.append(friend)

  return [user, collated_friends]


def show_song_recommendations(user: User, top_n=5, method: str = "average") -> list[Song]:
  songs = find_all("song")
  possible_songs = list(filter(lambda x: x.id_ not in user.song_ids, songs))

  return recommend_songs(user.playlist, possible_songs, top_n=top_n, method=method)
