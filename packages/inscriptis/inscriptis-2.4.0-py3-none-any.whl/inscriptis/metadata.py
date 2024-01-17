"""Inscriptis metadata information."""

import importlib.metadata as metadata

PACKAGE = 'inscriptis'

__author__ = metadata.metadata(PACKAGE)['Author']
__author_email__ = metadata.metadata(PACKAGE)['Author-email']
__copyright__ = f"{metadata.metadata(PACKAGE)['Name']} {metadata.metadata(PACKAGE)['Version']} © {metadata.metadata(PACKAGE)['Author']}"
__license__ = metadata.metadata(PACKAGE)['License']
__version__ = metadata.metadata(PACKAGE)['Version']

