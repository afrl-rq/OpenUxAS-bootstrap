from __future__ import annotations

import logging
import os
import subprocess

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Dict,
        List,
        Optional,
        Union
    )


class Command:
    def __init__(
        self,
        cmd: Union[str, List[str]],
        description: Optional[str] = None,
        cwd: Optional[str] = None
    ) -> None:
        self.cmd: List[str] = list()

        # Spurious type errors on both branches:
        if type(cmd) is str:
            self.cmd = [cmd]
        else:
            self.cmd = cmd

        self.description = description
        self.cwd = cwd


def format_command(command: Command) -> str:
    if command.cwd is not None:
        return "(cd {} && {})".format(os.path.relpath(command.cwd,
                                                      os.getcwd()),
                                      ' '.join(command.cmd))
    else:
        return ' '.join(command.cmd)


def log_command(command: Command,
                dry_run: Optional[bool] = False) -> int:
    if command.description is not None:
        logging.info(command.description)

    print_cmd = format_command(command)
    logging.debug(print_cmd)

    if dry_run:
        print(print_cmd)
        return 0
    else:
        return subprocess.run(command.cmd, cwd=command.cwd).returncode


def run_command_and_exit_on_fail(command: Command,
                                 dry_run: Optional[bool] = False) -> None:
    result = log_command(command, dry_run)
    if result != 0:
        if command.description is not None:
            logging.critical(command.description + ' failed.')
        else:
            logging.critical(format_command(command) + ' failed.')

        exit(result)
