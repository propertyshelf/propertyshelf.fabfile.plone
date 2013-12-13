# -*- coding: utf-8 -*-
"""Manage Plone application client components."""

from fabric import api
from propertyshelf.fabfile.common import rackspace
from propertyshelf.fabfile.common import utils
from propertyshelf.fabfile.common.exceptions import missing_env
from propertyshelf.fabfile.plone.utils import plone_config


def client_ctl(command=None):
    """Plone client control for start/stop/restart."""
    api.sudo('/etc/init.d/plone_client %s' % command)


@api.task
def remove():
    """Remove an existing MLS application client."""
    role = api.env.get('role_worker')
    role = role or missing_env('role_worker')
    opts = dict(
        environment='production',
        role=role,
    )
    rackspace.remove(**opts)


@api.task
@api.roles('worker')
def update():
    """Update the client packages."""
    config = plone_config()
    folder = config.get('client', {}).get('dir')
    client_ctl(command='stop')
    utils.backup_dev_packages(config=config, folder=folder)
    utils.run_buildout(config=config, folder=folder)
    client_ctl(command='start')


@api.task
@api.roles('worker')
def restart():
    """Restart the application client component."""
    client_ctl(command='restart')


@api.task
@api.roles('worker')
def rebuild():
    """Rebuild the application using buildout."""
    config = plone_config()
    folder = config.get('client', {}).get('dir')
    utils.run_buildout(config=config, folder=folder)
    client_ctl(command='restart')
