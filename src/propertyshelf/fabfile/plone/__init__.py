# -*- coding: utf-8 -*-
"""Deploy and manage Propertyshelf Plone applications using Fabric."""

import client
import database
import frontend


client = client  # PyFlakes
database = database  # PyFlakes
frontend = frontend  # PyFlakes


__all__ = [
    'client',
    'database',
    'frontend',
]
