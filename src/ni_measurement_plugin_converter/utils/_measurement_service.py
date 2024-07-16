"""NI Measurement Service Datatype and Instrument."""

import ast

from ni_measurement_plugin_converter.constants import NIMS_TYPE, DriverSession


def get_nims_datatype(type: str) -> str:
    try:
        return NIMS_TYPE[type]
    except KeyError:
        ...


def get_nims_instrument(instrument_type: str) -> str:
    try:
        return DriverSession[instrument_type].value
    except KeyError:
        ...


def extract_type(node):
    if isinstance(node, ast.Name):
        return node.id

    elif isinstance(node, ast.Subscript):
        generic_type = extract_type(node.value)

        if isinstance(node.slice.value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.value.elts]
            return inner_types

        elif isinstance(node.slice, ast.Index):
            slice_id = extract_type(node.slice.value)
            return f"{generic_type}[{slice_id}]"

        else:
            slice_id = extract_type(node.slice)
            return f"{generic_type}[{slice_id}]"

    else:
        return ""
