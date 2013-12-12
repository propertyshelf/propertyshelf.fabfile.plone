# -*- coding: utf-8 -*-
"""Manage Plone database components."""

from fabric import api
from propertyshelf.fabfile.common import zodb
from propertyshelf.fabfile.plone.utils import plone_config


def zodb_ctl(command=None):
    """ZODB database control for start/stop/restart."""
    api.sudo('/etc/init.d/plone_zeoserver %s' % command)


@api.task
@api.roles('database')
def restart():
    """Restart the database component."""
    zodb_ctl('restart')


@api.task
@api.roles('database')
def download_data():
    """Download the database files from the server."""
    zodb.download_data(plone_config())


@api.task
@api.roles('database')
def download_zodb():
    """Download ZODB part of Zope's data from the server."""
    zodb.download_zodb(plone_config())


@api.task
@api.roles('database')
def download_blobs():
    """Download blob part of Zope's data from the server."""
    zodb.download_blobs(plone_config())


@api.task
@api.roles('database')
def upload_data():
    """Upload the database files to the server."""
    zodb_ctl('stop')
    zodb.upload_data(plone_config())
    zodb_ctl('start')


@api.task
@api.roles('database')
def upload_zodb():
    """Upload ZODB part of Zope's data to the server."""
    zodb_ctl('stop')
    zodb.upload_zodb(plone_config())
    zodb_ctl('start')


@api.task
@api.roles('database')
def upload_blob():
    """Upload blob part of Zope's data to the server."""
    zodb_ctl('stop')
    zodb.upload_blob(plone_config())
    zodb_ctl('start')
