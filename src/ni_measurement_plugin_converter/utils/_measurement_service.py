"""Implementation of Get NI Measurement Plug In SDK Service Data type and Instrument."""

import ast
from typing import Union

from ni_measurement_plugin_converter.constants import NIMS_TYPE, DriverSession


def get_nims_datatype(python_native_data_type: str) -> str:
    """Get `measurement_plugin_sdk_service` data type.

    Args:
        python_native_data_type (str): Python native data type.

    Returns:
        str: Corresponding `measurement_plugin_sdk_service` data type.
    """
    try:
        return NIMS_TYPE[python_native_data_type]
    except KeyError:
        pass


def get_nims_instrument(instrument_type: str) -> str:
    """Get `measurement_plugin_sdk_service` instruments.

    Args:
        instrument_type (str): Instrument type.

    Returns:
        str: Corresponding `measurement_plugin_sdk_service` instrument.
    """
    try:
        return DriverSession[instrument_type].value
    except KeyError:
        pass


def extract_type(node: Union[ast.Name, ast.Subscript]) -> str:
    """Extract data type from the input/output node.

    Args:
        node (Union[ast.Name, ast.Subscript]): Input/output node.

    Returns:
        str: Data type.
    """
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Subscript):
        generic_type = extract_type(node.value)

        if isinstance(node.slice.value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.value.elts]
            return inner_types

        if isinstance(node.slice, ast.Index):
            slice_id = extract_type(node.slice.value)
            return f"{generic_type}[{slice_id}]"

        else:
            slice_id = extract_type(node.slice)
            return f"{generic_type}[{slice_id}]"
