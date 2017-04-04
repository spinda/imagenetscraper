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

import io
import os
import os.path
import re
import sys
import urllib.parse

import click
import defusedxml.ElementTree
import frogress
import grequests
import PIL.Image
import requests

SYNSET_PAGE_URL = 'http://image-net.org/synset?wnid={}'
SYNSET_INDEX_URL = \
    'http://image-net.org/python/gp.py/ImagesXML?type=synsetgood&synsetid={}&start=0&n={}'
IMAGENET_THUMB_URL = 'http://image-net.org/nodes/{}/{}/{}/{}.thumb'

class SynsetId(click.ParamType):
    name = 'synset_id'

    def convert(self, value, param, ctx):
        match = re.search('^n[0-9]{8}$', value.lower())
        if match:
            return value
        else:
            self.fail('{} is not a valid synset id; example: n00007846'.format(value), param, ctx)

class Size(click.ParamType):
    name = 'width,height'

    def convert(self, value, param, ctx):
        match = re.search('^([0-9]+),([0-9]+)$', value.lower())
        if match:
            return (int(match.group(1)), int(match.group(2)))
        else:
            self.fail('{} is not a valid size; example: 100,100'.format(value), param, ctx)

@click.command()
@click.argument('synset_id',
                type=SynsetId(),
                required=True)
@click.argument('output_dir',
                type=click.Path(dir_okay=True, file_okay=False),
                default='.')
@click.option('-c', '--concurrency',
              type=int,
              default=8,
              help='Number of concurrent downloads (default: 8).')
@click.option('-s', '--size',
              type=Size(),
              default=None,
              help='If specified, images will be rescaled to the given size.')
@click.option('-q', '--quiet',
              is_flag=True,
              default=False,
              help='Suppress progress output.')
@click.help_option('-h', '--help')
@click.version_option()
def main(synset_id, output_dir, concurrency, size, quiet):
    # Create output directory if it doesn't already exist.
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        report_exception(e, 'Failed to create output directory: {}'.format(output_dir))

    # Find the target id from the synset id.
    if not quiet:
        print('Retrieving synset target id')
    try:
        target_id = snag_synset_target_id(synset_id)
    except Exception as e:
        report_exception(e,
                'Failed to retrieve synset target id, are you sure a synset with id {} exists?'
                    .format(synset_id))

    # Make an initial request for zero images from the synset, so we can obtain
    # the total image count to request.
    if not quiet:
        print('Retrieving image count')
    try:
        total = int(snag_synset_imageset(target_id, 0).attrib['total'])
    except Exception as e:
        report_exception(e, 'Failed to retrieve image count, is there a connection issue?')

    # Now that we know the total image count for the synset, we can retrieve an
    # index of all images in one go.
    if not quiet:
        print('Retrieving synset index')
    try:
        images = snag_synset_imageset(target_id, total).iter('image')
    except Exception as e:
        report_exception(e, 'Failed to retrieve synset index, is there a connection issue?')

    # Prepare a batch of asynchronous HTTP requests, one per image.
    urls = (make_thumb_url(image) for image in images)
    reqs = (grequests.get(url) for url in urls)
    responses = grequests.imap(reqs, size=concurrency, exception_handler=report_save_exception)

    # Save images to disk as they download, rescaling if requested.
    if not quiet:
        responses = frogress.bar(responses, steps=total)
        print('\nDownloading {} images{}'
                .format(total, ' and scaling to {}'.format(size) if size else ''))
    for r in responses:
        try:
            r.raise_for_status()
            url = urllib.parse.urlparse(r.url)
            hash, _ = os.path.splitext(os.path.basename(url.path))
            output_file_path = os.path.join(output_dir, hash + '.jpg')

            if size:
                PIL.Image.open(io.BytesIO(r.content)).resize(size).save(output_file_path)
            else:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(r.content)
        except Exception as e:
            report_save_exception(r, e)
        finally:
            r.close()

    if not quiet:
        print('''

Done! If this tool helped with your research, a citation would be appreciated:

@Misc{imagenetscraper,
author = {Michael Smith},
title = {imagenetscraper: Bulk-download thumbnails from ImageNet synsets},
howpublished = {\\url{https://github.com/spinda/imagenetscraper}},
year = {2017}
}''')

def make_thumb_url(image):
    return IMAGENET_THUMB_URL.format(image.attrib['node'], image.attrib['synsetoffset'],
                                     image.attrib['prefix'][:2], image.attrib['prefix'])

def snag_synset_target_id(synset_id):
    r = requests.get(SYNSET_PAGE_URL.format(synset_id))
    r.raise_for_status()
    match = re.search('^target_id = \'([0-9]+)\';$', r.content.decode('utf-8'), re.M)
    if not match:
        raise Exception('Could not find target id in: {}'.format(r.url))
    return int(match.group(1))

def snag_synset_imageset(target_id, n):
    r = requests.get(SYNSET_INDEX_URL.format(target_id, n))
    r.raise_for_status()
    return defusedxml.ElementTree.fromstring(r.content).find('imageset')

def report_exception(e, prelude, exit=True):
    print(prelude, file=sys.stderr)
    print('({})'.format(e), file=sys.stderr)
    if exit:
        sys.exit(1)

def report_save_exception(r, e):
    report_exception(e, 'Failed to save image: {}'.format(r.url), exit=False)

if __name__ == '__main__':
    main()
