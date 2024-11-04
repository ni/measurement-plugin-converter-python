# Contributing to Measurement Plug-In Converter Python

Contributions to Measurement Plug-In Converter Python are welcome from all!

Measurement Plug-In Converter Python is managed via [git](https://git-scm.com), with the canonical upstream
repository hosted on [GitHub](https://github.com/ni/measurement-plugin-converter-python).

Measurement Plug-In Converter Python follows a pull-request model for development.  If
you wish to contribute, you will need to create a GitHub account, clone this
project, push a branch with your changes to your project, and then submit a
pull request.

Please remember to sign off your commits (e.g., by using `git commit -s` if you
are using the command-line client). This amends your git commit message with a line
of the form `Signed-off-by: Name LastName <name.lastmail@emailaddress.com>`. Please
include all authors of any given commit into the commit message with a
`Signed-off-by` line. This indicates that you have read and signed the Developer
Certificate of Origin (see below) and can legally submit your code to
this repository.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/)
for more details.

## Prerequisites

- (Optional) Install [Visual Studio Code](https://code.visualstudio.com/download).
- Install Git.
- Install Python and add it to the `PATH`.
- For the recommended Python version of NI Measurement Plug In Converter,
  see [Dependencies](src/converter/README.md#dependencies).
- For the recommended Python version of NI Measurement UI Creator,
  see [Dependencies](src/ui_creator/README.md#dependencies)
- Install [Poetry](https://python-poetry.org/docs/#installation). Version >= 1.8.2

## Clone or Update the Git Repository

To download the Measurement Plug-In Converter Python source, clone its Git
repository to your local PC.

```cmd
git clone https://github.com/ni/measurement-plugin-converter-python.git
```

If you already have the Git repository on your local PC, you can update it

```cmd
git checkout main

git pull
```

## Set up the Virtual Environment for NI Measurement Plug-In Converter

To setup the virtual environment

```cmd
cd measurement-plugin-converter-python/src/converter

poetry env use <Python path>
```

To run commands and scripts, spawn a shell within the virtual environment managed by Poetry:

```cmd
poetry shell
```

To install the dependencies,

```cmd
pip install <Measurement UI Creator wheel file path>

poetry install
```

## Set up the Virtual Environment for NI Measurement UI Creator

To setup the virtual environment

```cmd
cd measurement-plugin-converter-python/src/ui_creator

poetry env use <Python path>
```

To run commands and scripts, spawn a shell within the virtual environment managed by Poetry:

```cmd
poetry shell
```

To install the dependencies,

```cmd
poetry install
```

# Lint and Build Code

Change directory using the following command to respective packages

```cmd
cd <converter path>

Or

cd <ui_creator path>
```

## Lint Code for Style and Formatting

Use [ni-python-styleguide](https://github.com/ni/python-styleguide) to lint the
code for style and formatting. This runs other tools such as `flake8`,
`pycodestyle`, and `black`.

```cmd
poetry run ni-python-styleguide lint
```

If there are any failures, try using `ni-python-styleguide` to fix them, then
lint the code again. If `ni-python-styleguide` doesn't fix the failures, you
will have to manually fix them.

```cmd
poetry run ni-python-styleguide fix

poetry run ni-python-styleguide lint
```

## Mypy Type Checking

Use [Mypy](https://pypi.org/project/mypy/) to type check the code.

```cmd
poetry run mypy <package folder>
```

## Bandit Security Checks

Use [Bandit](https://pypi.org/project/bandit/) to check for common security issues.

```cmd
poetry run bandit -c pyproject.toml -r <package folder>
```

## Build Distribution Packages

To build distribution packages, run `poetry build`. This generates installable
distribution packages (source distributions and wheels) in the `dist`
subdirectory.

```cmd
poetry build
```

# Adding Dependencies

You can add new dependencies using `poetry add` or by editing the `pyproject.toml` file.

When adding new dependencies, use a `>=` version constraint (instead of `^`)
unless the dependency uses semantic versioning.

# Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/measurement-plugin-converter-python/blob/main/LICENSE)
for details about how Measurement Plug-In Converter is licensed.
