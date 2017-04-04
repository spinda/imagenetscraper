# vim: set tw=99:

# This file is part of imagenetscraper, a command-line utility for downloading
# all thumbnail images from an ImageNet synset.

# Copyright (C) 2017 Michael Smith <michael@spinda.net>

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.

# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import os.path
import subprocess
import unittest

TESTS_DIR = os.path.dirname(os.path.realpath(__file__))

class InvalidArgumentsTestCase(unittest.TestCase):
    def run_error_case(self, id, code, *args):
        p = subprocess.Popen([os.path.join(TESTS_DIR, '..', 'imagenetscraper.py')] + list(args),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        _, stderr = p.communicate()
        self.assertEqual(p.returncode, code)
        with open(os.path.join(TESTS_DIR, '{}.log').format(id), 'r', encoding='utf-8') as f:
            self.assertEqual(stderr.decode('utf-8'), f.read())

    def test_nonexistent_synset_id(self):
        """User supplies nonexistent (but valid) synset id, should exit with error."""
        self.run_error_case('nonexistent_synset_id', 1, 'n11111111')

    def test_invalid_synset_id(self):
        """User supplies invalid synset id, should exit with error."""
        self.run_error_case('invalid_synset_id', 2, 'invalid')

    def test_invalid_concurrency(self):
        """User supplies invalid concurrency, should exit with error."""
        self.run_error_case('invalid_concurrency', 2, '1', '--concurrency', 'aaa')

    def test_invalid_size(self):
        """User supplies invalid size, should exit with error."""
        self.run_error_case('invalid_size', 2, '1', '--size', 'aaa')
