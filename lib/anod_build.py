#!/usr/bin/env python

from __future__ import annotations

from lib.anod.build import UxasBuilder
from lib.anod.util import (check_common_tools, create_anod_context,
                           create_anod_sandbox)
from lib.anod.paths import (REPO_DIR, SPEC_DIR, SBX_DIR)

from e3.anod.context import AnodContext
from e3.anod.sandbox import SandBox
from e3.env import BaseEnv
from e3.main import Main

import os
import sys

from typing import TYPE_CHECKING


# Uxas repo root directory
OPENUXAS_ROOT_DIR = os.path.dirname(REPO_DIR)
os.environ['OPENUXAS_ROOT_DIR'] = OPENUXAS_ROOT_DIR


def do_build(m: Main, set_prog=True) -> int:
    if set_prog:
        m.argument_parser.prog = m.argument_parser.prog + ' build'
    m.argument_parser.add_argument(
        'spec_name', help='spec to build. This is '
        'the basename of an .anod file (without the extension)')
    m.argument_parser.add_argument('--qualifier', help='optional qualifier')
    m.argument_parser.add_argument(
        '--sandbox-dir',
        help='directory in which build artefacts are stored',
        default=SBX_DIR)
    m.argument_parser.add_argument(
        '--force',
        help='force rebuild of everything',
        action="store_true",
        default=False)
    m.parse_args()

    check_common_tools()

    ac = create_anod_context(SPEC_DIR)
    sbx = create_anod_sandbox(m.args.sandbox_dir, SPEC_DIR)

    sbx.create_dirs()

    ac.add_anod_action(name=m.args.spec_name,
                       primitive='build',
                       qualifier=m.args.qualifier,
                       sandbox=sbx,
                       upload=False,
                       env=BaseEnv.from_env())
    actions = ac.schedule(resolver=ac.always_create_source_resolver)

    walker = UxasBuilder(actions, sandbox=sbx, force=m.args.force)

    # TODO: something with walker.job_status['root'], assuming we can get a
    # useful value there. Right now, it's always 'unknown'
    return 0


if __name__ == '__main__':
    exit(do_build(Main(), set_prog=False))
