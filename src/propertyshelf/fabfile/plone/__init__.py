# -*- coding: utf-8 -*-
"""Deploy and manage Propertyshelf Plone applications using Fabric."""

import bootstrap
import client
import database
import frontend
import roles


bootstrap = bootstrap  # PyFlakes
client = client  # PyFlakes
database = database  # PyFlakes
frontend = frontend  # PyFlakes
roles = roles


__all__ = [
    'bootstrap',
    'client',
    'database',
    'frontend',
    'roles',
]
