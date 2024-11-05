# NI Measurement UI Creator

- [NI Measurement UI Creator](#ni-measurement-ui-creator)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [How to install?](#how-to-install)
  - [How to run?](#how-to-run)
    - [Create measurement plug-in UI file](#create-measurement-plug-in-ui-file)
    - [Update measurement plug-in UI file](#update-measurement-plug-in-ui-file)
    - [Supported data types](#supported-data-types)
    - [Supported data elements](#supported-data-elements)
    - [Unsupported data elements for update command](#unsupported-data-elements-for-update-command)
    - [Prerequisites](#prerequisites)
    - [Limitations](#limitations)
    - [Event logger](#event-logger)

## Introduction

- The Measurement Plug-In UI Creator is a CLI tool to create or update `.measui` files for measurement plug-ins.

## Dependencies

- [Python = ^3.8](https://www.python.org/downloads/release/python-385/)

## How to install?

- Place the UI Creator wheel file parallel to the [install.bat](../../batch_files/install.bat).
- Run the `install.bat` file by double clicking it.

## How to run?

- Open Command Prompt.
- Run the following command to know the available commands.

  ```cmd
  ni-measurement-plugin-ui-creator --help
  ```

  ```cmd
  Usage: ni-measurement-plugin-ui-creator [OPTIONS] COMMAND [ARGS]...

    NI Measurement Plug-In UI Creator is a Command Line tool for creating/updating
    measui files.

  Options:
    -h, --help  Show this message and exit.

  Commands:
    create  Create a new measurement plug-in UI file.
    update  Update the measurement plug-in UI file.
  ```

### Create measurement plug-in UI file

- Run the following command to create new `.measui` file(s).

  ```cmd
  ni-measurement-plugin-ui-creator create
  ```

  ```cmd
  Starting the NI Measurement Plug-In UI Creator...
  Supported UI Elements: ['Numeric Indicator', 'Numeric Control', 'Numeric Array Input', 'Numeric Array Output', 'Boolean Horizontal Slider', 'Boolean Round LED', 'String Control', 'String Indicator', 'String Array Input', 'String Array Output', 'Pin']
  Getting the active measurements...

  Available services:
  1. First Measurement (Py)
  2. Second Measurement (Py)

  Select a measurement service index (1-2) to update/generate measui file:
  ```

- Select the measurement by entering the number for which the UI file has to be created.

  ```cmd
  Measurement Plug-In UI created successfully at <Measurement Plug-In UI file path>
  Process completed.
  ```

- The UI File will be created in the current working directory.

### Update measurement plug-in UI file

- Run the following command to update `.measui` files.

  ```cmd
  ni-measurement-plugin-ui-creator update
  ```

  ```cmd
  Starting the NI Measurement Plug-In UI Creator...
  Supported UI Elements: ['Numeric Indicator', 'Numeric Control', 'Numeric Array Input', 'Numeric Array Output', 'Boolean Horizontal Slider', 'Boolean Round LED', 'String Control', 'String Indicator', 'String Array Input', 'String Array Output', 'Pin']
  Getting the active measurements...

  Available services:
  1. First Measurement (Py)
  2. Second Measurement (Py)

  Select a measurement service index (1-2) to update/generate measui file:
  ```

- Select the measurement by entering the number.

  ```cmd
  Available Measurement Plug-In UI Files:
  1. First measui file path
  2. Second measui file path
  Select a measurement plug-in UI file index (1-2) to update:
  ```

- Select the measurement plug-in UI file which has to be updated by entering the number.

  ```cmd
    Binding UI controls and indicators...
    Creating new controls and indicators...
    Measurement plug-in UI updated successfully. Please find at <Measurement Plug-In UI file path>
    Process completed.
  ```

- The updated file will be suffixed with `_updated`.

### Supported data types

- Int
- Float
- String
- Boolean
- Pin
- 1D array of int, float, string

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

- The selected measurement plug-in UI file should have been created using the Measurement Plug-In UI Editor.
- Atleast one control/indicator should be present in it.

### Limitations

- Unsupported data elements for the update command, if present in the input UI file but not bound to any input or output, will remain unbound. New elements will be created for inputs and outputs if their data types are [supported](#supported-data-types).
- Data types such as `Path`, `Enum`, `DoubleXYData`, and their 1D array variants are not supported.

### Event logger

- The tool generates a log at the start of the conversion process, recording all actions performed throughout.
- The log file is located inside the "Logs" folder within the output directory.
- This log includes detailed information on any errors encountered during the process.
