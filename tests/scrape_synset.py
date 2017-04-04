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

import hashlib
import os
import os.path
import subprocess
import tempfile
import unittest

class ScrapeSynsetTestCase(unittest.TestCase):
    def run_synset_scraper(self, id, *args, quiet=False):
        with tempfile.TemporaryDirectory() as tmp:
            p = subprocess.Popen(['./imagenetscraper.py', 'n00007846', tmp] + list(args),
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            self.assertEqual(p.returncode, 0)
            self.assertEqual(stderr.decode('utf-8'), '')
            if quiet:
                self.assertEqual(len(stdout), 0)
            else:
                self.assertNotEqual(len(stdout), 0)
            with open('./tests/{}.log'.format(id), 'r', encoding='utf-8') as f:
                expected_lines = f.read().strip().split('\n')
            actual_files = list(sorted(os.listdir(tmp)))
            self.assertEqual(len(actual_files), len(expected_lines))
            for actual_file, expected_line in zip(actual_files, expected_lines):
                with open(os.path.join(tmp, actual_file), 'rb') as f:
                    actual_hash = hashlib.sha256(f.read()).hexdigest()
                actual_line = '{}  {}'.format(actual_hash, actual_file)
                self.assertEqual(actual_line, expected_line)
            return stdout

    def test_scrape_synset_unscaled(self):
        """Scrape synset without rescaling, should save correct files at unscaled resolutions."""
        self.run_synset_scraper('scrape_synset_unscaled')

    def test_scrape_synset_scaled(self):
        """Scrape synset with rescaling, should save correct files at size 256x256."""
        self.run_synset_scraper('scrape_synset_scaled', '--size', '256,256')

    def test_scrape_synset_quiet(self):
        """Scrape synset in quiet mode, shouldn't produce any output."""
        self.run_synset_scraper('scrape_synset_unscaled', '--quiet', quiet=True)
