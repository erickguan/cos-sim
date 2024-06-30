from sim.models import Song, User, FriendList
from sim.data import save, find, clear, find_by_name, find_all

import pytest


@pytest.fixture(autouse=True)
def setup_test():
  """Fixture to clear store"""

  # Setup
  clear()

  yield  # execute tests

  # Teardown


def test_save_song():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)

  assert True  # test should pass without exception


def test_find_song():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)

  assert song == find("song", 1)


def test_find_song_by_name():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)

  assert song == find_by_name("song", "Karma")


def test_save_user():
  user = User(id_=1, username="john", name="John")
  save(user)

  assert True  # test should pass without exception


def test_find_user():
  user = User(id_=1, username="john", name="John", song_ids=[1])
  save(user)

  user = find("user", 1)
  assert [] == user.song_ids  # no associated song_ids
  assert [] == user.playlist  # no associated playlist


def test_find_user_by_name():
  user = User(id_=1, username="john", name="John", song_ids=[1])
  save(user)

  user = find_by_name("user", "John")
  assert 1 == user.id_


def test_find_user_with_song():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)
  user = User(id_=1, username="john", name="John", song_ids=[1])
  save(user)

  user = find("user", 1)
  assert [1] == user.song_ids
  assert [song] == user.playlist


def test_save_friend_list():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)
  user1 = User(id_=1, username="john", name="John", song_ids=[1])
  save(user1)
  user2 = User(id_=2, username="Tom", name="Tom", song_ids=[1])
  save(user2)
  friend_list1 = FriendList(id_=1, name="John", user_id=1, friend_ids=[2])
  save(friend_list1)
  friend_list2 = FriendList(id_=2, name="Tom", user_id=2, friend_ids=[1])
  save(friend_list2)

  assert True  # test should pass without exception


def test_find_friend_list():
  song = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song)
  user1 = User(id_=1, username="john", name="John", song_ids=[1])
  save(user1)
  user2 = User(id_=2, username="Tom", name="Tom", song_ids=[1])
  save(user2)
  friend_list1 = FriendList(id_=1, name="John", user_id=1, friend_ids=[2])
  save(friend_list1)
  friend_list2 = FriendList(id_=2, name="Tom", user_id=2, friend_ids=[1])
  save(friend_list2)

  friend_list = find("friend_list", 1)
  assert user1 == friend_list.user
  assert [user2] == friend_list.friends


def test_find_all():
  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song1)
  song2 = Song(
    id_=2, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2024
  )
  save(song2)

  assert [song1, song2] == find_all("song")


def test_save_set_id():
  song = Song(name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011)
  save(song)

  song = find_all("song")[-1]
  assert 1 == song.id_
  assert "Karma" == song.name


def test_save_overwrite_existing_song():
  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song1)
  song2 = Song(
    id_=1, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  save(song2)

  songs = find_all("song")
  song = songs[-1]
  assert 1 == len(songs)
  assert 1 == song.id_
  assert "fortnight" == song.name


def test_save_raise_with_same_name():
  song1 = Song(name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011)
  save(song1)
  song2 = Song(name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011)

  with pytest.raises(ValueError):
    save(song2)
