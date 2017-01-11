from os import mkdir
from os.path import join, isdir, isfile

def export_2_cmd(articles):
    """
    Print names of articles into CMD
    """
    for article in articles:
        print(article['title'])

def export_2_jekyll(articles):
    """
    Exports articles into jekyll format.
    Creates files:
        - yaml metadata
        - text in markdown
        - filename e.g. 2016-12-30-my-awesome-title.md
    """
    if not isdir(join(ns_short, '_posts')):
        mkdir(join(ns_short, '_posts'))
    for article in articles:
        filename = join(ns_short, '_posts', article['date'] + '-' + article['title_web'] + '.md')
        with open(filename, 'w') as fd:
            metadata = """---
title:	  %s
layout:	  post
category: blog
author:	  Piráti Praha
image:	  %s
tags:
date:	  %s
---
            """ % (article['title'], article['img'], article['date'])
            fd.write(metadata)
            fd.write(article['content']['md'])
