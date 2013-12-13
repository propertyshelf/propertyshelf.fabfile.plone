# -*- coding: utf-8 -*-
"""Deploy and manage Propertyshelf Plone applications using Fabric."""

import client
import database
import frontend
import roles


client = client  # PyFlakes
database = database  # PyFlakes
frontend = frontend  # PyFlakes
roles = roles


__all__ = [
    'client',
    'database',
    'frontend',
    'roles',
]
