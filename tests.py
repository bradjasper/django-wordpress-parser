from django.test import TestCase
from parser import Parser

FILENAME = '/Users/bradjasper/Sites/common/wxr_exporter/data/wordpress.2009-05-03.xml'

class ParserModel(TestCase):

    def setUp(self):
        """Set up our parser"""

        self.parser = Parser(FILENAME)

        self.assert_(self.parser)

    def testEntries(self):
        """Test entries on from WXP exporter"""

        self.assert_(self.parser.entries)

