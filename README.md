# Fantasy Anime League Engine

[![Travis (.org)](https://img.shields.io/travis/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://travis-ci.org/fantasy-anime-league/fantasy-anime-league)
[![Codecov](https://img.shields.io/codecov/c/github/fantasy-anime-league/fantasy-anime-league.svg?style=flat-square)](https://codecov.io/gh/fantasy-anime-league/fantasy-anime-league/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

## Setup

### [pipenv](https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv) requirements

```shell
# if pipenv is not already installed
$ pip install --user pipenv
...
$ pipenv install
...
# activate the Pipenv shell
$ pipenv shell
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

* Save backup of database first!

```shell
$ python run_fal.py --init-week
$ python run_fal.py --load-aces
$ python run_fal.py --anime-weekly-stats
$ python run_fal.py --team-score

# If you are confident
$ python run_fal.py --init-week --load-aces --anime-weekly-stats --team-score
```
