# NI Measurement Plug-In Converter

- [NI Measurement Plug-In Converter](#ni-measurement-plug-in-converter)
  - [Introduction](#introduction)
  - [Dependencies](#dependencies)
  - [How to install?](#how-to-install)
  - [How to run?](#how-to-run)
    - [Prerequisites](#prerequisites)
    - [Supported data types](#supported-data-types)
    - [Supported instrument drivers](#supported-instrument-drivers)
    - [Additional steps for VISA instruments](#additional-steps-for-visa-instruments)
    - [Event logger](#event-logger)
    - [Limitations](#limitations)

## Introduction

- The Measurement Plug-In Converter is a CLI tool to convert traditional Python measurements into measurement plug-ins.

## Dependencies

- [Python 3.8](https://www.python.org/downloads/release/python-3810/) or later
- NI Measurement Plug-In UI Creator

## How to install?

- Place the UI Creator and the Plug-In Converter wheel files parallel to the [install.bat](../../batch_files/install.bat). You can find the wheel files in the latest release.
- Run the `install.bat` file by double-clicking it.

## How to run?

- Open Command Prompt.
- Run the following command to know the required CLI arguments.

  ```cmd
  ni-measurement-plugin-converter --help
  ```

  ```cmd
  Usage: ni-measurement-plugin-converter [OPTIONS]

    Convert Python measurements to Python Measurement plug-ins.

  Options:
    -d, --display-name TEXT         Display name for the plug-in that will be
                                    converted.  [required]
    -m, --measurement-file-path TEXT
                                    Path of the Python measurement file to be
                                    converted.  [required]
    -f, --function TEXT             Name of the function in the measurement file
                                    that contains the logic for the measurement.
                                    [required]
    -o, --directory-out TEXT        Output directory for measurement plug-in
                                    files.  [required]
    -h, --help                      Show this message and exit.
  ```

- Run the following command to convert Python measurements to measurement plug-ins.

  ```cmd
  ni-measurement-plugin-converter -d "<display_name>" -m "<measurement_file_path>" -f "<measurement_function_name>" -o "<output_directory>"
  ```

### Prerequisites

- The Python measurement should have a measurement function.
- The measurement function should use at least one of the supported [instrument drivers](#supported-instrument-drivers) and [data types](#supported-data-types).
  The inputs and outputs of unsupported data types will be skipped.
- The measurement function must return a value through a variable. Assign the return value to a variable first, and then return that variable.
  Returning a function call or a constant value directly is not supported.

  ```py
  # Unsupported format
  def measurement() -> List[float]:
    # Measurement logic.
    return measure_voltages()

  # Supported format
  def measurement() -> List[float]:
    # Measurement logic.
    voltages = measure_voltages()
    return voltages
  ```

- The measurement function should have clear and accurate type hints for all input and output parameters.

  ```py
  # Unsupported format
  def measurement(voltage, current):
    # Measurement logic.
    resistance = voltage / current
    return resistance
  
  # Supported format
  def measurement(voltage: int, current: float) -> float:
    # Measurement logic.
    resistance = voltage / current
    return resistance
  ```

- The measurement function should have the instrument driver’s session initialization within the measurement function, indented at the next level.

  ```py
  # Unsupported format
  def measurement(voltage: int, current: float) -> float:
    if voltage:
      with nidcpower.Session("DCPower1") as session:
        # Measurement logic.
        return current

  # Supported format
  def measurement(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as session:
      # Measurement logic.
      return current
  ```

- The measurement function should consolidate all instrument driver session initializations at a single point using the `with` context manager.

  ```py
  # Unsupported format
  def measurement(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as dcpower_session:
      with nidmm.Session("DMM1") as dmm_session:
        # Measurement logic.
        return current

  # Unsupported format
  def measurement(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as dcpower_session:
        # Measurement logic.

    with nidmm.Session("DCPower1") as dmm_session:
        # Measurement logic.
    
    return current

  # Supported format
  def measurement(voltage: int, current: float) -> float:
    with nidcpower.Session("DCPower1") as dcpower_session, nidmm.Session("DMM1") as dmm_session:
      # Measurement logic.
      return current
  ```

### Supported data types

- Integer
- Float
- String
- Boolean
- 1D array of the above types

### Supported instrument drivers

- NI-DCPower
- NI-DMM
- NI-Digital Pattern Driver
- NI-FGEN
- NI-SWITCH
- NI-SCOPE
- NI-DAQmx
- NI-VISA

### Additional steps for VISA instruments

For measurements that use VISA instruments, the `session_constructor`, session type and `instrument_type` must be updated with appropriate values.

![VISA_updates](../../docs/images/VISA_updates.png)

Steps to be followed

- Define the gRPC device server support.
- Define the session class for the instrument type.
- Define the session constructor for the instrument type.

  ![VISA_updated](../../docs/images/VISA_updated.png)

- For `session_constructor`, create SessionConstructor object of the instrument driver used.
- For `instrument_type`, use the pin map instrument type id.
- For session type, the type of session should be passed.

For details, refer [Examples](https://github.com/ni/measurement-plugin-python/tree/releases/2.1/examples/nivisa_dmm_measurement).

![VISA_examples](../../docs/images/VISA_examples.png)

### Event logger

- The tool generates a log at the start of the conversion process, recording all actions performed throughout.
- The log file is located in the output directory.
- This log includes detailed information on any errors encountered during the process.

### Limitations

- The tool supports converting only one Python measurement to a plug-in in an execution.
- Class-based measurements are not supported for conversion.
- Data types such as `Path`, `Enum`, `DoubleXYData`, and their array variants are not supported.
- The measurement plug-in UI generated by the tool will exclude controls and indicators for the boolean lists.
- For measurements using VISA instruments, follow the [additional steps](#additional-steps-for-visa-instruments) after conversion.

Note: The `measurement.py` file in the generated plug-in is not formatted using [black](https://pypi.org/project/black/).
  