# -*- coding: utf-8 -*-

"""Console script for python_url_shortener."""
import sys
import typing

import click


@click.command()
def main(args: typing.Optional[str] = None) -> int:
    """ Console script for the url shortener service.
        Here, other useful tasks can be performed with cli arguments such as processing data etc
    """
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
