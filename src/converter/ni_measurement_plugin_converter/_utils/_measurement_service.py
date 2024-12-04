"""Implementation of Get NI Measurement Plug In SDK Service Data type and Instrument."""

import ast
import sys
from typing import Union

# Python native data types and its corresponding `measurement_plugin_sdk_service` data types.
NIMS_TYPE = {
    "int": "nims.DataType.Int64",
    "float": "nims.DataType.Double",
    "str": "nims.DataType.String",
    "bool": "nims.DataType.Boolean",
    "List[int]": "nims.DataType.Int64Array1D",
    "List[float]": "nims.DataType.DoubleArray1D",
    "List[str]": "nims.DataType.StringArray1D",
    "List[bool]": "nims.DataType.BooleanArray1D",
}


def get_nims_datatype(python_native_data_type: str) -> str:
    """Get `measurement_plugin_sdk_service` data type.

    Args:
        python_native_data_type (str): Python native data type.

    Returns:
        str: Corresponding `measurement_plugin_sdk_service` data type.
    """
    try:
        return NIMS_TYPE[python_native_data_type]
    except (KeyError, TypeError):
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

        if sys.version_info >= (3, 9) and isinstance(node.slice, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.elts]
            return inner_types

        if isinstance(node.slice.value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in node.slice.value.elts]
            return inner_types

        if isinstance(node.slice, ast.Index):
            slice_id = extract_type(node.slice.value)
            return f"{generic_type}[{slice_id}]"

        else:
            slice_id = extract_type(node.slice)
            return f"{generic_type}[{slice_id}]"
