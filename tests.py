import datetime

from django.test import TestCase
from parser import Parser


FILENAME = '/Users/bradjasper/Sites/common/wxr_exporter/data/wordpress.2009-05-03.xml'

class ParserModel(TestCase):

    def setUp(self):
        """Set up our parser"""

        self.parser = Parser(FILENAME)

        self.assert_(self.parser)

    def test_entries(self):
        """Test entries on from WXP exporter"""

        self.assert_(self.parser.entries)

        for entry in self.parser.entries:

            self.assert_(entry['status'] in ['publish', 'draft'],
                    entry['status'])

            self.assert_(entry['id'], entry['id'])
            self.assert_(entry['status'], entry['status'])


    def test_comments(self):
        """Make sure the comments are valid and being parsed correctly"""

        for entry in self.parser.entries:

            for comment in entry['comments']:

                self.assert_(comment['status'] in
                        ['approved', 'draft', 'spam'], comment['status'])

                for field in ['id', 'author', 'ip', 'content']:
                    self.assert_(comment[field], comment[field])

                self.assert_(issubclass(
                    comment['datetime'].__class__,
                    datetime.datetime))

