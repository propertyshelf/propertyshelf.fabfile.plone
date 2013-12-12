# -*- coding: utf-8 -*-
"""Deploy and manage Propertyshelf Plone applications using Fabric."""

import database
import frontend


database = database  # PyFlakes
frontend = frontend  # PyFlakes


__all__ = [
    'database',
    'frontend',
]
