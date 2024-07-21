# NI Measurement Plug-in Converter for Python

### Description

- NI Measurement Plug-in Converter for Python is a CLI tool used to convert python measurements to NI Measurement Plug-ins.

### Code Setup

- Clone the repository using `git clone <repository link>`.
- Check out to the required branch using `git checkout <branch name>`

### Setup Virtual Environment

- Open terminal.
- Run `cd python-code-migration-utility`
- Run `poetry env use <Python 3.8 path>`
- Run `poetry shell` to activate virtual environment.
- Run `poetry install` to install dependency files.

### Example usage

- Run `ni-measurement-plugin-converter --help` to know required CLI arguments.
```
Usage: ni-measurement-plugin-converter [OPTIONS]

  Run the CLI tool.

  Args:     display_name (str): Display name.     measurement_file_dir (str):
  Measurement file directory.     function (str): Measurement function name.
  output_dir (str): Output directory.

Options:
  -d, --display-name TEXT         Display name.  [required]
  -m, --measurement-file-dir TEXT
                                  Measurement file directory.  [required]
  -f, --function TEXT             Measurement function name.  [required]
  -o, --output-dir TEXT           Output directory.  [required]
  -h, --help                      Show this message and exit.
```
- Run `ni-measurement-plugin-converter -d <display name> -m <measurement file direcotry> -f <measurement function name> -o <output directory>` to convert python measurement to measurement plug-in.
