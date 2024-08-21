"""Implementation of session management."""

import ast
from logging import getLogger
from typing import List, Tuple

import astor

from ni_measurement_plugin_converter.constants import (
    DEBUG_LOGGER,
    ENCODING,
    DebugMessage,
    DriverSession,
    UserMessage,
)
from ni_measurement_plugin_converter.models import UnsupportedDriverError

from ._manage_session_helper import (
    get_plugin_session_initializations,
    get_sessions,
    replace_session_initializations,
)

_RESERVATION = "reservation"
_SESSION_INFO = "session_info"


def manage_session(migrated_file_dir: str, function: str) -> str:
    """Manage session.

    1. Add session reservation variable to migrated file.
    2. Replace session initialization in migrated file.
    3. Insert session assignment into migrated file.

    Args:
        migrated_file_dir (str): Migrated measurement file directory.
        function (str): Measurement function name.

    Returns:
        str: Instrument name.
    """
    logger = getLogger(DEBUG_LOGGER)

    with open(migrated_file_dir, "r", encoding=ENCODING) as file:
        source_code = file.read()

    code_tree = ast.parse(source_code)

    sessions = get_sessions(code_tree, function)
    if not sessions:
        raise UnsupportedDriverError(
            UserMessage.INVALID_DRIVERS.format(
                supported_drivers=[driver.name for driver in DriverSession]
            )
        )

    logger.info(UserMessage.ADD_RESERVE_SESSION)
    reservation_added_code_tree = add_param(
        code_tree=code_tree,
        function=function,
        param=_RESERVATION,
    )
    plugin_session_initializations = get_plugin_session_initializations(
        reservation_added_code_tree, function, sessions
    )
    logger.info(UserMessage.REPLACE_SESSION_INITIALIZATION)
    code_tree = replace_session_initializations(code_tree, function, plugin_session_initializations)

    logger.info(UserMessage.ASSIGN_SESSION_INFO)

    session_inserted_code_tree = insert_session_assignment(
        code_tree=code_tree,
        function=function,
        sessions=sessions,
    )

    code_tree = astor.to_source(session_inserted_code_tree)

    with open(migrated_file_dir, "w", encoding=ENCODING) as file:
        file.write(code_tree)

    logger.debug(DebugMessage.MIGRATED_FILE_MODIFIED)

    return sessions


def add_param(code_tree: ast.Module, function: str, param: str) -> ast.Module:
    """Add a parameter to user measurement function in code tree.

    Args:
        code_tree (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.
        param (str): Parameter to be added.

    Returns:
        ast.Module: Updated measurement function with parameter.
    """
    for node in code_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function:
            node.args.args.insert(0, param)

    return code_tree


def insert_session_assignment(
    code_tree: ast.Module,
    function: str,
    sessions: str,
) -> ast.Module:
    """Insert session assignment into migrated measurement file source code.

    Args:
        source_code (ast.Module): Migrated measurement source code tree.
        function (str): Measurement function name.
        sessions (str): Session name from user measurement.

    Returns:
        ast.Module: Session assignment inserted source code tree.
    """
    session_assignments = []
    for driver, actual_session_names in sessions.items():
        if len(actual_session_names) == 1:
            session_assignments.append(
                ast.Assign(
                    targets=[ast.Name(id=actual_session_names[0], ctx=ast.Store())],
                    value=ast.Attribute(
                        value=ast.Name(id=f"{driver}_{_SESSION_INFO}", ctx=ast.Load()),
                        attr="session",
                        ctx=ast.Load(),
                    ),
                )
            )
        elif len(actual_session_names) > 1:
            for index in range(len(actual_session_names)):
                session_assignments.append(
                    ast.Assign(
                        targets=[ast.Name(id=actual_session_names[index], ctx=ast.Store())],
                        value=ast.Attribute(
                            value=ast.Name(
                                id=f"{driver}_{_SESSION_INFO}s[{index}]", ctx=ast.Load()
                            ),
                            attr="session",
                            ctx=ast.Load(),
                        ),
                    )
                )

    for node in ast.walk(code_tree):
        if isinstance(node, ast.FunctionDef) and node.name == function:
            for child_node in node.body:
                if isinstance(child_node, ast.With):
                    for session_assignment in session_assignments[::-1]:
                        child_node.body.insert(0, session_assignment)

    return code_tree
