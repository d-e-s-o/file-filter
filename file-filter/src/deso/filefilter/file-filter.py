#!/usr/bin/env python

#/***************************************************************************
# *   Copyright (C) 2016-2017 Daniel Mueller (deso@posteo.net)              *
# *                                                                         *
# *   This program is free software: you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation, either version 3 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program.  If not, see <http://www.gnu.org/licenses/>. *
# ***************************************************************************/

"""A script to filter out specific files from a list of arbitrary files."""

from argparse import (
  ArgumentParser,
)
from sys import (
  argv as sysargv,
  stderr,
  stdin,
)


def hasPythonShebang(file_):
  """Check whether a file contains a Python shebang."""
  with open(file_, "r") as f:
    try:
      line = next(f)
      return line.startswith("#!") and "python" in line
    except (StopIteration, UnicodeDecodeError):
      return False


def isPythonFile(file_):
  """Check whether a file is a Python file or not."""
  return file_.endswith("py") or hasPythonShebang(file_)


def isRustFile(file_):
  """Check whether a file is a Rust file or not."""
  return file_.endswith("rs")


def main(argv):
  """Filter specific files out of a list of arbitrary files."""
  parser = ArgumentParser()
  # By default we perform no filtering at all.
  parser.set_defaults(filter_=lambda x: True)

  parser.add_argument(
    "files", action="store", default=[], nargs="*",
    help="A list of files to filter.",
  )
  parser.add_argument(
    "--python", action="store_const", const=isPythonFile, dest="filter_",
    help="Filter out Python files.",
  )
  parser.add_argument(
    "--rust", action="store_const", const=isRustFile, dest="filter_",
    help="Filter out Rust files.",
  )
  parser.add_argument(
    "--stdin", action="store_true", default=False,
    help="Read file names from stdin and not from the argument list supplied.",
  )
  parser.add_argument(
    "-v", "--verbose", action="store_true", default=False,
    help="Print output files.",
  )
  ns = parser.parse_args(argv[1:])

  if ns.stdin:
    files = stdin.read().splitlines()
    joiner = "\n"
  else:
    files = ns.files
    joiner = " "

  files = [f for f in files if ns.filter_(f)]

  if files is []:
    return 1

  if ns.verbose:
    print("Files: %s" % ", ".join(files), file=stderr)

  print(joiner.join(files))
  return 0


if __name__ == "__main__":
  exit(main(sysargv))
