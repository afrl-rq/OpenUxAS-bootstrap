from __future__ import annotations

import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from argparse import Namespace

STREAM_FMT = "%(levelname)-8s %(message)s"
FILE_FMT = "%(asctime)s: %(name)-24s: %(levelname)-8s %(message)s"


def configure_logging(args: Namespace) -> None:
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose == 2:
        level = logging.DEBUG
    else:
        level = args.loglevel

    logging.getLogger("").setLevel(logging.DEBUG)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(logging.Formatter(STREAM_FMT))
    streamHandler.setLevel(level)
    logging.getLogger("").addHandler(streamHandler)

    if args.log_file:
        fileHandler = logging.FileHandler(args.log_file)
        fileHandler.setFormatter(logging.Formatter(FILE_FMT))
        fileHandler.setLevel(min(level, logging.DEBUG))
        logging.getLogger("").addHandler(fileHandler)


def fix_e3_loglevel(args: Namespace) -> None:
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose == 2:
        level = logging.DEBUG
    else:
        level = logging.ERROR

    logging.getLogger("").handlers[0].setLevel(level)
