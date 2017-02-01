# -*- coding: UTF-8 -*-
# Copyright 2012-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
This is the base for all settings of lino.projects.min1

.. autosummary::
   :toctree:

   demo


"""

from lino.projects.std.settings import *


class Site(Site):
    title = "Lino Mini 1"

    demo_fixtures = 'std demo demo2'

    user_types_module = 'lino_xl.lib.xl.user_types'

    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        tb.add_action(self.modules.contacts.Persons.detail_action)
        tb.add_action(self.modules.contacts.Companies.detail_action)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino_xl.lib.contacts'
        yield 'lino_xl.lib.cal'
        yield 'lino.modlib.export_excel'

