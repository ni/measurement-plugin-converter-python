# NI Measurement UI Creator

- [NI Measurement UI Creator](#ni-measurement-ui-creator)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [How to install?](#how-to-install)
  - [How to run?](#how-to-run)
    - [Create measurement UI file](#create-measurement-ui-file)
    - [Update measurement UI file](#update-measurement-ui-file)
    - [Supported data types](#supported-data-types)
    - [Supported data elements](#supported-data-elements)
    - [Unsupported data elements for update command](#unsupported-data-elements-for-update-command)
    - [Prerequisites](#prerequisites)
    - [Limitations](#limitations)
    - [Event logger](#event-logger)

## Introduction

- NI Measurement UI Creator is a CLI tool to create and update UI files for NI measurement plug-ins.

## Dependencies

- [Python = ^3.8](https://www.python.org/downloads/release/python-385/)

## How to install?

- Place the UI Creator wheel file parallel to the [install.bat](../../batch_files/install.bat).
- Run the `install.bat` file by double clicking it.

## How to run?

- Open Command Prompt.
- Run the following command to know the required CLI arguments.

  ```cmd
  ni-measurement-ui-creator --help
  ```

  ```cmd
  Usage: ni-measurement-ui-creator [OPTIONS] COMMAND [ARGS]...

    NI Measurement UI Creator is a Command Line tool for creating/updating
    measui files.

  Options:
    -h, --help  Show this message and exit.

  Commands:
    create  Create a new measurement UI file.
    update  Update the measurement UI file.
  ```

### Create measurement UI file

- Run the following command to create `.measui` files.

  ```cmd
  ni-measurement-ui-creator create
  ```

  ```cmd
  Starting the NI Measurement UI Creator...
  Supported UI Elements: ['Numeric Indicator', 'Numeric Control', 'Numeric Array Input', 'Numeric Array Output', 'Boolean Horizontal Slider', 'Boolean Round LED', 'String Control', 'String Indicator', 'String Array Input', 'String Array Output', 'Pin']
  Getting the active measurements...

  Available services:
  1. First Measurement (Py)
  2. Second Measurement (Py)

  Select a measurement service index (1-2) to update/generate measui file:
  ```

- Select the measurement by entering the number for which the UI file has to be created.

  ```cmd
  Measurement UI created successfully at <Measurement UI file path>
  Process completed.
  ```

- The UI File will be created in the current working directory.

### Update measurement UI file

- Run the following command to update `.measui` files.

  ```cmd
  ni-measurement-ui-creator update
  ```

  ```cmd
  Starting the NI Measurement UI Creator...
  Supported UI Elements: ['Numeric Indicator', 'Numeric Control', 'Numeric Array Input', 'Numeric Array Output', 'Boolean Horizontal Slider', 'Boolean Round LED', 'String Control', 'String Indicator', 'String Array Input', 'String Array Output', 'Pin']
  Getting the active measurements...

  Available services:
  1. First Measurement (Py)
  2. Second Measurement (Py)

  Select a measurement service index (1-2) to update/generate measui file:
  ```

- Select the measurement by entering the number.

  ```cmd
  Available Measurement UI Files:
  1. First measui file path
  2. Second measui file path
  Select a measurement UI file index (1-2) to update:
  ```

- Select the measurement UI file which has to be updated by entering the number.

  ```cmd
  Binding UI controls and indicators...
  Creating new controls and indicators...
  Measurement UI updated successfully. Please find at <Measurement UI file path>
  Process completed.
  ```

- The updated file will be suffixed with `_updated`.

### Supported data types

- Int
- Float
- String
- Boolean
- List of integers
- List of floats
- List of string
- Pin

### Supported data elements

- Numeric Indicator
- Numeric Control
- Numeric Array Input
- Numeric Array Output
- Horizontal Slider
- Round LED
- String Control
- String Indicator
- String Array Input
- String Array Output
- Pin

### Unsupported data elements for update command

- Path Control
- Enum Control
- Enum Indicator
- Ring Control
- Ring Indicator
- Graph Array Output
- Progress Bar

### Prerequisites

For update command,

- The Measurement UI file that is created in the File Explorer directly will be invalid and hence it has to be created from Measurement Plug-In UI Editor.
- Atleast one control/indicator should be present.

### Limitations

- Though [unsupported data elements for update command](#unsupported-data-elements-for-update-command) are already present in the inputted UI file but without being bound to some input or output, the elements will not be bind. New elements for the inputs/outputs will be created if the data type of the input/output is [supported](#supported-data-types).
- Path, Enum, DoubleXYData and their array counterpart data types are not supported.

### Event logger

- The tool will generate a log once the creation/update process is started, documenting all the actions performed by the tool throughout the process.
- Log file can be found in the output directory under Logs folder.
- The log includes the details about any errors encountered during the process.
