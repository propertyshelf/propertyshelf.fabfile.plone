# -*- coding: utf-8 -*-
"""Manage chef roles."""

from fabric import api
from propertyshelf.fabfile.common import roles


@api.task
def check():
    """Check if the required roles are available."""
    roles.check_required()


@api.task
def create_missing():
    """Create missing roles on the chef server."""
    raise NotImplementedError


@api.task
def list_nodes(role_list=None):
    """List all available nodes with given roles."""
    roles.list_nodes()
