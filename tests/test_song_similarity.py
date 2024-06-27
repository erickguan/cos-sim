from sim.models import Song
from sim.song_similarity import calculate_similarity_index


def test_calculate_similarity_index_1():
  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  song2 = Song(
    id_=2, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2024
  )

  # same = 4
  # total = 6
  assert 0.66 < calculate_similarity_index(song1, song2) < 0.67


def test_calculate_similarity_index_2():
  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=80, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  song2 = Song(
    id_=2, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2024
  )

  # same = 3
  # total = 6
  assert 0.5 - 10**-4 < calculate_similarity_index(song1, song2) < 0.5 + 10**-4
