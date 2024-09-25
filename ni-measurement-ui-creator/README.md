# NI Measurement UI Creator

### Description

- NI Measurement UI Creator is a command-line tool for generating `measui` files for active measurements.

### Prerequisite

For update command,
- Meas UI file has to be created from Measurement Plug-In UI Editor.
- Atleast one control/indicator should be present.

### Code Setup

- Clone the repository using `git clone <respository link>`.
- Check out to the required branch using `git checkout <branch name>`.
- Please find the branch [here](https://github.com/ni/ni-measurement-plugin-converter/tree/ni-measui-creator)

### Setup Virtual Environment

- Open terminal.
- Run `cd ni-measurement-ui-creator`
- Run `poetry env use "<Python38 Path>"`.
- Run `poetry shell` to activate virtual environment.
- Run `pip install dependencies\<whl files>`.
- Run `poetry install` to install dependency files.

### Installing whl file

- Run `pip install <ni-measurement-ui-creator whl file>`.
- Run `ni-measurement-ui-creator --output-directory <output folder path>` to run the tool.
- Ensure measurement services are running.

### Supported data elements

- Numeric Indicator
- Numeric Control
- Numeric Array Input
- Numeric Array Output
- Horizontal Slider
- Round LED
- String Control
- String Indicator
- Pin

### Binds the supported data types for update command.

- Int
- Float
- String
- Numeric Array

### Unsupported elements for update command

- Path Control
- Enum Control
- Enum Indicator
- Ring Control
- Ring Indicator
- Graph Array Output
- Progress Bar
- RadialProgressBar
