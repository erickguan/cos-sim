from dataclasses import dataclass, field


@dataclass
class Song:
  id_: int
  name: str
  genre: str
  tempo: int
  singer: str
  popularity_score: int
  release_year: int


@dataclass
class User:
  id_: int
  username: str
  name: str

  song_ids: list[int] = field(default_factory=list)
  # `data` module maps `sond_ids` to `playlist`.
  # The list might omit song when song doesn't exist or invalid.
  playlist: list[Song] = field(default_factory=list)


@dataclass
class FriendList:
  id_: int
  user_id: int
  # `data` module maps `user_id` to `user`. `None` when user doesn't exist or invalid.
  user: User | None = None

  friend_ids: list[int] = field(default_factory=list)
  # `data` module maps `friend_ids` to `friends`.
  # The list might omit users when user doesn't exist or invalid.
  friends: list[User] = field(default_factory=list)
