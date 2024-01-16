from __future__ import annotations

import os
from collections.abc import Sequence

from ._caller import Caller


def run(
    file: str,
    shots: int = 100,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    # TODO: additional_args: str = "",
) -> tuple[int, str, str]:
    """This function encapsulates the ``simulate`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        shots: Shots number of quantum simulation.
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        additional_args: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    """

    cmd_list = ["run"]
    cmd_list.append(os.path.expanduser(file))
    if int_param is not None:
        for i in int_param:
            cmd_list.append("-i")
            cmd_list.append(str(i))
    if double_param is not None:
        for d in double_param:
            cmd_list.append("-d")
            cmd_list.append(str(d))
    cmd_list.append("--shots")
    cmd_list.append(str(shots))

    return Caller().rcmd(cmd_list)
