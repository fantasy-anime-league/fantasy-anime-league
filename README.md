# Fantasy Anime League Engine

[![Travis (.org)](https://img.shields.io/travis/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://travis-ci.org/fantasy-anime-league/fantasy-anime-league)
[![Codecov](https://img.shields.io/codecov/c/github/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://codecov.io/gh/fantasy-anime-league/fantasy-anime-league/)

## Setup

### pip requirements

```shell
$ pip install -r requirements.txt
...
```

### [git-secret](https://git-secret.io/)

* be sure to run `git secret reveal` after checking out master to decrypt files containing private keys for development
* you may also need to run `git secret tell <your@email.com>` before being able to decrypt them

### [Connecting to MySQL database](https://www.namecheap.com/support/knowledgebase/article.aspx/1249/89/how-to-remotely-connect-to-a-mysql-database-located-on-our-shared-server)

* After tunnelling with PuTTY, you will be asked for login credentials. Adding your public key for SSH access will make your login process slightly easier.
* You may wish to use a desktop client such as [HeidiSQL](https://www.heidisql.com/) for convenience.
  * Contact the owners Fantasy Anime League for an individual db user account to be created for you.

## Tests

### Unit and Integration Tests

```shell
# In root of repository
$ python -m pytest
```

### Type Checking

```shell
$ mypy fal run_fal.py
...
```