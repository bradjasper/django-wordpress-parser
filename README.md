# django-wordpress-parser

django-wordpress-parser helps you migrate your blog from Wordpress to Django.

It takes an exported file from WXP exporter and grabs the blog entries and comments.

It allows you to easily take the data and import it into a custom blog application. It doesn't do everything for you, but helps with some of the heavy lifting.

Comments are extracted so they work with the standard Django comments application.

## Usage

    import django_wordpress_parser
    parser = django_wordpress_parser.Parser('wordpress.2009-01-31.xml')

    for entry in parser.entries:
        # Import entries into your blog here
        print entry


## Contact

Web: http://bradjasper.com<br>
Twitter: <a href="https://twitter.com/bradjasper">@bradjasper</a><br>
Email: <a href="mailto:contact@bradjasper.com">contact@bradjasper.com</a><br>
