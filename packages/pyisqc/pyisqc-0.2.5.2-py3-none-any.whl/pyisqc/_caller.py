from __future__ import annotations

import configparser
import logging
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

from rich.console import Console
from rich.table import Table

from ._about import __version__
from ._downloader import Downloader


class Caller:
    def __init__(self, mute=False):
        localConfig = self._getLocalConfig()
        if localConfig is None:
            # no local config, try to create a new one
            console = Console()
            # (1) first try searching isqc in env
            isqc_env = self._search_isqc_by_which()
            if isqc_env is None:
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column(
                    "   :exclamation_mark: 输入回车直接跳过 (press enter if unconcerned)",
                    overflow="fold",
                )
                printStr = (
                    "地本没有找到isqc，如果您确认安装了isqc，请输入路径:\n"
                    "(输入的是[cyan]可执行文件[/cyan]的路径,不是[red]所在目录[/red]的路径，\n"
                    "直接回车将会自动为您下载并安装一个isqc)\n"
                    "--------------------------------------------\n"
                    "isqc not found. Provide the path if you have it installed: \n"
                    "(Enter path of isqc [cyan]executable file[/cyan], not the [red]directory[/red] it located,\n"
                    "enter empty to download one for you)"
                )
                table.add_row(
                    printStr,
                )
                console.print(table)

                while True:
                    enter = input(
                        "请输入(Please input):\n"
                    )
                    if enter != "":
                        if self.is_valid_isqc(enter):
                            bin = enter
                            break
                        else:
                            console.print(
                                f"[yellow]{enter}[/yellow] [red]is not a valid path, please try again.[/red]"
                            )
                    else:
                        bin = self._getBinByDownload()
                        break
            else:
                logging.info(f"isqc is found at {isqc_env}, use this one.")
                bin = isqc_env
            # (2) ask for auto downloading
            self.bin = bin
            self._saveLocalConfig(data={"config": {"bin": self.bin}})
        else:
            self.bin = localConfig["config"]["bin"]

    def getIsqcDir(self):
        return os.path.dirname(self.bin)

    @staticmethod
    def _getBinByDownload() -> str:
        # ----------
        isqVersion = __version__[:-2]
        # url = "http://192.168.1.32:8000/isqc-0.2.5.tar.gz"
        url = f"https://www.arclightquantum.com/isq-releases/isqc-standalone/{isqVersion}/isqc-{isqVersion}.tar.gz"
        dlFileName = f"isqc-{isqVersion}.tar.gz"
        isqcDir = os.path.join(Path.home(), f"isqc-{isqVersion}")
        # ----------
        if not os.path.exists(isqcDir):
            os.makedirs(isqcDir)
        console = Console()
        console.print(f"[green] isqc -> <{isqcDir}>, downloading...[/green]")
        with tempfile.TemporaryDirectory() as tmp:
            dirPath = tmp
            destPath = os.path.join(dirPath, dlFileName)
            Downloader.downloadSingleFile(url=url, destPath=dirPath)
            tar = tarfile.open(destPath, "r:gz")
            os.chdir(isqcDir)
            tar.extractall()
            tar.close()
        return os.path.join(isqcDir, "isqc")

    def rcmd(self, rcmd_args: list[str], pwd: str | None = None, **kw):
        cmd_args = [self.bin] + rcmd_args
        pipes = subprocess.Popen(
            cmd_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        std_out, std_err = pipes.communicate()
        return pipes.returncode, std_out.decode("utf-8"), std_err.decode("utf-8")

    @staticmethod
    def is_valid_isqc(binPath: str):
        cmd = f"{binPath} -V"
        stdout = os.popen(cmd).read().strip()
        return stdout[:12] == "isQ Compiler"

    @staticmethod
    def _getlocalConfigFilePath() -> str:
        configDir = os.path.join(Path.home(), ".config")
        if not os.path.exists(configDir):
            os.makedirs(configDir)
        configFilePath = os.path.join(configDir, ".pyisqc")
        return configFilePath

    @classmethod
    def _getLocalConfig(cls) -> dict:
        configFilePath = cls._getlocalConfigFilePath()
        if os.path.exists(configFilePath):
            config = configparser.ConfigParser()
            config.read(configFilePath)
            res = {}
            for section in config:
                if section.upper() != "DEFAULT":
                    res[section] = dict(config[section])
            return res
        else:
            return None

    @classmethod
    def _saveLocalConfig(cls, data: dict):
        configFilePath = cls._getlocalConfigFilePath()
        parser = configparser.ConfigParser()
        for section in data:
            parser.add_section(section)
            for key in data[section]:
                parser.set(section, key, data[section][key])
        with open(configFilePath, "w") as f:
            parser.write(f)

    @classmethod
    def _search_isqc_by_which(cls):
        isqc = shutil.which("isqc")
        if isqc is not None and cls.is_valid_isqc(isqc):
            return isqc
        return None
