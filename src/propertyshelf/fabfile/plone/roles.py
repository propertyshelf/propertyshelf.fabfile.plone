# -*- coding: utf-8 -*-
"""Manage chef roles."""

from chef import autoconfigure, Role
from fabric import api
from fabric.colors import green
from propertyshelf.fabfile.common import roles

PYTHON_MD5 = '3b477554864e616a041ee4d7cef9849751770bc7c39adaf78a94ea145c488059'


@api.task
def check():
    """Check if the required roles are available."""
    roles.check_required()


@api.task
def create_missing():
    """Create missing roles on the chef server."""
    chef_api = autoconfigure()
    required = roles.get_required()
    domain = api.env.get('domain', 'example.com')

    # Create the role_base.
    if not roles.check(required.get('role_base')):
        name = required.get('role_base')
        description = 'Plone Application for %s.' % domain
        run_list = (
            "role[base]",
            "recipe[build-essential]",
        )
        default_attributes = {
            'domain': domain,
            'haproxy': {
                'app_server_role': required.get('role_worker'),
                'incoming_address': '127.0.0.1',
                'incoming_port': '8300',
                'member_port': '8080',
            },
            'nginx': {
                'client_max_body_size': '150m',
            },
            'plone': {
                'client': {
                    'count': 2,
                    'eggs': [
                        "Products.Doormat == 0.9.1",
                        "Products.PloneFormGen == 1.7.12",
                        "Products.RedirectionTool == 1.3.1",
                        "collective.carousel == 1.6.2",
                        "collective.contentleadimage == 1.3.4",
                        "collective.cover == 1.0a6",
                        "collective.googleanalytics == 1.4.3",
                        "mls.apiclient == 1.1.1",
                        "plone.app.multilingual == 1.2.1",
                        "plone.mls.core == 0.4.2",
                        "plone.mls.listing == 0.9.7",
                        "plone.multilingualbehavior == 1.2",
                    ],
                    'extends': [
                        'plone_sites.cfg',
                    ],
                    'zeo_role': required.get('role_database'),
                },
                'version': api.env.get('plone_version', '4.3.2'),
                'vhost_data_bag': api.env.get('vhost_databag', ''),
            },
            'python': {
                'checksum': PYTHON_MD5,
                'configure_options': [
                    '--prefix=/usr/local',
                ],
                'install_method': 'source',
                'prefix_dir': '/usr/local',
                'version': '2.7.5',
            },
            'varnish': {
                'listen_address': '127.0.0.1',
                'listen_port': '9000',
                'backend_port': '8300',
                'storage': 'malloc',
                'storage_size': '512M',
                'vcl_cookbook': 'plone_hosting',
                'vcl_source': 'varnish.vcl.erb',
            }
        }

        Role.create(
            name,
            api=chef_api,
            description=description,
            run_list=run_list,
            default_attributes=default_attributes,
        )
        print(green('Created role %s') % name)

    # Create the role_database.
    if not roles.check(required.get('role_database')):
        name = required.get('role_database')
        description = 'ZEO Server for %s.' % domain
        run_list = (
            "role[%s]" % required.get('role_base'),
            "recipe[plone_hosting::database_server]",
        )
        override_attributes = {
            'plone': {
                'client': {
                    'count': 2,
                }
            },
        }

        Role.create(
            name,
            api=chef_api,
            description=description,
            run_list=run_list,
            override_attributes=override_attributes,
        )
        print(green('Created role %s') % name)

    # Create the role_frontend.
    if not roles.check(required.get('role_frontend')):
        name = required.get('role_frontend')
        description = 'Frontend Server for %s.' % domain
        run_list = (
            "role[%s]" % required.get('role_base'),
            "recipe[plone_hosting::load_balancer]",
            "recipe[plone_hosting::cache_server]",
            "recipe[plone_hosting::web_server]"
        )

        Role.create(
            name,
            api=chef_api,
            description=description,
            run_list=run_list,
        )
        print(green('Created role %s') % name)

    # Create the role_worker.
    if not roles.check(required.get('role_worker')):
        name = required.get('role_worker')
        description = 'Application Worker for %s.' % domain
        run_list = (
            "role[%s]" % required.get('role_base'),
            "recipe[plone_hosting::app_server]",
        )

        Role.create(
            name,
            api=chef_api,
            description=description,
            run_list=run_list,
        )
        print(green('Created role %s') % name)


@api.task
def list_nodes(role_list=None):
    """List all available nodes with given roles."""
    roles.list_nodes()
