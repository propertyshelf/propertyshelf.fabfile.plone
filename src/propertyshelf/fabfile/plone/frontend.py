# -*- coding: utf-8 -*-
"""Manage Plone frontend components like web server, load balancer, cache."""

from fabric import api
from propertyshelf.fabfile.common import frontend


@api.task
@api.roles('frontend')
def restart():
    """Restart the frontend components."""
    restart_haproxy()
    restart_varnish()
    restart_nginx()


@api.task
@api.roles('frontend')
def restart_nginx():
    """Restart the NginX web server component."""
    frontend.restart_nginx()


@api.task
@api.roles('frontend')
def restart_varnish():
    """Restart the Varnish caching proxy component."""
    frontend.restart_varnish()


@api.task
@api.roles('frontend')
def restart_haproxy():
    """Restart the HA-Proxy load balancer component."""
    frontend.restart_haproxy()
