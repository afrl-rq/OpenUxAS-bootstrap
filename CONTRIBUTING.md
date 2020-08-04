Contributing to OpenUxAS-bootstrap
==================================

Thank you for taking the time to contribute!

Code conventions
----------------

### pre-commit checks

Before contributing a change please activate pre-commit checks locally:

```bash
$ pip3 install pre-commit
$ pre-commit install
```

Note that the pre-commit check configuration can be found in ``.pre-commit-config.yaml``. 
Before any change to that file please run:

```bash
$ pre-commit run --all-files
```

The pre-commit checks will format the code with Black, run flake8 and mypy.

### Flake8, mypy, and Black

All code should follow [PEP8](https://www.python.org/dev/peps/pep-0008/),
[PEP257](https://www.python.org/dev/peps/pep-0257/). The code is automatically
formatted with Black at commit time.

All changes should contain type hinting and running mypy should be clean of
errors.

You should also document your method's parameters and their return values
in *reStructuredText* format:

```python
"""Doc string for function

:param myparam1: description for param1
:param myparam2: description for param1
:return: description for returned object
"""
```
The code is automatically formatted with Black.
