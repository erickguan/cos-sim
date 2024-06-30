"""Policies for song recommendations"""

from dataclasses import fields

# a whitelist for song's similarity fields
SONG_SIMILARITY_FIELDS = ["name", "genre", "tempo", "singer", "popularity_score", "release_year"]


def calculate_similarity_index(song1, song2):
  # TODO: consider normalize different fields
  # e.g., `release_year`, `tempo` can be better to put in bins
  same_attributes = sum(
    1
    for field in fields(song1)
    if field.name in SONG_SIMILARITY_FIELDS and getattr(song1, field.name) == getattr(song2, field.name)
  )
  total_attributes = len(list(filter(lambda x: x.name in SONG_SIMILARITY_FIELDS, fields(song1))))
  return same_attributes / total_attributes


def calculate_friend_similarity_index(song, user_friends):
  total_presence = sum(1 for user in user_friends if song in user.playlist)
  return total_presence / len(user_friends)
