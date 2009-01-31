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

    for entry in parser.entries:
        print entry

    Notes:

    This also uses amara for XML parsing. I did this because I think its the
    best Python XML parsing lib. Its namespace support is better than
    everyone elses. It does however have this funky behaviour of having to
    convert everything to unicode objects before its useful. If you know how
    to get around this please e-mail me.
"""
import amara

def amara_to_unicode(obj):
    """Convert amara bindery objects into unicode. There should be a more
    graceful way to do this. Any thoughts?"""

    if isinstance(obj, list):
        return map(amara_to_unicode, obj)

    elif isinstance(obj, dict):
        func = lambda (x,y): (x, amara_to_unicode(y))
        return dict(map(func, obj.iteritems()))

    # Gotta be a better way to do this
    elif 'amara.bindery' in str(obj.__class__):
        return unicode(obj)

    return obj

class Parser(object):
    """Main parser that eats a Wordpress Export File (WXP)"""

    def __init__(self, file):
        self.file = file
        self.process_file(file)

    def process_file(self, file):
        """Process a WXP file. Store results in our parser objects"""

        doc = amara.parse(file)

        entries = []
        for item in doc.xml_xpath('*//item'):

            get_node = lambda x: item.xml_xpath(x).pop()

            # TODO: Add support for other items like excerpt, etc...
            entry = {
                'id': get_node('wp:post_id'),
                'status': get_node('wp:status'),
                'title': item.title,
                'link': item.link,
                'creator': get_node('dc:creator'),
                'pub_date': item.pubDate,
                'content': get_node('content:encoded')}

            categories = item.xml_xpath('category')

            cat_filter = lambda x: getattr(x, 'domain', False) == 'category'
            entry['categories'] = set(filter(cat_filter, categories))

            tag_filter = lambda x: getattr(x, 'domain', False) == 'tag'
            entry['tags'] = set(filter(tag_filter, categories))


            entries.append(entry)

        self.entries = map(amara_to_unicode, entries)
