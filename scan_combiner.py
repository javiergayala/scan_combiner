#!/usr/bin/env python3
"""
Script to combine two separate PDFs from scans of odd pages and even
pages.
"""

__author__ = "Javier Ayala"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
from logzero import logger
from pikepdf import Pdf

cli_args = None


def main(_cli_args=cli_args):
    """Main entry point of the app"""
    logger.info("Beginning PDF Merge")
    logger.info(_cli_args)
    _pageno = 1
    try:
        logger.info(f"Opening odd: {_cli_args.odd.name}")
        _odd = Pdf.open(_cli_args.odd.name)
        logger.info(f"Opening even: {_cli_args.even.name}")
        _even = Pdf.open(_cli_args.even.name)
        logger.info("Reversing the Even/Backside Pages")
        _even.pages.reverse()
    except Exception as _e:
        print(f"Exception: {_e}")
    for _p, p_data in enumerate(_even.pages):
        _odd.pages.insert(_pageno, p_data)
        _pageno += 2
    logger.info(f"Saving to {_cli_args.output_file.name}")
    _odd.save(_cli_args.output_file.name)
    logger.info("Done!")


if __name__ == "__main__":
    """This is executed when run from the command line"""
    parser = argparse.ArgumentParser()

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    # Add positional argument for Odd pages
    parser.add_argument("odd", type=open)

    # Add positional argument for Even pages
    parser.add_argument("even", type=open)

    # Add optional argument to name the output file
    parser.add_argument(
        "-o",
        "--output-file",
        type=argparse.FileType("w", encoding="utf-8"),
        required=True,
    )

    cli_args = parser.parse_args()
    main(cli_args)
