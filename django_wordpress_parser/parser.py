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

            cat_tags = item.xml_xpath('category')
            info['categories'] = self._get_categories(cat_tags)
            info['tags'] = self._get_tags(cat_tags)

            info['comments'] = self._get_comments(item)

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

    def _parse_datetime(self, input):
        """Another method to parse a full datetime"""
        return datetime.strptime(input, "%Y-%m-%d %H:%M:%S")
        

    def _get_categories(self, items):
        """Return only categories from the items"""
        return _to_unicode([item for item in items if \
                getattr(item, 'domain', None) == 'category'])

    def _get_tags(self, items):
        """Return only tags from the items"""
        return _to_unicode([item for item in items if \
                getattr(item, 'domain', None) == 'tag'])

    def _get_comments(self, item):
        """Return comments from the item"""

        return [self._parse_comment(comment) for comment in \
                item.xml_xpath('wp:comment')]

    def _parse_comment(self, comment):
        """Parse an individual comment into a usable format"""

        get_node = lambda x: comment.xml_xpath(x).pop()

        new_comment = _to_unicode({
            "id": get_node("wp:comment_id"),
            "author": get_node("wp:comment_author"),
            "email": get_node("wp:comment_author_email"),
            "url": get_node("wp:comment_author_url"),
            "ip": get_node("wp:comment_author_IP"),
            "datetime": get_node("wp:comment_date"),
            "content": get_node("wp:comment_content"),
            "status": get_node("wp:comment_approved")})


        new_comment['id'] = int(new_comment['id'])
        new_comment['status'] = self._parse_status(new_comment['status'])
        new_comment['datetime'] = self._parse_datetime(new_comment['datetime'])

        return new_comment

    def _parse_status(self, status):
        """Wordpress has a funky way of returning status values. Sometimes it
        returns a number, and sometimes it returns a number. This method 
        normalizes all values to strings"""

        return {
            "0": "unapproved",
            "1": "approved"}.get(status, status)
            
if __name__ == "__main__":
    import sys
    import pprint
    file = sys.argv[1]
    parser = Parser(file)
    for entry in parser.entries:
        pprint.pprint(entry)
