#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Settings
url = {
    'domain': 'https://www.pirati.cz/',
    'ns_feed': 'feed.php?mode=list&linkto=current&ns=',
    'export': '_export/raw/',
    'media': '_media/'
}
ns = 'regiony:praha:tiskove-zpravy'
ns_short  = 'praha'
filename = ns_short + '.feed'
converter_bin = './DokuWiki-to-Markdown-Converter/convert.php'
converter_git = 'https://github.com/ludoza/DokuWiki-to-Markdown-Converter'

# Regular expressions
re_parse_url = r"%s(?P<ns>[/\W]*)" % url['domain']
re_paste_url = r"%s%s\g<ns>" % (url['domain'], url['export'])
re_removes = [

    #sed  -i 's/
    # {{\s*\([^?|}]\+\?\)\(?[^|}]\+\?\)\?\s*\(|\(.\+\?\)\)\?}} /
    # ![\4](\1)
    #/g' "$file";
]
re_image = r'{{\s*(?P<filename>(?P<name>\w*).jpg)\?[0-9]*\s*}}'
re_replace = [
    ('~~NOTOC~~', ''),
    ('~~READMORE~~', ''),
    ('===== BOX:related =====', ''),
    (r'{{\s*(?P<filename>(?P<name>\w*).jpg)\?[0-9]*\s*}}', r'[\g<name>](\g<filename>)')
]
