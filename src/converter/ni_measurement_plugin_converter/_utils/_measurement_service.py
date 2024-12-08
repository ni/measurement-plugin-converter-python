"""Implementation of Get NI Measurement Plug In SDK Service Data type and Instrument."""

import ast
import sys
from typing import Optional, Union

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


def get_nims_datatype(python_native_data_type: str) -> Optional[str]:
    """Get the corresponding `measurement_plugin_sdk_service` data type.

    Args:
        python_native_data_type: Python native data type as a string.

    Returns:
        Corresponding `measurement_plugin_sdk_service` data type.
    """
    try:
        return NIMS_TYPE[python_native_data_type]
    except (KeyError, TypeError):
        return None


def extract_type(node: Union[ast.Name, ast.Subscript, ast.expr, ast.slice, ast.Index]) -> str:
    """Extract data type from the input/output node.

    Args:
        node: Input/output node.

    Returns:
        Data type as string.
    """
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Subscript):
        generic_type = extract_type(node.value)

        slice_value = node.slice

        if hasattr(slice_value, "value"):
            slice_value = slice_value.value

        if sys.version_info >= (3, 9) and isinstance(slice_value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in slice_value.elts]
            return f"{generic_type}[{', '.join(inner_types)}]"

        if isinstance(slice_value, ast.Tuple):
            inner_types = [extract_type(elt) for elt in slice_value.elts]
            return f"{generic_type}[{', '.join(inner_types)}]"

        if isinstance(slice_value, ast.Index):
            return f"{generic_type}[{extract_type(slice_value)}]"

        else:
            return f"{generic_type}[{extract_type(slice_value)}]"

    # Fallback for other node types
    return str(type(node).__name__)
