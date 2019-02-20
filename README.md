# Fantasy Anime League Engine

[![Travis (.org)](https://img.shields.io/travis/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://travis-ci.org/fantasy-anime-league/fantasy-anime-league)
[![Codecov](https://img.shields.io/codecov/c/github/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://codecov.io/gh/fantasy-anime-league/fantasy-anime-league/)

## Requirements

```shell
# Run these commands to get the dependencies
# JikanPy is not on PyPI so we have to install it separately
$ pip install -r requirements.txt
$ pip install git+git://github.com/AWConant/jikanpy.git
```

* [git-secret](https://git-secret.io/)

  * be sure to run `git secret reveal` after checking out master to decrypt files containing private keys for development
  * you may also need to run `git secret tell <your@email.com>` before being able to decrypt them

## Tests

```shell
# In root of repository
$ python -m pytest
```
