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

  # has to appear later because of default argument
  id_: int | None = None

  # `data` module maps `user_id` to `user`. `None` when user doesn't exist or invalid.
  user: User | None = None

  friend_ids: list[int] = field(default_factory=list)
  # `data` module maps `friend_ids` to `friends`.
  # The list might omit users when user doesn't exist or invalid.
  friends: list[User] = field(default_factory=list)
