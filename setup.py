#!/usr/bin/env python

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

import setuptools

with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8').replace('|pypi| |travis|', '')

setuptools.setup(name='imagenetscraper',
                 py_modules=['imagenetscraper'],
                 entry_points='''
                     [console_scripts]
                     imagenetscraper = imagenetscraper:main
                 ''',
                 description='Bulk-download all thumbnails from an ImageNet synset, with ' +
                             'optional rescaling',
                 long_description=long_description,
                 version='1.0.1',
                 license='AGPLv3',
                 author='Michael Smith',
                 author_email='michael@spinda.net',
                 url='https://github.com/spinda/imagenetscraper',
                 download_url = 'https://github.com/spinda/imagenetscraper/archive/1.0.1.tar.gz',
                 keywords = ['imagenet', 'synset', 'scraper', 'download', 'ml'],
                 test_suite='tests',
                 install_requires=[
                     'click',
                     'defusedxml',
                     'frogress',
                     'grequests',
                     'pillow',
                     'requests'
                 ])
