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

# pylint: skip-file

"""
Main code for sonosmusicservicelib.

.. _Google Python Style Guide:
   https://google.github.io/styleguide/pyguide.html

"""

import logging
from spyne import rpc, ServiceBase, ComplexModel, Integer, Unicode, Boolean


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

SONOS_SERVICE_NS_LO = "http://www.sonos.com/Services/1.1"
SONOS_SERVICE_NS = 'xmlns="http://www.sonos.com/Services/1.1"'


class LastUpdate(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    catalog = Integer


class RequestSomething(ComplexModel):
    count = Integer
    id = Unicode
    index = Integer


class StreamMetadata(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    logo = Unicode
    description = Unicode
    isEphemeral = Boolean


class MediaMetadata(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    id = Integer
    itemType = Unicode
    title = Unicode
    # TODO: Somehow, when mimeType is set, everything breaks. No clue why, keep like this for now.
    # mimeType = Unicode
    streamMetadata = StreamMetadata


class MediaCollection(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    id = Unicode
    itemType = Unicode
    title = Unicode
    summary = Unicode
    canPlay = Boolean
    albumArtURI = Unicode


class Metadata(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    index = Integer
    count = Integer
    total = Integer
    mediaMetadata = MediaMetadata.customize(max_occurs='unbounded')
    mediaCollection = MediaCollection.customize(max_occurs='unbounded')


class ExtendedMetadata(ComplexModel):
    __namespace__ = SONOS_SERVICE_NS_LO
    mediaCollection = MediaCollection


class SonosService(ServiceBase):

    __namespace__ = SONOS_SERVICE_NS_LO

    @rpc(Integer, Integer, Unicode, _returns=Metadata, _body_style='wrapped')
    def getMetadata(ctx, index, count, id):
        index = int(index)
        count = int(count)
        return ctx.app.get_service_proxy().get_metadata_by_id(id, index, count)

    @rpc(_returns=LastUpdate, _body_style='wrapped')
    def getLastUpdate(ctx):
        return ctx.app.get_service_proxy().get_last_update()

    @rpc(Unicode, _returns=Unicode, _body_style='wrapped')
    def getMediaURI(ctx, id):
        id_ = id
        return ctx.app.get_service_proxy().get_media_uri_by_id(id_)

    @rpc(Integer, _returns=MediaMetadata, _body_style='wrapped')
    def getMediaMetadata(ctx, id):
        id_ = id
        return ctx.app.get_service_proxy().get_media_metadata_by_id(id_)

    @rpc(Unicode, _returns=ExtendedMetadata, _body_style='wrapped')
    def getExtendedMetadata(ctx, id):
        id_ = id
        return ctx.app.get_service_proxy().get_extended_metadata_by_id(id_)
