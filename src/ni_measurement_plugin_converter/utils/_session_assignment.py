import ast
import itertools
from typing import Dict, List, Union

from ni_measurement_plugin_converter.constants import SessionManagement


def get_combined_session_info(sessions_details: Dict[str, List[str]]) -> ast.Assign:
    """Get combined session info.

    1. Get all driver's session_info variables in a list.
    2. Return the list as `ast.Assign` object.

    Args:
        sessions_details (Dict[str, List[str]]):

    Returns:
        ast.Assign: Assignment object of the combined session info.
    """
    combined_session_info = [
        f"{driver}_{SessionManagement.SESSION_INFO}" for driver in sessions_details.keys()
    ]

    # Initialize the base of the expression
    expr = ast.Name(id=combined_session_info[0], ctx=ast.Load())

    # Combine variables using addition
    for var in combined_session_info[1:]:
        expr = ast.BinOp(left=expr, op=ast.Add(), right=ast.Name(id=var, ctx=ast.Load()))

    # Create the assignment node
    assignment = ast.Assign(
        targets=[ast.Name(id=SessionManagement.ALL_SESSIONS_INFO, ctx=ast.Store())],
        value=expr,
    )

    return assignment


def get_session_mapping_logic() -> List[Union[ast.Assign, ast.For]]:
    """Get session mapping logic.

    1. Map the session objects to its respective variables.
    2. Return the logic as a code tree.

    Returns:
        List[ast.Assign, ast.For]: Session mapping logic code tree.
    """
    body = [
        get_dict_assignment(),
        ast.For(
            target=ast.Name(id=SessionManagement.SESSION_VAR, ctx=ast.Store()),
            iter=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id=SessionManagement.SESSIONS_AND_RESOURCES, ctx=ast.Load()),
                    attr="keys",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            ),
            body=[get_inner_for_loop_logic()],
            orelse=[],
        ),
    ]

    return body


def get_dict_assignment() -> ast.Assign:
    """Get dictionary ast.Assign object.

    1. Create a empty dictionary.
    2. Return the assignment of empty dictionary to `session_values` as ast.Assign.

    Returns:
        ast.Assign: Empty dictionary assignment object.
    """
    empty_dict_ast = ast.Dict(keys=[], values=[])
    return ast.Assign(
        targets=[ast.Name(id=SessionManagement.SESSION_VALUES, ctx=ast.Store())],
        value=empty_dict_ast,
    )


def get_inner_for_loop_logic() -> ast.For:
    """Return inner for loop logic for session mapping.

    Returns:
        ast.For: Inner for loop logic.
    """
    return ast.For(
        target=ast.Name(id=SessionManagement.SESSION_INFO, ctx=ast.Store()),
        iter=ast.Name(id=SessionManagement.ALL_SESSIONS_INFO, ctx=ast.Load()),
        body=[get_condition_check_logic()],
        orelse=[],
    )


def get_condition_check_logic() -> ast.If:
    """Get condition check logic for session mapping.

    Returns:
        ast.If: If condition check and session mapping assignment logic as ast code tree.
    """
    return ast.If(
        test=ast.Compare(
            left=ast.Attribute(
                value=ast.Name(id=SessionManagement.SESSION_INFO, ctx=ast.Load()),
                attr="resource_name",
                ctx=ast.Load(),
            ),
            ops=[ast.Eq()],
            comparators=[
                ast.Subscript(
                    value=ast.Name(id=SessionManagement.SESSIONS_AND_RESOURCES, ctx=ast.Load()),
                    slice=ast.Index(
                        value=ast.Name(id=SessionManagement.SESSION_VAR, ctx=ast.Load())
                    ),
                    ctx=ast.Load(),
                )
            ],
        ),
        body=[get_mapped_session_assignment_logic(), ast.Break()],
        orelse=[],
    )


def get_mapped_session_assignment_logic() -> ast.Assign:
    """Get mapped session assignment logic.

    Returns:
        ast.Assign: Session mapping assignment object.
    """
    return ast.Assign(
            targets=[
                ast.Subscript(
                    value=ast.Name(id=SessionManagement.SESSION_VALUES, ctx=ast.Store()),
                    slice=ast.Index(
                        value=ast.Name(id=SessionManagement.SESSION_VAR, ctx=ast.Load())
                    ),
                    ctx=ast.Store(),
                )
            ],
            value=ast.Attribute(
                value=ast.Name(id=SessionManagement.SESSION_INFO, ctx=ast.Load()),
                attr="session",
                ctx=ast.Load(),
            ),
        )


def get_session_mapping_assignment(sessions_details: Dict[str, List[str]]) -> List[ast.Assign]:
    """Get session mapping assignment.

    1. Assign session objects to session variables.
    2. Return the assignments as ast.Assign

    Args:
        sessions_details (Dict[str, List[str]]): Session details.

    Returns:
        List[ast.Assign]: Session assignments objects.
    """
    session_assignments = []

    session_vars = list(itertools.chain.from_iterable(list(sessions_details.values())))

    for session_var in session_vars:
        session_assignments.append(
            ast.Assign(
                targets=[ast.Name(id=f"{session_var}", ctx=ast.Store())],
                value=ast.Subscript(
                    value=ast.Name(id=SessionManagement.SESSION_VALUES, ctx=ast.Load()),
                    slice=ast.Index(value=ast.Constant(value=f"{session_var}")),
                    ctx=ast.Load(),
                ),
            )
        )

    return session_assignments
