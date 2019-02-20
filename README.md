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

### Unit Tests

```shell
# In root of repository
$ python -m pytest
```

### Integration Tests

Integration tests currently need to be run manually with:

```shell
$ python -m pytest test/integration
...
```

This is for two reasons:

* we can't really get Travis to run these tests without committing secure credentials to source control
* issues with sshtunneling as currently described in [Issue #5](https://github.com/fantasy-anime-league/fantasy-anime-league/issues/5)