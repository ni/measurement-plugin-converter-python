<%page args="display_name, version, serviceconfig_file, resource_name, instrument_type, nims_instrument, inputs_info, outputs_info, input_signature, input_param_names, output_signature, migrated_file, function_name, iterable_outputs"/>\
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
    nims.DataType.PinArray1D,
    ["${resource_name}"],
    instrument_type=${nims_instrument},
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
% if not iterable_outputs:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        return (${function_name}(reservation, ${input_param_names}),)
% else:
def measure(pin_names: Iterable[str], ${input_signature}) -> Iterable[Union[${output_signature}]]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        return ${function_name}(reservation, ${input_param_names})
%endif
def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
