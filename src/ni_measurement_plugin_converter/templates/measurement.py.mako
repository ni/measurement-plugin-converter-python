<%page args="display_name, version, service_class, serviceconfig_file, resource_name, instrument_type, nims_instrument, input_configurations, output_configurations, input_signature, input_param_names, output_param_types, updated_file_name, method_name, tuple_of_outputs"/>\
\

import pathlib
import sys
from typing import List, Tuple, Iterable
from ${updated_file_name} import ${method_name}

import ni_measurementlink_service as nims

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
    %for input_config in input_configurations:
        %if input_config.nims_type == "nims.DataType.String":
@measurement_service.configuration("${input_config.param_name}", ${input_config.nims_type}, "${input_config.default_value}")
        %else:
@measurement_service.configuration("${input_config.param_name}", ${input_config.nims_type}, ${input_config.default_value})
        %endif
    %endfor
    %for output_config in output_configurations:
@measurement_service.output("${output_config.variable_name}", ${output_config.variable_type})
    %endfor
% if not tuple_of_outputs:
def measure(pin_names: Iterable[str], ${input_signature}) -> Tuple[${output_param_types}]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        return (${method_name}(reservation, ${input_param_names}),)
% else:
def measure(pin_names: Iterable[str], ${input_signature}) -> Tuple[${output_param_types}]:
    with measurement_service.context.reserve_session(pin_names) as reservation:
        return ${method_name}(reservation, ${input_param_names})
%endif
def main() -> None:
    with measurement_service.host_service():
        input("Press enter to close the measurement service.\n")


if __name__ == "__main__":
    main()
