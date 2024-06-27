from sim.models import Song
from sim.song_recommendation import recommend_songs, RECOMMEND_METHOD_AVERAGE


def test_recommend_songs():
  song1 = Song(
    id_=1, name="Karma", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2011
  )
  song2 = Song(
    id_=2, name="fortnight", genre="Pop", tempo=100, singer="Taylor Swift", popularity_score=80, release_year=2024
  )
  song3 = Song(id_=3, name="Wires", genre="Pop", tempo=130, singer="Athlete", popularity_score=30, release_year=2001)
  song4 = Song(
    id_=4, name="You Got the Style", genre="Pop", tempo=110, singer="Athlete", popularity_score=50, release_year=2003
  )
  song5 = Song(
    id_=5, name="El Salvador", genre="Pop", tempo=110, singer="Athlete", popularity_score=80, release_year=2003
  )
  song6 = Song(id_=6, name="Chances", genre="Pop", tempo=140, singer="Athlete", popularity_score=50, release_year=2005)

  assert [song2, song5] == recommend_songs(
    [song1], [song2, song3, song4, song5, song6], top_n=2, method=RECOMMEND_METHOD_AVERAGE
  )
