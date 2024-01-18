#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: sonosmusicservicelib.py
#
# Copyright 2023 Jenda Brands
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for the serviceproxy.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
from abc import ABC, abstractmethod

__author__ = '''Jenda Brands <jenda@brnds.eu>'''
__docformat__ = '''google'''
__date__ = '''28-12-2023'''
__copyright__ = '''Copyright 2023, Jenda Brands'''
__credits__ = ["Jenda Brands"]
__license__ = '''MIT'''
__maintainer__ = '''Jenda Brands'''
__email__ = '''<jenda@brnds.eu>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".


# This is the main prefix used for logging
LOGGER_BASENAME = '''sonosmusicservicelib'''
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())


class ServiceProxy(ABC):
    @abstractmethod
    def get_channels_metadata(self, index, count, service):
        """Should return metadata for channels."""

    @abstractmethod
    def get_last_update(self):
        """Should return a specific value indicating the last update."""

    @abstractmethod
    def get_media_uri_by_id(self, channel_id):
        """Should return the media URI based on a given channel id."""

    @abstractmethod
    def get_media_metadata_by_id(self, channel_id):
        """Should return media metadata of a given id."""

    @abstractmethod
    def get_extended_metadata_by_id(self, channel_id):
        """Should return extended media metadata of a given id."""

    @abstractmethod
    def get_metadata_by_id(self, metadata_id, index, count):
        """Should return metadata for a given id."""

    @abstractmethod
    def get_favorite_channels(self, index, count):
        """Should return a list of favorited channels."""
