from sim.models import Song, User
from sim.repl import add_song, add_user, add_friend, show_song_recommendations
from sim.data import clear, find_by_name, save

import pytest


@pytest.fixture(autouse=True)
def setup_test():
  """Fixture to clear store"""

  # Setup
  clear()

  yield  # execute tests

  # Teardown


@pytest.fixture(name="songs")
def setup_songs():
  """Fixture to create a few songs"""

  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song1)
  song2 = Song(
    id_=2, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2024
  )
  save(song2)
  song3 = Song(
    id_=3, name="Song For The Lonely", genre="Pop", tempo=100, singer="Cher", popularity_score=10, release_year=2024
  )
  save(song3)


@pytest.fixture(name="users")
def setup_users():
  """Fixture to create a few users"""

  user1 = User(id_=1, username="john", name="John")
  save(user1)
  user2 = User(id_=2, username="siri", name="Siri")
  save(user2)
  user3 = User(id_=3, username="bob", name="Bob")
  save(user3)


@pytest.fixture(name="users_and_songs")
def setup_users_and_songs(users, songs):
  """Fixture to create a few users and songs"""

  john = find_by_name("user", "John")
  john.song_ids = [1, 2, 3]
  save(john)

  siri = find_by_name("user", "Siri")
  siri.song_ids = [1]
  save(siri)

  bob = find_by_name("user", "Bob")
  bob.song_ids = [2]
  save(bob)


def test_add_song():
  song = add_song(
    {"name": "Believe", "genre": "Pop", "tempo": 150, "singer": "John", "popularity_score": 10, "release_year": 2010}
  )

  assert song.id_ is not None
  assert song == find_by_name("song", "Believe")


def test_add_song_throws_when_duplicates():
  _song = add_song(
    {"name": "Believe", "genre": "Pop", "tempo": 150, "singer": "John", "popularity_score": 10, "release_year": 2010}
  )

  with pytest.raises(ValueError):
    add_song(
      {"name": "Believe", "genre": "Pop", "tempo": 150, "singer": "John", "popularity_score": 10, "release_year": 2010}
    )


def test_add_song_throws_if_attributes_are_missing():
  with pytest.raises(TypeError):
    add_song({"genre": "Pop", "tempo": 150, "singer": "John", "popularity_score": 10, "release_year": 2010})


def test_add_user(songs):
  user = add_user(
    {
      "name": "John",
      "username": "john",
    }
  )

  assert user.id_ is not None
  assert user == find_by_name("user", "John")


def test_add_user_throws_when_duplicates():
  _user = add_user(
    {
      "name": "John",
      "username": "john",
    }
  )

  with pytest.raises(ValueError):
    add_user(
      {
        "name": "John",
        "username": "john",
      }
    )


def test_add_user_ignores_invalid_attributes():
  _user = add_user({"name": "John", "username": "john", "song_ids": [1]})

  persisted_user = find_by_name("user", "John")
  assert "John" == persisted_user.name
  assert [] == persisted_user.song_ids


def test_add_user_throws_if_attributes_are_missing():
  with pytest.raises(TypeError):
    add_user(
      {
        "username": "john",
      }
    )


def test_add_friend(users):
  user = find_by_name("user", "John")

  _user, friends = add_friend(user, ["Siri"])
  assert 1 == len(friends)

  user_friend_list = find_by_name("friend_list", "John")
  assert friends == user_friend_list.friends
  siri_friend_list = find_by_name("friend_list", "Siri")
  assert [user] == siri_friend_list.friends


def test_add_friend_ignores_unfound_friend(users):
  user = find_by_name("user", "John")

  user, friends = add_friend(user, ["NOT_EXIST_USER"])

  user_friends = find_by_name("friend_list", "John")
  assert 0 == len(friends)
  assert user_friends is None


def test_add_friend_raise_when_add_oneself(users):
  user = find_by_name("user", "John")

  with pytest.raises(ValueError):
    add_friend(user, ["John"])


def test_add_friend_persists(users):
  john = find_by_name("user", "John")
  siri = find_by_name("user", "Siri")
  bob = find_by_name("user", "Bob")

  add_friend(john, ["Siri", "Bob"])
  add_friend(siri, ["John"])

  john_friend_list = find_by_name("friend_list", "John")
  assert [siri, bob] == john_friend_list.friends
  siri_friend_list = find_by_name("friend_list", "Siri")
  assert [john] == siri_friend_list.friends
  bob_friend_list = find_by_name("friend_list", "Bob")
  assert [john] == bob_friend_list.friends


def test_add_friend_persists_bidirectional(users):
  john = find_by_name("user", "John")
  siri = find_by_name("user", "Siri")
  bob = find_by_name("user", "Bob")

  add_friend(john, ["Siri", "Bob"])
  add_friend(siri, ["John"])
  add_friend(bob, ["Siri"])

  john_friend_list = find_by_name("friend_list", "John")
  assert [siri, bob] == john_friend_list.friends
  siri_friend_list = find_by_name("friend_list", "Siri")
  assert [john, bob] == siri_friend_list.friends
  bob_friend_list = find_by_name("friend_list", "Bob")
  assert [john, siri] == bob_friend_list.friends


def test_show_song_recommendations_no_more_songs(users_and_songs):
  john = find_by_name("user", "John")

  assert [] == show_song_recommendations(john)


def test_show_song_recommendations_recommends(users_and_songs):
  siri = find_by_name("user", "Siri")

  assert [find_by_name("song", "fortnight"), find_by_name("song", "Song For The Lonely")] == show_song_recommendations(
    siri
  )


def test_show_song_recommendations_recommends_relevance(users_and_songs):
  siri = find_by_name("user", "Siri")

  assert [find_by_name("song", "fortnight")] == show_song_recommendations(siri, top_n=1)
