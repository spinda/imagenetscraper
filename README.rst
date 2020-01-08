imagenetscraper
===============

|pypi| |travis|

Command-line utility for downloading all thumbnail images from an ImageNet_
synset, optionally rescaling to a different resolution.

**NOTICE:** ImageNet downloads are currently offline. This is an upstream issue
and out of my control. From the relevant announcement_:

    While conducting our study, since January 2019 we have disabled downloads of
    the full ImageNet data, except for the small subset of 1,000 categories used
    in the ImageNet Challenge. We are in the process of implementing our
    proposed remedies. 

Usage
-----

::

    Usage: imagenetscraper [OPTIONS] SYNSET_ID [OUTPUT_DIR]

    Options:
      -c, --concurrency INTEGER  Number of concurrent downloads (default: 8).
      -s, --size WIDTH,HEIGHT    If specified, images will be rescaled to the
                                 given size.
      -q, --quiet                Suppress progress output.
      -h, --help                 Show this message and exit.
      --version                  Show the version and exit.

If the URL of a synset page looks like:

::

    http://image-net.org/synset?wnid=n00000000
                                     ^^^^^^^^^
                                     SYNSET_ID

``SYNSET_ID`` is the ``n00000000`` part. For example, for the "person,
individual, someone, somebody, mortal, soul" synset at
http://image-net.org/synset?wnid=n00007846, the corresponding synset id is
``n00007846``.

The default output directory (``OUTPUT_DIR``) is the current directory.

Examples
********

To download all thumbnail imagess from the synset mentioned above to the
directory "person_images", run:

::

    imagenetscraper n00007846 person_images

To do the same, but with each thumbnail image rescaled to a width of 256 and a
height of 128, add ``--size 256,128``:

::

    imagenetscraper n00007846 person_images --size 256,128

To run in "quiet mode", suppressing progress output, add ``--quiet``:

::

    imagenetscraper n00007846 person_images --size 256,128 --quiet

By default, imagenetscraper will download 8 images at once. To change this, use
``--concurrency``:

::

    imagenetscraper n00007846 person_images --size 256,128 --concurrency 4

Install
-------

1) Install Python 3, pip, and a development version of libjpeg. imagenetscraper
   is tested with Python 3.4-3.7 and libjpeg-turbo 8.

   ::

    sudo apt-get install python3 python3-pip libjpeg-turbo8-dev

2) Download and install imagenetscraper with pip.

   ::

    sudo -H pip3 install imagenetscraper

Citation
--------

If this tool helped with your research, a citation would be appreciated:

::

    @Misc{imagenetscraper,
    author = {Michael Smith},
    title = {imagenetscraper: Bulk-download thumbnails from ImageNet synsets},
    howpublished = {\url{https://github.com/spinda/imagenetscraper}},
    year = {2017}
    }

Testing
-------

To run unit tests, use:

::

    python3 setup.py test

License
-------

Copyright (C) 2017-2018 Michael Smith <michael@spinda.net>

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <http://www.gnu.org/licenses/>.

.. _ImageNet: http://image-net.org/
.. _announcement: http://image-net.org/update-sep-17-2019

.. |pypi| image:: https://img.shields.io/pypi/v/imagenetscraper.svg
    :alt: PyPI
    :target: https://pypi.python.org/pypi/imagenetscraper
.. |travis| image:: https://img.shields.io/travis/spinda/imagenetscraper/master.svg
    :alt: Build Status
    :target: https://travis-ci.org/spinda/imagenetscraper
