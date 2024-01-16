from __future__ import annotations

import os
from collections.abc import Sequence
from typing import Literal

from ._caller import Caller
from .utils import FindSimulator

TARGET = Literal["qir", "open-qasm3", "qcis"]


def compile(
    file: str,
    target: TARGET = "qir",
    int_param: Sequence[int] | None = None,
    double_param: Sequence[float] | None = None,
    output: str | None = None,
    **kwargs,  # TODO:extra args
) -> tuple[int, str, str]:
    """This function encapsulates the ``compile`` of isQ compiler.

    Args:
        file: The path to the file that needs to be compiled.
        target: The compiled target output form:
                1) qir;
                2) open-qasm3;
                3) qcis.
        int_param: An integer variable (array) passed in when compiling.
        double_param: An double variable (array) passed in when compiling.
        output: The name of the output file.
        kwargs: Other arguments passed in when compiling, see more:
                         https://www.arclightquantum.com/isq-docs/latest/

    """

    cmd_list = ["compile"]
    cmd_list.append(os.path.expanduser(file))
    cmd_list.append("--target")
    cmd_list.append(str(target))
    if int_param is not None:
        for i in int_param:
            cmd_list.append("-i")
            cmd_list.append(str(i))
    if double_param is not None:
        for d in double_param:
            cmd_list.append("-d")
            cmd_list.append(str(d))
    cmd_list.append("--output")
    cmd_list.append(str(output))

    # TODO: kwargs
    return Caller().rcmd(cmd_list)


def _gen_qcis_from_so(
    file: str,
    int_param: Sequence[int] | int | None = None,
    double_param: Sequence[float] | float | None = None,
    # additional_args: str = "",
    # TODO: addtional
) -> str:
    """According to the compilation plan of isQ compiler, this function is not
    open to users.
    """

    FindSimulator.makeSimulatorBIN()
    simulator_exec = FindSimulator.get_simulatorBIN_path()

    cmd_list = [str(simulator_exec)]
    cmd_list.append(os.path.expanduser(file))
    cmd_list.append("--qcisgen")
    cmd_list.append("-e")
    cmd_list.append("__isq__entry")

    if int_param is not None:
        for i in int_param:
            cmd_list.append("-i")
            cmd_list.append(str(i))
    if double_param is not None:
        for d in double_param:
            cmd_list.append("-d")
            cmd_list.append(str(d))

    # NOTE: using popen, cannot use rcmd
    return os.popen(" ".join(cmd_list)).read()
