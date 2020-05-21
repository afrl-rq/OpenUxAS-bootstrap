from __future__ import annotations

from argparse import ArgumentParser
import logging


def add_logging_group(argument_parser: ArgumentParser) -> None:
    log_group = argument_parser.add_argument_group(title='logging arguments')
    log_group.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='make the log output on the console more verbose',
    )
    log_group.add_argument(
        '--log-file',
        metavar='FILE',
        default=None,
        help='store all the logs into the specified file',
    )
    log_group.add_argument(
        '--loglevel',
        default=logging.ERROR,
        help='set the console log level',
        choices={
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARN': logging.WARN,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL,
        },
    )


def add_interactive_group(argument_parser: ArgumentParser) -> None:
    interactive_group = argument_parser.add_mutually_exclusive_group()
    interactive_group.add_argument(
        '--interactive',
        action='store_true',
        default=True,
        help='run in interactive mode: ask before executing all actions',
    )
    interactive_group.add_argument(
        '--automatic',
        action='store_false',
        dest='interactive',
        help='run in automatic mode',
    )


def add_update_group(argument_parser: ArgumentParser) -> None:
    update_group = argument_parser.add_mutually_exclusive_group()
    update_group.add_argument(
        '--update',
        dest='update_apt',
        action='store_true',
        default=True,
        help='update apt',
    )
    update_group.add_argument(
        '--no-update',
        dest='update_apt',
        action='store_false',
        help='do not update apt',
    )


def add_package_group(argument_parser: ArgumentParser) -> None:
    package_group = argument_parser.add_mutually_exclusive_group()
    package_group.add_argument(
        '--packages',
        dest='install_packages',
        action='store_true',
        default=True,
        help='install packages needed by e3-core',
    )
    package_group.add_argument(
        '--no-packages',
        dest='install_packages',
        action='store_false',
        help='do not install packages needed by e3-core',
    )


def add_dry_run_argument(argument_parser: ArgumentParser) -> None:
    argument_parser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        default=False,
        help='print out actions to be taken, but do not make any changes'
    )


def add_print_env_argument(argument_parser: ArgumentParser) -> None:
    argument_parser.add_argument(
        '--print-env',
        action='store_true',
        default=False,
        help='print out the environment for the tools installed and quit')
