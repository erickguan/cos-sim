"""Algorithms for song recommendations."""

from sim.song_similarity import calculate_similarity_index, calculate_friend_similarity_index

# Balance choices across overall quality of user's entire playlist
RECOMMEND_METHOD_AVERAGE = "average"

# Ensure at least a similar song
RECOMMEND_METHOD_MAX = "max"

# Can create a variation of songs including other features.
# Can "vary" recommendation quality in a sequence.
RECOMMEND_METHOD_WEIGHTED_AVERAGE = "weighted_average"


def recommend_songs(user_playlist, music_library, top_n=5, method=RECOMMEND_METHOD_AVERAGE):
  """Online recommendation on songs based on similarity index"""

  si_scores = []
  for library_song in music_library:
    # TODO: a naive optimization is to cache this. a scalable approach is to calculate SI offline
    si_values = [calculate_similarity_index(library_song, playlist_song) for playlist_song in user_playlist]

    if method == RECOMMEND_METHOD_AVERAGE:
      aggregated_si = sum(si_values) / len(si_values)
    elif method == RECOMMEND_METHOD_MAX:
      aggregated_si = max(si_values)
    elif method == RECOMMEND_METHOD_WEIGHTED_AVERAGE:
      weights = [1] * len(si_values)  # TODO: customize weights, can be customized
      aggregated_si = sum(w * si for w, si in zip(weights, si_values)) / sum(weights)
    else:
      raise ValueError("Unknown method specified")

    si_scores.append((library_song, aggregated_si))

  si_scores.sort(key=lambda x: x[1], reverse=True)
  recommendations = [song for song, _si in si_scores[:top_n]]  # TODO: improve top n with "container"

  return recommendations


def recommend_songs_social(user_playlist, music_library, user_friends, top_n=5):
  """Use friend similarity index to recommend songs. (Bonus task)

  3 approaches:
  1. extend recommend_songs with weights (by friend similarity index) while reuse RECOMMEND_METHOD_WEIGHTED_AVERAGE.
  2. explicitly pass weights (by friend similarity index) to recommend_songs
  3. only use friend similarity index

  Start simple with 3.
  """

  si_scores = []
  for library_song in music_library:
    value = calculate_friend_similarity_index(library_song, user_friends)
    # this is a simple implementation, if a song is not present in any of friends, it has 0 score.
    # of course, it's better to improve with other similarity data.
    #
    # For now, I implement it with simplicity.

    si_scores.append((library_song, value))

  si_scores.sort(key=lambda x: x[1], reverse=True)
  recommendations = [song for song, _si in si_scores[:top_n]]  # TODO: improve top n with "container"

  return recommendations
