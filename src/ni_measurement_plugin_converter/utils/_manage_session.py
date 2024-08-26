"""Implementation of session management."""

import ast
from logging import getLogger
from typing import Dict, List

import astor
import black

from ni_measurement_plugin_converter.constants import (
    DEBUG_LOGGER,
    ENCODING,
    DebugMessage,
    SessionManagement,
    UserMessage,
)
from ni_measurement_plugin_converter.models import UnsupportedDriverError
from ni_measurement_plugin_converter.utils import get_function_node

from ._manage_session_helper import get_plugin_session_initializations, get_sessions_details


def manage_session(migrated_file_dir: str, function: str) -> List[str]:
    """Manage session.

    1. Get sessions details.
    2. Add session reservation variable to migrated file.
    3. Replace session initialization in migrated file.
    4. Insert session assignment into migrated file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function (str): Measurement function name.

    Returns:
        List[str]: VISA instrument driver parameters.
    """
    logger = getLogger(DEBUG_LOGGER)

    measurement_function_node = get_function_node(file_dir=migrated_file_dir, function=function)

    logger.info(UserMessage.EXTRACT_DRIVER_SESSIONS)

    sessions_details = get_sessions_details(function_node=measurement_function_node)
    if not sessions_details:
        raise UnsupportedDriverError(
            UserMessage.INVALID_DRIVERS.format(
                supported_drivers=SessionManagement.NI_DRIVERS + ["VISA"]
            )
        )

    logger.info(UserMessage.ADD_RESERVE_SESSION)

    visa_params = get_visa_params(sessions_details)
    params_added_function = add_params(
        function_node=measurement_function_node,
        params=[SessionManagement.RESERVATION] + visa_params,
    )

    logger.info(UserMessage.REPLACE_SESSION_INITIALIZATION)

    plugin_session_initializations = get_plugin_session_initializations(
        function_node=measurement_function_node
    )
    session_replaced_function = replace_session_initializations(
        function_node=params_added_function,
        session_initializations=plugin_session_initializations,
    )

    logger.info(UserMessage.ASSIGN_SESSION_INFO)
    sessions_assignments = get_session_assignments(sessions_details)
    session_assignment_inserted_function = insert_session_assignment(
        function_node=session_replaced_function,
        sessions_assignments=sessions_assignments,
    )

    with open(migrated_file_dir, "r", encoding=ENCODING) as file:
        source_code = file.read()

    source_code_tree = ast.parse(source_code)

    for node in ast.walk(source_code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            node.args = session_assignment_inserted_function.args
            node.body = session_assignment_inserted_function.body
            break

    source_code = astor.to_source(source_code_tree)
    formatted_code = black.format_str(source_code, mode=black.FileMode())

    with open(migrated_file_dir, "w", encoding=ENCODING) as file:
        file.write(formatted_code)

    logger.debug(DebugMessage.MIGRATED_FILE_MODIFIED)

    return visa_params


def get_visa_params(sessions_details: Dict[str, List[str]]) -> List[str]:
    """Get session_constructor and instrument_type parameters for VISA instruments.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        List[str]: VISA instrument parameters.
    """
    visa_instruments_params = []

    for driver in list(sessions_details.keys()):
        if driver in SessionManagement.NI_DRIVERS:
            continue

        visa_instruments_params.extend(
            [
                f"{driver}_{SessionManagement.SESSION_CONSTRUCTOR}",
                f"{driver}_{SessionManagement.INSTRUMENT_TYPE}",
            ]
        )

    return visa_instruments_params


def add_params(function_node: ast.FunctionDef, params: List[str]) -> ast.FunctionDef:
    """Add parameters to user measurement function.

    Args:
        function_node (ast.FunctionDef): Measurement function code tree.
        params (List[str]): Parameters to be added.

    Returns:
        ast.FunctionDef: Parameters added function code tree.
    """
    for param in params[::-1]:
        function_node.args.args.insert(0, param)

    return function_node


def replace_session_initializations(
    function_node: ast.FunctionDef,
    session_initializations: Dict[str, List[ast.withitem]],
) -> ast.FunctionDef:
    """Replace session initializations with plug-in session initializations.

    Args:
        function_node (ast.FunctionDef): Measurement function code tree.
        session_initializations (Dict[str, List[ast.withitem]]): Session initializations.

    Returns:
        ast.FunctionDef: Session replaced measurement function code tree.
    """
    for child_node in ast.walk(function_node):
        if isinstance(child_node, ast.With) and hasattr(child_node, "items") and child_node.items:
            child_node.items = [withitem for withitem in session_initializations.values()]
            break

    return function_node


def get_session_assignments(sessions_details: Dict[str, List[str]]) -> List[ast.Assign]:
    """Get `Assign` objects to the sessions initialized.

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        List[ast.Assign]: Session `Assign` objects.
    """
    session_assignments = []

    for driver, actual_session_names in sessions_details.items():
        for index in range(len(actual_session_names)):
            session_assignments.append(
                ast.Assign(
                    targets=[ast.Name(id=actual_session_names[index], ctx=ast.Store())],
                    value=ast.Attribute(
                        value=ast.Name(
                            id=f"{driver}_{SessionManagement.SESSION_INFO}[{index}]",
                            ctx=ast.Load(),
                        ),
                        attr="session",
                        ctx=ast.Load(),
                    ),
                )
            )

    return session_assignments


def insert_session_assignment(
    function_node: ast.FunctionDef,
    sessions_assignments: List[ast.Assign],
) -> ast.FunctionDef:
    """Insert session assignment into migrated measurement file source code.

    Args:
        source_code (ast.FunctionDef): Measurement function code tree.
        sessions_details (Dict[str, List[str]]): Sessions details.

    Returns:
        ast.FunctionDef: Session assignment inserted function code tree.
    """
    for child_node in function_node.body:
        if isinstance(child_node, ast.With):
            for session_assignment in sessions_assignments[::-1]:
                child_node.body.insert(0, session_assignment)

    return function_node


def get_param_str(params: List[str]) -> str:
    """Get the VISA instrument parameters string.

    Args:
        params (List[str]): List of VISA parameter string.

    Returns:
        str: VISA instrument parameter string.
    """
    param_str = ""

    for param in params:
        param_str += f"{param}={param}, "

    return param_str
