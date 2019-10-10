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
  * Contact the owners of Fantasy Anime League for an individual db user account to be created for you.

## Order to run scripts

### Preseason (before registration)
```shell
$ python run_fal.py --collect-series
$ python run_fal.py --ptw-counter
```

### Preseason (after registration)
```shell
$ python run_fal.py --load-teams
$ python run_fal.py --headcount
$ python run_fal.py --team-overview
$ python run_fal.py --team-stats
$ python run_fal.py --team-dist
```

### Midseason
```shell
$ python run_fal.py --init-week
$ python run_fal.py --load-aces
$ python run_fal.py --anime-weekly-stats
$ python run_fal.py --team-score

# If you are confident
$ python run_fal.py --init-week --load-aces --anime-weekly-stats --team-score
```

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