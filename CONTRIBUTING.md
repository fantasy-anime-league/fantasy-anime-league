# Contributing

## Code Formatting
We use the [black](https://github.com/psf/black) code formatter. Please run black
on any files that you change in your pull request.

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
