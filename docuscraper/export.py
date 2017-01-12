import sys
from os import mkdir
from os.path import join, isdir, isfile
import urllib
from urllib.request import urlopen
from wand.image import Image

from .settings import *

def export_2_cmd(articles):
    """
    Print names of articles into CMD
    """
    for article in articles:
        print(article['title'])

def get_image(url, name, dir=None, size=(600, 337)):
    """
    Download and resize image
    """
    if dir:
        img_filename = dir
    else:
        img_filename = join(ns_short, 'img', name)

    response = urlopen(url)
    try:
        with Image(file=response) as img:
            img.resize(size[0], size[1])
            img.save(filename=img_filename)
    finally:
        response.close()

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
    if not isdir(join(ns_short, 'img')):
        mkdir(join(ns_short, 'img'))
    for article in articles:
        try:
            get_image(article['img']['url'], article['img']['name'])
        except:
            print('ERROR', article['title'], article['img']['url'], file=sys.stderr)
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
            """ % (article['title'], article['img']['name'], article['date'])
            fd.write(metadata)
            fd.write(article['content']['md'])
