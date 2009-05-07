#!/usr/bin/env python
import sys, re, codecs
from optparse import OptionParser

# coarse hack for coercing input to utf-8
reload(sys)
sys.setdefaultencoding('utf_8')

def strip_chars(f,extra=u''):
    remove_re = re.compile(u'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F%s]'
                           % extra)
    i = 1
    stripped = 0
    for line in f:
        new_line, count = remove_re.subn('', line) 
        if count > 0:
            plur = ((count > 1) and u's') or u''
            sys.stderr.write('Line %d, removed %s character%s.\n'
                             % (i, count, plur))
        sys.stdout.write(new_line)
        stripped = stripped + count
        i = i + 1
    sys.stderr.write('Stripped %d characters from %d lines.\n'
                     % (stripped, i))

def main():
    p = OptionParser("usage: strip_xml_entities.py file/to/parse.xml")
    p.add_option('-c','--chars',dest='chars',
                 help="additional CHARS to strip",
                 metavar="CHARS")
    (options, args) = p.parse_args()
    extra = options.chars or u''

    # if positional arg, use that file, otherwise stdin
    fin = (len(args) and open(args[0], 'r')) or sys.stdin
    strip_chars(fin, extra)
    fin.close()

if __name__ == '__main__':
    sys.exit(main())
