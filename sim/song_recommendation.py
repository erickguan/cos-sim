from sim.song_similarity import calculate_similarity_index

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
