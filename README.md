# Measurement Plug-In Converter Python

- [Measurement Plug-In Converter Python](#measurement-plug-in-converter-python)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
    - [NI Measurement Plug-In Converter](#ni-measurement-plug-in-converter)
    - [NI Measurement UI Creator](#ni-measurement-ui-creator)
  - [How to install?](#how-to-install)
    - [NI Measurement Plug-In Converter](#ni-measurement-plug-in-converter-1)
    - [NI Measurement UI Creator](#ni-measurement-ui-creator-1)
  - [How to run?](#how-to-run)
    - [NI Measurement Plug-In Converter](#ni-measurement-plug-in-converter-2)
      - [Supported data types](#supported-data-types)
      - [Supported instrument drivers](#supported-instrument-drivers)
      - [Prerequisites](#prerequisites)
      - [Limitations](#limitations)
      - [Additional steps for VISA instruments](#additional-steps-for-visa-instruments)
      - [Event logger](#event-logger)
    - [NI Measurement UI Creator](#ni-measurement-ui-creator-2)
      - [Create measurement UI file](#create-measurement-ui-file)
      - [Update measurement UI file](#update-measurement-ui-file)
      - [Supported data elements](#supported-data-elements)
      - [Supported data types](#supported-data-types-1)
      - [Unsupported data elements for update command](#unsupported-data-elements-for-update-command)
        - [Note](#note)
      - [Prerequisites](#prerequisites-1)
      - [Event logger](#event-logger-1)

## Introduction

Measurement Plug-In Converter Python has the following packages

- NI Measurement Plug-In Converter for Python - A CLI tool to convert Python measurements to NI measurement plug-ins.
- NI Measurement UI Creator - A CLI tool to create and update UI files for NI measurement plug-ins.

## Dependencies

### NI Measurement Plug-In Converter

- [Python = 3.8.5](https://www.python.org/downloads/release/python-385/)
- [NI Measurement UI Creator](dependencies/ni_measurement_ui_creator-1.0.0.dev8-py3-none-any.whl)

### NI Measurement UI Creator

- [Python = ^3.8](https://www.python.org/downloads/release/python-385/)

## How to install?

### NI Measurement Plug-In Converter

- Place the UI Creator and the Plug-In Converter wheel files parallel to the [install.bat](batch_files/install.bat)
- Run the `install.bat` file by double clicking it.

### NI Measurement UI Creator

- Place the Plug-In Converter wheel file parallel to the [install.bat](batch_files/install.bat)
- Run the `install.bat` file by double clicking it.

## How to run?

### NI Measurement Plug-In Converter

- Open Command Prompt
- Run the following command to know the required CLI arguments.

  ```cmd
  ni-measurement-plugin-converter --help
  ```

  ```cmd
  Usage: ni-measurement-plugin-converter [OPTIONS]

    NI Measurement Plug-In Converter is a Command Line tool to convert     
    Python measurements to measurement plug-ins.

  Options:
    -d, --display-name TEXT         Display name.  [required]
    -m, --measurement-file-path TEXT
                                    Measurement file path.  [required]
    -f, --function TEXT             Measurement function name.  [required]
    -o, --output-dir TEXT           Output directory.  [required]
    -h, --help                      Show this message and exit.
  ```

- Run the following command to convert Python measurements to measurement plug-ins.

  ```cmd
  ni-measurement-plugin-converter -d "<display name>" -m "<measurement file path>" -f "<measurement function name>" -o "<output directory>"
  ```

#### Supported data types

- Integer
- Float
- String
- Boolean
- List of integers
- List of floats
- List of strings
- List of booleans

#### Supported instrument drivers

- NI-DCPower
- NI-DMM
- NI-Digital
- NI-FGEN
- NI-Switch
- NI-Scope
- NI-DAQmx
- NI-VISA

#### Prerequisites

The Python measurement should contain a measurement function which should

- Use one of the supported [drivers](#supported-instrument-drivers) and [data types](#supported-data-types). Inputs and outputs of unsupported data types will be skipped.
- Contain a return value. The return value should be a variable and not a direct function call or constant value.

  ```py
    # Not supported
    def measurement_function() -> List[float]:
      # Measurement logic.
      return measure_voltages()

    # Supported
    def measurement_function() -> List[float]:
      # Measurement logic.
      voltages = measure_voltages()
      return voltages
  ```

- Have properly type hinted inputs and outputs.

  ```py
  # Not supported
  def measurement_function(voltage, current):
    # Measurement logic.
    resistance = voltage / current
    return resistance
  
  # Supported
  def measurement_function(voltage: int, current: float) -> float:
    # Measurement logic.
    resistance = voltage / current
    return resistance
  ```

- Have the instrument driver's session initialization inside the measurement function and within the next level of indentation.

  ```py
  # Not supported
  def measurement_function(voltage: int, current: float) -> float:
    if voltage:
      with nidcpower.Session("DCPower1") as session:
        # Measurement logic.
        return current

  # Supported
  def measurement_function(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as session:
      # Measurement logic.
      return current
  ```

- Have all the instrument driver's session initialization at a single point using the context manager `with`

  ```py
  # Not supported
  def measurement_function(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as dcpower_session:
      with nidmm.Session("DMM1") as dmm_session:
        # Measurement logic.
        return current

  # Supported
  def measurement_function(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as dcpower_session, nidmm.Session("DMM1") as dmm_session:
      return current
  ```

#### Limitations

- Conversion of class based measurements are not supported.
- Measurement UI generated by the tool will not include controls and indicators for list of booleans.
- For measurements that use VISA instruments, a few more [additional steps](#additional-steps-for-visa-instruments) must be followed.

#### Additional steps for VISA instruments

For measurement that use VISA instruments, the `session_constructor`, session type and `instrument_types` must be updated with appropriate values.

![VISA_updates](docs/images/VISA_updates.png)

Steps to be followed

- Define the grpc support.
- Define the Session class for the instrument type.
- Define the session constructor for the instrument type.

  ![VISA_updated](docs/images/VISA_updated.png)

- For `session_constructor`, create SessionConstructor object of the instrument driver used.
- For instrument_type, use the pin map instrument type id.
- For session type, the type of session should be passed.

For details, refer [Examples](https://github.com/ni/measurement-plugin-python/tree/releases/2.0/examples/nivisa_dmm_measurement)

![VISA_examples](docs/images/VISA_examples.png)

#### Event logger

- The tool will generate a log once the conversion process is started, documenting all the actions performed by the tool throughout the conversion process.
- Log file can be found in the output directory.
- The log includes the details about any errors encountered during the process.

### NI Measurement UI Creator

- Open Command Prompt
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

#### Create measurement UI file

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

  Select a measurement service index (1-1) to update/generate measui file:
  ```

- Select the measurement by entering the number for which the UI file has to be created.

  ```cmd
  Measurement UI created successfully at <Measurement UI file path>
  Process completed.
  ```

- The UI File will be created in the current working directory.

#### Update measurement UI file

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

  Select a measurement service index (1-1) to update/generate measui file:
  ```

- Selecting the measurement by entering the number which will list the configured `measui` file paths.

  ```cmd
  Available Measurement UI Files:
  1. First measui file path
  2. Second measui file path
  Select a measurement UI file index (1-1) to update:
  ```

- Select the measurement UI file which has to be updated by entering the number.

  ```cmd
    Binding UI controls and indicators...
    Creating new controls and indicators...
    Measurement UI updated successfully. Please find at <Measurement UI file path>
    Process completed.
  ```

- The updated file will be suffixed with `_updated`.

#### Supported data elements

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

#### Supported data types

- Int
- Float
- String
- Boolean
- List of integers
- List of floats
- List of string
- Pin

#### Unsupported data elements for update command

- Path Control
- Enum Control
- Enum Indicator
- Ring Control
- Ring Indicator
- Graph Array Output
- Progress Bar

##### Note

- Unsupported data elements will not be bound though they are already present in the inputted UI file.

#### Prerequisites

For update command,

- The Measurement UI file that is created in the file explorer will be invalid and hence it has to be created from Measurement Plug-In UI Editor.
- Atleast one control/indicator should be present.

#### Event logger

- The tool will generate a log once the creation/update process is started, documenting all the actions performed by the tool throughout the process.
- Log file can be found in the output directory under Logs folder.
- The log includes the details about any errors encountered during the process.
