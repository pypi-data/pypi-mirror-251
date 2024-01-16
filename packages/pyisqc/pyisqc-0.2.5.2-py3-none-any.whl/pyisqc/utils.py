from __future__ import annotations

import logging
import os
from collections.abc import Sequence

from ._caller import Caller


class FindSimulator:
    """To build a SIMULATOR BIN for isqc."""

    def __init__(self) -> None:
        self.makeSimulatorBIN()

    @staticmethod
    def set_simulator_file_name():
        return "SIMULATOR"

    @staticmethod
    def get_dir_name_of_simulator(isqcDIR):
        storeDIR = os.path.join(isqcDIR, "nix", "store")
        messList = os.listdir(storeDIR)
        for line in messList:
            if "simulator" in line:
                return line.strip()
        logging.error("cannot find simulator dir")

    @staticmethod
    def get_isQ_dir():
        return Caller().getIsqcDir()

    @classmethod
    def get_simulatorBIN_path(cls):
        return os.path.join(cls.get_isQ_dir(), cls.set_simulator_file_name())

    @classmethod
    def makeSimulatorBIN(cls):
        # will automatically find dir of isqc, and make a SIMULATOR with
        # appropriate chmod
        simBinFile = cls.get_simulatorBIN_path()
        if os.path.exists(simBinFile):
            return
        isQdir = cls.get_isQ_dir()
        messName = cls.get_dir_name_of_simulator(isQdir)
        # replaceKeyWord = f"/nix/store/{messName}/bin/simulator"
        isqcFile = os.path.join(isQdir, "isqc")
        with open(isqcFile, "r") as f:
            isqcContent = f.read()
        slides = isqcContent.split(" ")
        slides[-2] = f"/nix/store/{messName}/bin/simulator"
        simBINcontent = " ".join(slides)
        with open(simBinFile, "w") as f:
            f.write(simBINcontent)
        os.chmod(simBinFile, 0o555)
