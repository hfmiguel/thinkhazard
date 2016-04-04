# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 by the GFDRR / World Bank
#
# This file is part of ThinkHazard.
#
# ThinkHazard is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# ThinkHazard is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# ThinkHazard.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from subprocess import call
from urlparse import urlparse

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from sqlalchemy import engine_from_config

from .. import load_local_settings
from ..models import (
    DBSession,
    Publication,
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def database_name(config_uri, name, options={}):
    settings = get_appsettings(config_uri, name=name, options=options)
    load_local_settings(settings, name)
    url = settings['sqlalchemy.url']
    return urlparse(url).path.strip('/')


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)

    # Create new publication in admin database
    settings = get_appsettings(config_uri, name='admin', options=options)
    load_local_settings(settings, 'admin')
    engine = engine_from_config(settings, 'sqlalchemy.')
    with engine.begin() as db:
        DBSession.configure(bind=db)
        Publication.new()
        DBSession.flush()

    admin_database = database_name(config_uri, 'admin', options=options)
    public_database = database_name(config_uri, 'public', options=options)

    print 'Restart PostgreSQL'
    call(["sudo", "-u", "postgres", "/etc/init.d/postgresql", 'restart'])

    print 'Drop database', public_database
    call(["sudo", "-u", "postgres", "dropdb", public_database])

    print 'Create new fresh database', public_database
    call(["sudo", "-u", "postgres", "createdb", public_database])

    print 'Copy data from', admin_database, 'to', public_database
    cmd = 'sudo -u postgres pg_dump {} | sudo -u postgres psql -d {}'.format(
        admin_database,
        public_database)
    call(cmd, shell=True)

    print 'Restarting Apache to clear cached data'
    call(["sudo", "apache2ctl", "graceful"])
