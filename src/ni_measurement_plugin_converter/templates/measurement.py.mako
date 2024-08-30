<%page args="display_name, version, serviceconfig_file, inputs_info, outputs_info, input_signature, input_param_names, output_signature, visa_params, migrated_file, function_name, iterable_outputs"/>\
\

import pathlib
import sys
from typing import Iterable, List, Union
from ${migrated_file} import ${function_name}

import ni_measurement_plugin_sdk_service as nims

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "${serviceconfig_file}",
    version="${version}",
    ui_file_paths=[service_directory / "${display_name}.measui"],
)


@measurement_service.register_measurement
@measurement_service.configuration(
    "pin_names",
    nims.DataType.IOResourceArray1D,
    ["Pin1"],
)
    %for input_info in inputs_info:
        %if input_info.nims_type == "nims.DataType.String":
@measurement_service.configuration("${input_info.param_name}", ${input_info.nims_type}, "${input_info.default_value}")
        %else:
@measurement_service.configuration("${input_info.param_name}", ${input_info.nims_type}, ${input_info.default_value})
        %endif
    %endfor
    %for output_info in outputs_info:
@measurement_service.output("${output_info.variable_name}", ${output_info.nims_type})
    %endfor
% if not iterable_outputs and not visa_params:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_sessions(pin_names) as reservation:
        # update sessions_and_resources with session variables and its corresponding resource names.
        # Example sessions_and_resources = {'dcpower_session': 'DCPower', 'dmm_session': 'DMM'}
        sessions_and_resources = {}
        return (${function_name}(reservation=reservation, sessions_and_resources=sessions_and_resources, ${input_param_names}),)

% elif not iterable_outputs and visa_params:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_sessions(pin_names) as reservation:
        # update sessions_and_resources with session variables and its corresponding resource names.
        # Example sessions_and_resources = {'dcpower_session': 'DCPower', 'dmm_session': 'DMM'}
        sessions_and_resources = {}
        # Update session_constructor object and instrument_types accordingly.
        return (${function_name}(reservation=reservation, sessions_and_resources=sessions_and_resources, ${visa_params} ${input_param_names}),)

% elif iterable_outputs and not visa_params:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_sessions(pin_names) as reservation:
        # update sessions_and_resources with session variables and its corresponding resource names.
        # Example sessions_and_resources = {'dcpower_session': 'DCPower', 'dmm_session': 'DMM'}
        sessions_and_resources = {}
        return ${function_name}(reservation=reservation, sessions_and_resources=sessions_and_resources, ${input_param_names})

% elif iterable_outputs and visa_params:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_sessions(pin_names) as reservation:
        # update sessions_and_resources with session variables and its corresponding resource names.
        # Example sessions_and_resources = {'dcpower_session': 'DCPower', 'dmm_session': 'DMM'}
        sessions_and_resources = {}
        # Update session_constructor object and instrument_types accordingly.
        return ${function_name}(reservation=reservation, sessions_and_resources=sessions_and_resources, ${visa_params} ${input_param_names})
%endif
def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
