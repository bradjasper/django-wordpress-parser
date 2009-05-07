"""
    WXR Parser (Wordpress eXtended RSS Parser)

    This is a WXP parser to handle migrating Wordpress to something in
    Python. This will not import to your project for you. You will have to
    connect the pieces. This just makes it easier to export from Wordpress.

    Author: Brad Jasper
    Site: http://bradjasper.com
    Version: 0.1b
    Date: January 31, 2009

    Usage:

    import wxr_exporter
    parser = wxr_exporter.Parser('wordpress.2009-01-31.xml')

    for info in parser.entries:
        print info

    Notes:

    This also uses amara for XML parsing. I did this because I think its the
    best Python XML parsing lib. Its namespace support is better than
    everyone elses. It does however have this funky behaviour of having to
    convert everything to unicode objects before its useful. If you know how
    to get around this please e-mail me.
"""
import sys
from datetime import datetime
import amara

def _to_unicode(obj):
    """Convert an object and it's items to unicode. Is there a better way
    to do this?"""

    if isinstance(obj, dict):
        return dict((name, unicode(value)) for name, value in obj.iteritems())

    elif isinstance(obj, list):
        return map(_to_unicode, obj)

    return unicode(obj)

class Parser(object):
    """Main parser that eats a Wordpress Export File (WXP)"""

    def __init__(self, file):
        self.file = file
        self.items = []
        self.process_file(file)

    def process_file(self, file):
        """Process a WXP file. Store results in our parser objects"""

        doc = amara.parse(file)

        items = []
        for item in doc.xml_xpath('*//item'):

            get_node = lambda x: item.xml_xpath(x).pop()

            info = _to_unicode({
                'id': get_node('wp:post_id'),
                'status': get_node('wp:status'),
                'slug': get_node('wp:post_name'),
                'title': item.title,
                'type': get_node('wp:post_type'),
                'link': item.link,
                'creator': get_node('dc:creator'),
                'pub_date': item.pubDate,
                'guid': item.guid,
                'content': get_node('content:encoded')})

            info['pub_date'] = self._parse_date(info['pub_date'])
            info['id'] = int(info['id'])

            items = item.xml_xpath('category')
            info['categories'] = self._get_categories(items)
            info['tags'] = self._get_tags(items)

            self.items.append(info)

    @property
    def entries(self):
        """Return the post entries from the set of items"""
        return [item for item in self.items if item['type'] == 'post']

    def _parse_date(self, input):
        """Turn a string date into a datetime object"""
        # Trying the %z directive throws an error, this may break other exports
        # by using +0000
        return datetime.strptime(input, "%a, %d %b %Y %H:%M:%S +0000")

    def _get_categories(self, items):
        """Return only categories from the items"""
        return _to_unicode([item for item in items if \
                getattr(item, 'domain', None) == 'category'])

    def _get_tags(self, items):
        """Return only tags from the items"""
        return _to_unicode([item for item in items if \
                getattr(item, 'domain', None) == 'tag'])



if __name__ == "__main__":
    
    file = sys.argv[1]
    parser = Parser(file)
    for info in parser.entries:
        print info
