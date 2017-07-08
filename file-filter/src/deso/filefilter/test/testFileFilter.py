# testFileFilter.py

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

"""Tests for the file-filter functionality."""

from deso.execute import (
  execute,
)
from os import (
  extsep,
  pardir,
)
from os.path import (
  dirname,
  join,
  realpath,
)
from random import (
  randint,
)
from unittest import (
  TestCase,
  main,
)
from sys import (
  executable,
)
from tempfile import (
  NamedTemporaryFile,
)


FILE_FILTER = realpath(join(dirname(__file__), pardir, "file-filter.py"))


class TestFileFilter(TestCase):
  """A test case for testing of the file-filter functionality."""
  def doTest(self, file_type, use_stdin, indices):
    """Perform the filtering test."""
    with NamedTemporaryFile(buffering=0) as file0,\
         NamedTemporaryFile(buffering=0, suffix="%spy" % extsep) as file1,\
         NamedTemporaryFile(buffering=0, suffix="%sh" % extsep) as file2,\
         NamedTemporaryFile(buffering=0, suffix="%srs" % extsep) as file3,\
         NamedTemporaryFile(buffering=0) as file4,\
         NamedTemporaryFile(buffering=0, suffix="%sbin" % extsep) as file5:
      # We leave 'file0' empty.
      file1.write(b"pass")
      file2.write(bytes("// %s" % file3.name, "utf-8"))
      file3.write(bytes("#!/usr/bin/rustc", "utf-8"))
      file4.write(bytes("#!%s" % executable, "utf-8"))
      file5.write(bytes("".join(chr(randint(0, 255)) for _ in range(512)), "utf-8"))

      files = [file0.name, file1.name, file2.name, file3.name, file4.name, file5.name]
      if use_stdin:
        stdin = "\n".join(files).encode()
        joiner = "\n"
        out, _ = execute(executable, FILE_FILTER, file_type, "--stdin", stdin=stdin, stdout=b"")
      else:
        joiner = " "
        out, _ = execute(executable, FILE_FILTER, file_type, *files, stdout=b"")

      expected = joiner.join(map(lambda i: files[i], indices))
      self.assertEqual(out.decode("utf-8")[:-1], expected)


  def testPythonFileFiltering(self):
    """Verify filtering of Python files provided as arguments works as expected."""
    for use_stdin in (False, True):
      # Only files 1 & 4 should be recognized as Python files.
      self.doTest("--python", use_stdin, [1, 4])


  def testRustFileFiltering(self):
    """Verify filtering of Rust files provided as arguments works as expected."""
    for use_stdin in (False, True):
      self.doTest("--rust", use_stdin, [3])


if __name__ == "__main__":
  main()
