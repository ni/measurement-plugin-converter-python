<%page args="display_name, pins_info, relays_info, session_mappings, pin_and_relay_signature, pin_or_relay_names, session_initializations, serviceconfig_file, inputs_info, outputs_info, input_signature, input_param_names, is_visa, migrated_file, function_name, iterable_outputs"/>
import pathlib
import sys
from typing import List
from ${migrated_file} import ${function_name}

import ni_measurement_plugin_sdk_service as nims

script_or_exe = sys.executable if getattr(sys, "frozen", False) else __file__
service_directory = pathlib.Path(script_or_exe).resolve().parent
measurement_service = nims.MeasurementService(
    service_config_path=service_directory / "${serviceconfig_file}",
    ui_file_paths=[service_directory / "${display_name}.measui"],
)

@measurement_service.register_measurement
% for pin_info in pins_info:
@measurement_service.configuration("${pin_info.name}", nims.DataType.IOResource, "${pin_info.default_value}", instrument_type=${pin_info.instrument_type})
% endfor
% for relay_info in relays_info:
@measurement_service.configuration("${relay_info.name}", nims.DataType.String, "${relay_info.default_value}")
%endfor
% for input_info in inputs_info:
    % if input_info.nims_type == "nims.DataType.String":
@measurement_service.configuration("${input_info.param_name}", ${input_info.nims_type}, "${input_info.default_value}")
    % else:
@measurement_service.configuration("${input_info.param_name}", ${input_info.nims_type}, ${input_info.default_value})
    % endif
% endfor
% for output_info in outputs_info:
@measurement_service.output("${output_info.variable_name}", ${output_info.nims_type})
% endfor
% if not iterable_outputs and not is_visa:
def measure(${pin_and_relay_signature}, ${input_signature}):
    pin_or_relay_names = [${pin_or_relay_names}]

    with measurement_service.context.reserve_sessions(pin_or_relay_names) as reservation:
        with ${session_initializations}:
            % for session in session_mappings:
            ${session.name} = ${session.mapping}
            % endfor
            return (${function_name}(${sessions}, ${input_param_names}),)

% elif not iterable_outputs and is_visa:
def measure(${pin_and_relay_signature}, ${input_signature}):
    pin_or_relay_names = [${pin_or_relay_names}]

    # Update session_constructor object, instrument_types and Session type accordingly.

    with measurement_service.context.reserve_sessions(pin_or_relay_names) as reservation:
        with ${session_initializations}:
            % for session in session_mappings:
            ${session.name} = ${session.mapping}
            % endfor
            return (${function_name}(${sessions}, ${input_param_names}),)

% elif iterable_outputs and not is_visa:
def measure(${pin_and_relay_signature}, ${input_signature}):
    pin_or_relay_names = [${pin_or_relay_names}]

    with measurement_service.context.reserve_sessions(pin_or_relay_names) as reservation:
        with ${session_initializations}:
            % for session in session_mappings:
            ${session.name} = ${session.mapping}
            % endfor
            return ${function_name}(${sessions}, ${input_param_names})

% elif iterable_outputs and is_visa:
def measure(${pin_and_relay_signature}, ${input_signature}):
    pin_or_relay_names = [${pin_or_relay_names}]

    # Update session_constructor object, instrument_types and Session type accordingly.

    with measurement_service.context.reserve_sessions(pin_or_relay_names) as reservation:
        with ${session_initializations}:
            % for session in session_mappings:
            ${session.name} = ${session.mapping}
            % endfor
            return ${function_name}(${sessions}, ${input_param_names})
% endif

def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")

if __name__ == "__main__":
    main()
