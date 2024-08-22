# Changelog

All notable change to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## NI Measurement Plug-In Converter

## [1.0.0-dev6] - 2024-08-23

### Changed

- Print absolute path for output directory.
- Dependency whl files.
- Updated spacing according to ni_measurement_ui_creator-1.0.0.dev6

## [1.0.0-dev5] - 2024-08-12

### Added

- Support for NI-VISA instrument driver.

### Fixed

- Error due to skipped input arguments in user measurement function.

### Changed

- Error handling - print the logger file location in case of exceptions.
- `Float` and `FloatArray1D` to `Double` and `DoubleArray1D` to leverage their higher bitness and precision.

## [1.0.0-dev4] - 2024-08-09

### Added

- Integrate MeasUI Creator with `NI Measurement Plug-In Converter` tool for generating `.measui` file.

## [1.0.0-dev3] - 2024-08-05

### Added

- Support for NI-DAQmx instrument driver.

### Changed

- Handling of unsupported data types. Inform users about unsupported inputs and outputs.

## [1.0.0-dev2] - 2024-07-31

### Added

- Support for NI-Digital, NI-Switch, NI-FGEN and NI-Scope instrument drivers.

## [1.0.0-dev1] - 2024-07-24

### Added

- Support for NI-DMM instrument driver.

## [1.0.0-dev0] - 2024-07-19

### Added

- Support for integer, float, string, boolean and the corresponding array data types.
- Support for NI-DCPower instrument driver.
