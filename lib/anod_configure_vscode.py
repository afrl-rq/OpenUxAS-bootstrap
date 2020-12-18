#!/usr/bin/env python3

"""Anod vscode configurator."""

from __future__ import annotations

from lib.anod.util import check_common_tools, create_anod_context, create_anod_sandbox
from lib.anod.paths import SPEC_DIR, SBX_DIR

from e3.main import Main
from e3.env import BaseEnv

import logging
import os
import pathlib


# Template for the c_cpp_properties.json file we generate
C_CPP_PROPERTIES_JSON = """\
{
    "configurations": [
        {
            "name": "OpenUxAS",
            "includePath": [
                "${workspaceFolder}/**",
                "%s"
            ],
            "defines": [],
            "compilerPath": "/usr/bin/gcc",
            "cStandard": "gnu11",
            "cppStandard": "gnu++11",
            "intelliSenseMode": "gcc-x64"
        }
    ],
    "version": 4
}
"""

DEFAULT_PATH = "develop/OpenUxAS/.vscode/c_cpp_properties.json"


def do_configure(m: Main, set_prog: bool = True) -> int:
    """Create the configuration file for VS Code."""
    if set_prog:
        m.argument_parser.prog = m.argument_parser.prog + " configure-vscode"

    m.argument_parser.add_argument(
        "spec_name",
        nargs="?",
        help="spec for which the VS Code configuration should be generated",
        default="uxas",
    )

    m.argument_parser.add_argument("--qualifier", help="optional qualifier")
    m.argument_parser.add_argument(
        "--sandbox-dir",
        help="directory in which build artifacts are stored",
        default=SBX_DIR,
    )

    output_group = m.argument_parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "--stdout",
        help="print the configuration file to STDOUT",
        action="store_true",
        default=False,
    )

    output_group.add_argument(
        "--out", help="specify the output file", default=DEFAULT_PATH
    )

    m.parse_args()

    # Disable logging messages except errors
    logging.getLogger("").setLevel(logging.ERROR)

    check_common_tools()

    ac = create_anod_context(SPEC_DIR)
    sbx = create_anod_sandbox(m.args.sandbox_dir, SPEC_DIR)

    anod_instance = ac.add_anod_action(
        name=m.args.spec_name,
        primitive="build",
        qualifier=m.args.qualifier,
        sandbox=sbx,
        upload=False,
        env=BaseEnv.from_env(),
    ).anod_instance

    if hasattr(anod_instance, "build_setenv"):
        anod_instance.build_setenv()

        config_content = C_CPP_PROPERTIES_JSON % '",\n                "'.join(
            os.environ["CPLUS_INCLUDE_PATH"].split(os.pathsep)
        )

        if m.args.stdout:
            print(config_content)
        else:
            abspath = os.path.abspath(m.args.out)

            if not os.path.exists(os.path.dirname(abspath)):
                pathlib.Path(os.path.dirname(abspath)).mkdir(parents=True)

            open(abspath, "w").write(config_content)

        return 0
    else:
        logging.error(
            f"Cannot generate a VS Code configuration for {m.args.spec_name} "
            "because it does not export a build_setenv"
        )

        return 1
