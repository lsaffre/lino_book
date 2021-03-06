# -*- coding: UTF-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""

.. autosummary::
   :toctree:

   demo
   www


"""

import datetime

from lino_noi.lib.noi.settings import *


class Site(Site):

    workflows_module = 'lino_book.projects.noi1e.workflows'

    the_demo_date = datetime.date(2015, 5, 23)

    languages = "en de fr"
    # readonly = True
    catch_layout_exceptions = False

    use_linod = True
    # use_ipdict = True
    # use_websockets = True
    social_auth_backends = [
        'social_core.backends.github.GithubOAuth2',
        # 'social_core.backends.google.GoogleOAuth2',
        # 'social_core.backends.google.GoogleOAuth',
        'social_core.backends.google.GooglePlusAuth',
        'social_core.backends.facebook.FacebookOAuth2',
        'social_core.backends.mediawiki.MediaWiki'
    ]
    use_experimental_features = True
    # default_ui = 'lino_extjs6.extjs6'
    # default_ui = 'lino.modlib.bootstrap3'
    # default_ui = 'lino_openui5.openui5'
    # default_ui = 'lino_react.react'

    # def get_installed_apps(self):
    #     yield super(Site, self).get_installed_apps()
    #     yield 'lino_react.react'

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('excerpts', 'responsible_user', 'jean')
        # yield ('memo', 'front_end', 'react')

    def get_installed_apps(self):
        # add lino.modlib.restful to the std list of plugins
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.restful'
        # yield 'lino_xl.lib.caldav'
        # 20210305 removed mailbox. See :mod:`lino_xl.lib.mailbox`.
        # yield 'lino_xl.lib.mailbox'

    def setup_plugins(self):
        """Change the default value of certain plugin settings.

        - :attr:`excerpts.responsible_user
          <lino_xl.lib.excerpts.Plugin.responsible_user>` is set to
          ``'jean'`` who is both senior developer and site admin in
          the demo database.

        """
        super(Site, self).setup_plugins()
        # self.plugins.social_auth.configure(
        #     backends=['social_core.backends.github.GithubOAuth2'])
        # self.plugins.excerpts.configure(responsible_user='jean')
        if self.is_installed('extjs'):
            self.plugins.extjs.configure(enter_submits_form=False)
        if False:
            self.plugins.mailbox.add_mailbox(
                'mbox', "Luc's aaa mailbox",
                '/home/luc/.thunderbird/luc/Mail/Local Folders/aaa')



# https://github.com/organizations/lino-framework/settings/applications/632218
SOCIAL_AUTH_GITHUB_KEY = '355f66b1557f0cbf4d1d'
SOCIAL_AUTH_GITHUB_SECRET = '4dbeea1701bf03316c1759bdb422d9f88969b782'

SOCIAL_AUTH_GOOGLE_PLUS_KEY = '451271712409-9qtm9bvjndaeep2olk3useu61j6qu2kp.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = 'NHyaqV2HY8lV5ULG6k51OMwo'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
    'profile',
    'https://www.googleapis.com/auth/plus.login',
    'https://www.googleapis.com/auth/contacts.readonly', # To have just READ permission
    'https://www.googleapis.com/auth/contacts ', # To have WRITE/READ permissions
]

SOCIAL_AUTH_FACEBOOK_KEY = '1837593149865295'
SOCIAL_AUTH_FACEBOOK_SECRET = '1973f9e9d9420c4c6502aa40cb8cb7db'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'public_profile', 'user_friends']

SOCIAL_AUTH_MEDIAWIKI_KEY = '7dbd2e1529e45108f798349811c7a2b7'
SOCIAL_AUTH_MEDIAWIKI_SECRET = '8041055fcd16333fa242b346e0ae52133fd2ee14'
SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'
SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'oob'

if False:  # not needed for newbies

    # Add ldap authentication. Requires  Hamza's fork of django_auth_ldap.
    # temporary installation instructions:
    # $ sudo apt-get install build-essential python3-dev python2.7-dev libldap2-dev libsasl2-dev slapd ldap-utils lcov valgrind
    # $ pip install -e git+https://github.com/khchine5/django-auth-ldap.git#egg=django-auth-ldap
    # import ldap
    # from django_auth_ldap.config import LDAPSearch, LDAPGroupType,GroupOfNamesType,LDAPSearchUnion,GroupOfUniqueNamesType

    AUTHENTICATION_BACKENDS.append("django_auth_ldap.backend.LDAPBackend")

    AUTH_LDAP_SERVER_URI = "ldap://ldap.forumsys.com"
    AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,dc=example,dc=com"
    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': 'givenName',
        'last_name': 'sn',
        'email': 'mail',
    }


DEBUG = True
ALLOWED_HOSTS=["*"]
