# -*- coding: utf-8 -*-

"""Command line interface for :mod:`pubquiz`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m pubquiz`` python will execute``__main__.py`` as a script.
  That means there won't be any ``pubquiz.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``pubquiz.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import logging
import subprocess

import click

from pubquiz import Quiz

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
def main():
    """CLI for pubquiz."""


valid_outputs = ["sheets", "slides"]


# Make a pub quiz from a yaml file
@main.command()
@click.argument("yaml_file", type=click.Path(exists=True))
@click.argument("output", type=click.Choice(valid_outputs + ["all"]), default="all")
@click.option("--no-compile", is_flag=True, default=False, help="Do not compile the output files.")
def make(yaml_file, output, no_compile):
    """Make a pub quiz from a yaml file."""
    if output == "all":
        outputs = valid_outputs
    else:
        outputs = [output]

    quiz = Quiz.from_yaml(yaml_file)

    for o in outputs:
        if o == "sheets":
            string = quiz.to_sheets()
        elif o == "slides":
            string = quiz.to_slides()
        with open(f"{o}.tex", "w") as f:
            f.write(string)

        if not no_compile:
            proc = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", f"{o}.tex"], stdout=subprocess.DEVNULL
            )
            if proc.returncode != 0:
                logger.error(
                    f"'pdflatex {o}.tex' returned non-zero exit code. Try running pdflatex manually to "
                    "see what went wrong."
                )


if __name__ == "__main__":
    main()
