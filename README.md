## Project setup

Except development, this project doesn't have dependencies. I wrote this on Python 3.11. I believe Python 3.8 should work as well.
Simply run `PYTHONPATH=. python scenes/1_test.py`.

For development, this project uses [`uv`](https://github.com/astral-sh/uv). See more on uv website to start.

## Project Structure

The project builds an ActiveRecord model layer. The model is in `sim/models.py`. The storage functions are built by `sim/data_store.py`.

The actual storage exists in memory in `sim/data_store.py`.

The functions to provide API (interactions) is in `sim/repl.py`.

The recommendation is built on top of models in `sim/song_recommendation.py`. A high level policy is in `sim/song_similarity.py`.

## Tests

Tests present for two purposes:
1. Functionality validation
2. Maintain program structure
3. Show readers what particular functions are doing.