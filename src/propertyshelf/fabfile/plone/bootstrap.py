# -*- coding: utf-8 -*-
"""Bootstrap new servers."""

from fabric import api
from propertyshelf.fabfile.common import bootstrap, rackspace
from propertyshelf.fabfile.common.exceptions import missing_env


@api.task
def database(nodename=None, image=None, flavor=None):
    """Bootstrap a new standalone database server."""
    bootstrap.database(nodename=nodename, image=image, flavor=flavor)


@api.task
def frontend(nodename=None, image=None, flavor=None):
    """Bootstrap a new standalone frontend server."""
    bootstrap.frontend(nodename=nodename, image=image, flavor=flavor)


@api.task
def worker(nodename=None, image=None, flavor=None):
    """Bootstrap a new standalone application worker."""
    bootstrap.worker(nodename=nodename, image=image, flavor=flavor)


@api.task
def plone_m(nodename=None, image=None, flavor=None):
    """Bootstrap a new 'Plone M' bundle."""
    nodename = nodename or api.env.get('nodename_database')
    nodename = nodename or missing_env('nodename_database')

    image = image or api.env.get('os_image')
    image = image or missing_env('os_image')

    flavor = flavor or api.env.get('flavor_database')
    flavor = flavor or missing_env('flavor_database')

    role_database = api.env.get('role_database')
    role_database = role_database or missing_env('role_database')
    role_frontend = api.env.get('role_frontend')
    role_frontend = role_frontend or missing_env('role_frontend')
    role_worker = api.env.get('role_worker')
    role_worker = role_worker or missing_env('role_worker')

    runlist = ','.join([
        'role[%s]' % role_database,
        'role[%s]' % role_frontend,
        'role[%s]' % role_worker,
    ])

    opts = dict(
        environment='production',
        flavor=flavor,
        image=image,
        nodename=nodename,
        runlist=runlist,
        servername=nodename,
    )
    rackspace.create(**opts)


@api.task
def staging(nodename=None, image=None, flavor=None):
    """Bootstrap a staging system."""
    bootstrap.staging(nodename=nodename, image=image, flavor=flavor)
