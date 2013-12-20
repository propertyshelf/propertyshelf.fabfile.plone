propertyshelf.fabfile.plone
===========================

This project contains a bunch of fabric commands we use at
`Propertyshelf`_ to deploy and maintain our Plone CMS systems.


Requirements
------------

`propertyshelf.fabfile.plone` currently uses `knife`_ to communicate with
Rackspace servers. Please make sure `knife` is installed and configured
successfully on your system.


Install
-------

You can install `propertyshelf.fabfile.plone` with PIP::

    pip install propertyshelf.fabfile.plone

All required dependencies will be installed automatically.


Usage
-----

First, we need a working `knife.rb` file to interact with our Chef server and
the Rackspace cloud eco system. Below is an example `knife.rb` file that gets
all its required info from environment variables. This way you can add this
`knife.rb` file inside a `.chef` directory to your project and savely put it
under version control::

    # Logging.
    log_level                         :info
    log_location                      STDOUT

    # Chef server configuration.
    chef_server_url                   "#{ENV['KNIFE_CHEF_SERVER']}"
    client_key                        "#{ENV['KNIFE_CLIENT_KEY']}"
    node_name                         "#{ENV['KNIFE_NODE_NAME']}"
    validation_client_name            "#{ENV['KNIFE_VALIDATION_CLIENT_NAME']}"
    validation_key                    "#{ENV['KNIFE_VALIDATION_CLIENT_KEY']}"
    encrypted_data_bag_secret         "#{ENV['ENCRYPTED_DATA_BAG_SECRET_FILE']}"

    # Rackspace API configuration.
    knife[:rackspace_api_key]       = "#{ENV['RACKSPACE_API_KEY']}"
    knife[:rackspace_api_username]  = "#{ENV['RACKSPACE_USERNAME']}"
    knife[:rackspace_endpoint]      = "#{ENV['RACKSPACE_ENDPOINT']}"
    knife[:rackspace_version]       = "#{ENV['RACKSPACE_VERSION']}"

Next, we need a `fabfile.py`. All we need to do is to import
`propertyshelf.fabfile.plone` to make the fabric commands available and the
available environments we can work with from `propertyshelf.fabfile.common`.::

    # -*- coding: utf-8 -*-
    """Sample application deployment script."""

    from fabric import api

    from propertyshelf.fabfile.common.environments import *
    from propertyshelf.fabfile.plone import *


    # Definition of role names to be used.
    api.env.role_base = 'plone_01'
    api.env.role_database = '%s_database' % api.env.role_base
    api.env.role_frontend = '%s_frontend' % api.env.role_base
    api.env.role_worker = '%s_worker' % api.env.role_base

    # Definition of used Rackspace flavors (server sized) for our servers.
    api.env.flavor_database = '4'
    api.env.flavor_frontend = '2'
    api.env.flavor_worker = '2'

    # Definition of node names to be used.
    BASE_NODENAME = 'plone-01'
    api.env.nodename_database = '%s-database' % BASE_NODENAME
    api.env.nodename_frontend = '%s-frontend' % BASE_NODENAME
    api.env.nodename_worker = '%s-worker' % BASE_NODENAME
    api.env.nodename_development = BASE_NODENAME

    # The Rackspace server image we use. This is a Debian 6.0.6.
    api.env.os_image = '695ca76e-fc0d-4e36-82e0-8ed66480a999'

    api.env.domain = 'example.com'
    api.env.vhost_databag = 'virtual_hosts_plone_01'
    api.env.plone_version = '4.3.2'

You can now use fabric to manage your Plone application::

    $ fab -l
    Sample application deployment script.

    Available commands:

        development               Work locally with vagrant.
        production                Work with the production environment.
        staging                   Work with the staging environment.
        bootstrap.database        Bootstrap a new standalone database server.
        bootstrap.frontend        Bootstrap a new standalone frontend server.
        bootstrap.plone_m         Bootstrap a new 'Plone M' bundle.
        bootstrap.staging         Bootstrap a staging system.
        bootstrap.worker          Bootstrap a new standalone application worker.
        client.rebuild            Rebuild the application using buildout.
        client.remove             Remove an existing MLS application client.
        client.restart            Restart the application client component.
        client.update             Update the client packages.
        database.download_blobs   Download blob part of Zope's data from the server.
        database.download_data    Download the database files from the server.
        database.download_zodb    Download ZODB part of Zope's data from the server.
        database.restart          Restart the database component.
        database.upload_blob      Upload blob part of Zope's data to the server.
        database.upload_data      Upload the database files to the server.
        database.upload_zodb      Upload ZODB part of Zope's data to the server.
        frontend.restart          Restart the frontend components.
        frontend.restart_haproxy  Restart the HA-Proxy load balancer component.
        frontend.restart_nginx    Restart the NginX web server component.
        frontend.restart_varnish  Restart the Varnish caching proxy component.
        roles.check               Check if the required roles are available.
        roles.create_missing      Create missing roles on the chef server.
        roles.list_nodes          List all available nodes with given roles.

Before we can start it is a good idea to check if all roles we defined are
available on the chef server::

    $ fab roles.check
    Role plone_01 NOT available.
    Role plone_01_database NOT available.
    Role plone_01_frontend NOT available.
    Role plone_01_worker NOT available.

    Done.

To create the missing roles based on our configuration, we simply have to do::

    $ fab roles.create_missing
    Created role plone_01
    Created role plone_01_database
    Created role plone_01_frontend
    Created role plone_01_worker

    Done.

You can now manage the single components::

    $ fab production frontend.restart
    [x.x.x.x] Executing task 'frontend.restart'
    [x.x.x.x] sudo: /etc/init.d/haproxy restart
    [x.x.x.x] out: sudo password:

    [x.x.x.x] out: Restarting haproxy: haproxy.
    [x.x.x.x] out:

    [x.x.x.x] sudo: /etc/init.d/varnish restart
    [x.x.x.x] out: sudo password:
    [x.x.x.x] out: Stopping HTTP accelerator: varnishd.
    [x.x.x.x] out: Starting HTTP accelerator: varnishd.
    [x.x.x.x] out:

    [x.x.x.x] sudo: /etc/init.d/nginx restart
    [x.x.x.x] out: sudo password:
    [x.x.x.x] out: Restarting nginx: nginx.
    [x.x.x.x] out:


    Done.
    Disconnecting from x.x.x.x... done.

We also support download of the database files for local testing::

    $ fab production database.download_data
    [x.x.x.x] Executing task 'database.download_data'
    This will overwrite your local Data.fs. Are you sure you want to continue? [Y/n]
    [localhost] local: mkdir -p var/filestorage
    [localhost] local: mv var/filestorage/Data.fs var/filestorage/Data.fs.bak
    [x.x.x.x] out: sudo password:
    [x.x.x.x] sudo: rsync -a var/filestorage/Data.fs /tmp/Data.fs
    [x.x.x.x] out: sudo password:
    [x.x.x.x] out:
    [x.x.x.x] download: /Volumes/Work/Propertyshelf/Plone/Provisioning/var/filestorage/Data.fs <- /tmp/Data.fs
    This will overwrite your local blob files. Are you sure you want to continue? [Y/n]
    [localhost] local: rm -rf var/blobstorage_bak
    [localhost] local: mv var/blobstorage var/blobstorage_bak
    [x.x.x.x] sudo: rsync -a ./var/blobstorage /tmp/
    [x.x.x.x] out: sudo password:
    [x.x.x.x] out:
    [x.x.x.x] sudo: tar czf blobstorage.tgz blobstorage
    [x.x.x.x] out: sudo password:
    [x.x.x.x] out:
    [x.x.x.x] download: /Volumes/Work/Propertyshelf/Plone/Provisioning/var/blobstorage.tgz <- /tmp/blobstorage.tgz

    Warning: Local file /Volumes/Work/Propertyshelf/Plone/Provisioning/var/blobstorage.tgz already exists and is being overwritten.

    [localhost] local: tar xzf blobstorage.tgz

    Done.
    Disconnecting from x.x.x.x... done.

.. _`Propertyshelf`: http://propertyshelf.com
.. _`knife`: http://docs.opscode.com/knife.html
