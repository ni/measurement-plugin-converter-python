# NI Measurement Plug-In UI Creator

- [NI Measurement Plug-In UI Creator](#ni-measurement-plug-in-ui-creator)
      - [Create measurement plug-in UI file](#create-measurement-plug-in-ui-file)
      - [Update measurement plug-in UI file](#update-measurement-plug-in-ui-file)
      - [Prerequisites](#prerequisites)
      - [Supported data types](#supported-data-types)
      - [Supported data elements](#supported-data-elements)
      - [Unsupported data elements for update command](#unsupported-data-elements-for-update-command)
      - [Event logger](#event-logger)
      - [Limitations](#limitations)

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

The create command will create a new UI file for the selected active measurement.

- Run the following command to create new `.measui` file(s).

  ```cmd
  ni-measurement-plugin-ui-creator create
  ```

  ```cmd
  Starting the NI Measurement Plug-In UI Creator...
  Supported UI Elements: ['Boolean Horizontal Slider', 'Boolean Round LED', 'Numeric Array Input', 'Numeric Array Output', 'Numeric Control', 'Numeric Indicator', 'Pin', 'String Array Input', 'String Array Output', 'String Control', 'String Indicator']
  Getting the active measurements...

  Registered measurements:
  1. First Measurement (Py)
  2. Second Measurement (Py)

  Select a measurement service index (1-2) to update/generate measui file:
  ```

- Select the measurement by entering the number for which the UI file has to be created.

  ```cmd
  Measurement Plug-In UI created successfully at <Measurement Plug-In UI file path>
  Process completed.
  ```

- The UI file will be created in the current working directory.

### Update measurement plug-in UI file

The update command will update the UI file by

- Linking controls and indicators to its respective inputs and outputs if there are any controls and indicators unlinked
- Creating new controls and indicators and linking it to the inputs and outputs.

- Run the following command to update `.measui` files.

  ```cmd
  ni-measurement-plugin-ui-creator update
  ```

  ```cmd
  Starting the NI Measurement Plug-In UI Creator...
  Supported UI Elements: ['Boolean Horizontal Slider', 'Boolean Round LED', 'Numeric Array Input', 'Numeric Array Output', 'Numeric Control', 'Numeric Indicator', 'Pin', 'String Array Input', 'String Array Output', 'String Control', 'String Indicator']
  Getting the active measurements...

  Registered measurements:
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

### Prerequisites

For update command,

- The selected measurement plug-in UI file should have been created using the Measurement Plug-In UI Editor.
- Atleast one control/indicator should be present in the measurement plug-in UI file.

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

### Event logger

- The tool generates a log at the start of the conversion process, recording all actions performed throughout.
- The log file is located inside the "ui_creator_logs" folder within the output directory.
- This log includes detailed information on any errors encountered during the process.

### Limitations

- For the update command, if an unsupported data element exists in the input UI file and is not linked to any input or output, it will remain unbound and will not be updated. New elements will be created for inputs and outputs if their data types are [supported](#supported-data-types).
- Data types such as `Path`, `Enum`, `DoubleXYData`, and their 1D array variants are not supported.
