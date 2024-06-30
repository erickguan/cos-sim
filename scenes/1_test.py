from sim.repl import *
from pprint import pp

song_attrs = [
  {"name": "Blinding Lights", "genre": "Pop", "tempo": 171, "singer": "The Weeknd", "popularity_score": 95, "release_year": 2019},
  {"name": "Watermelon Sugar", "genre": "Pop", "tempo": 95, "singer": "Harry Styles", "popularity_score": 93, "release_year": 2019},
  {"name": "Dance Monkey", "genre": "Pop", "tempo": 98, "singer": "Tones and I", "popularity_score": 92, "release_year": 2019},
  {"name": "Circles", "genre": "Hip Hop", "tempo": 120, "singer": "Post Malone", "popularity_score": 91, "release_year": 2019},
  {"name": "Don't Start Now", "genre": "Pop", "tempo": 124, "singer": "Dua Lipa", "popularity_score": 94, "release_year": 2019},
  {"name": "Levitating", "genre": "Pop", "tempo": 103, "singer": "Dua Lipa", "popularity_score": 96, "release_year": 2020},
  {"name": "Savage Love", "genre": "Pop", "tempo": 132, "singer": "Jawsh 685, Jason Derulo", "popularity_score": 90, "release_year": 2020},
  {"name": "Rockstar", "genre": "Hip Hop", "tempo": 160, "singer": "DaBaby, Roddy Ricch", "popularity_score": 89, "release_year": 2020},
  {"name": "Life Goes On", "genre": "K-pop", "tempo": 126, "singer": "BTS", "popularity_score": 88, "release_year": 2020},
  {"name": "Peaches", "genre": "R&B", "tempo": 90, "singer": "Justin Bieber", "popularity_score": 87, "release_year": 2021}
]

songs = [add_song(attr) for attr in song_attrs]

user = add_user({"name": "John", "username": "john"}, ["Dance Monkey", "Rockstar"])
siri = add_user({"name": "Siri", "username": "siri"})

add_friend(user, ["Siri"])
pp(show_song_recommendations(user))