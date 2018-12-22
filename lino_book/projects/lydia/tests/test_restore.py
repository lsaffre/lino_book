"""
Test whether dump the previous versions can be restored

  $ go lydia
  $ python manage.py test tests.test_restore

"""

from lino.utils.djangotest import RestoreTestCase

class TestCase(RestoreTestCase):
    tested_versions = ['18.12.0']

