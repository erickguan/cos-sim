"""
ActiveRecord style models based on dataclass.

Caveat exists such as:
* associations are set up by data layer.
* associations needs to be manually constructed.
* some data validation happens at data layer.
"""

from dataclasses import dataclass, field


@dataclass
class Song:
  name: str
  genre: str
  tempo: int
  singer: str
  popularity_score: int
  release_year: int

  # has to appear later because of default argument
  id_: int | None = None


@dataclass
class User:
  username: str
  name: str

  # has to appear later because of default argument
  id_: int | None = None
  song_ids: list[int] = field(default_factory=list)
  # `data` module maps `sond_ids` to `playlist`.
  # The list might omit song when song doesn't exist or invalid.
  playlist: list[Song] = field(default_factory=list)


@dataclass
class FriendList:
  user_id: int
  # user's name. This is a hack to reuse "name" index.
  # I made this to save implementation time for this demo.
  name: str

  # has to appear later because of default argument
  id_: int | None = None

  # `data` module maps `user_id` to `user`. `None` when user doesn't exist or invalid.
  user: User | None = None

  friend_ids: list[int] = field(default_factory=list)
  # `data` module maps `friend_ids` to `friends`.
  # The list might omit users when user doesn't exist or invalid.
  #
  # assume friends are bidirectional and user can't choose not to have a friend
  friends: list[User] = field(default_factory=list)
