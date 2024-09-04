# NI Measurement Plug-In Converter for Python

### Overview

- NI Measurement Plug-In Converter for Python is a CLI tool to convert Python measurements to NI measurement plug-ins.

### Code Setup

- Clone the repository using `git clone <repository link>`.
- Check out to the required branch using `git checkout <branch name>`

### Setup Virtual Environment

- Open terminal.
- Run `cd python-code-migration-utility`
- Run `poetry env use <Python exe path>`
- Run `poetry shell` to activate virtual environment.
- Run `pip install dependencies\<whl files>`.
- Run `poetry install` to install dependency files.

### Installation

- Ensure all the dependency files are placed parallel to `install.bat`
- Run the `install.bat` file by double clicking it.

#### Note

- Require internet access to install the external dependencies of NI Measurement Plug-In Converter.

### Example Usage

- Run `ni-measurement-plugin-converter --help` to know required CLI arguments.

  ```
  Usage: ni-measurement-plugin-converter [OPTIONS]

    NI Measurement Plug-In Converter is a Command Line tool to convert     
    Python measurements to measurement plug-ins.

  Options:
    -d, --display-name TEXT         Display name.  [required]
    -m, --measurement-file-dir TEXT
                                    Measurement file directory.  [required]
    -f, --function TEXT             Measurement function name.  [required]
    -o, --output-dir TEXT           Output directory.  [required]
    -h, --help                      Show this message and exit.
  ```
- Run `ni-measurement-plugin-converter -d <display name> -m <measurement file directory> -f <measurement function name> -o <output directory>` to convert Python measurements to measurement plug-ins.

### Prerequisites

The Python measurement should contain a measurement function which should

  - Use one of the supported drivers and data types. Inputs and outputs of unsupported data types will be skipped.
  - Contain a return value. The return value should be a variable and not a direct function call or constant value.
    ```
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
    ```
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
    ```
    # Not supported
    def measurement_function(voltage: int, current: float) -> float:
      if voltage:
        with nidcpower.Session("DCPower1) as session:
          # Measurement logic.
          return current

    # Supported
    def measurement_function(voltage: int, current: float) -> float:
      with nidcpower.Session("DCPower1) as session:
        # Measurement logic.
        return current
    ```
  - Have all the instrument driver's session initialization at a single point using the context manager `with`
    ```
    # Not supported
    def measurement_function(voltage: int, current: float) -> float:
      with nidcpower.Session("DCPower1) as dcpower_session:
        with nidmm.Session("DMM1) as dmm_session:
          # Measurement logic.
          return current

    # Supported
    def measurement_function(voltage: int, current: float) -> float:
      with nidcpower.Session("DCPower1") as dcpower_session, nidmm.Session("DMM1) as dmm_session:
        return current
    ```
