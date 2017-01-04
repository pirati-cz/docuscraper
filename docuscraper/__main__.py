#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import re
from os import mkdir
from os.path import join, isdir, isfile
from subprocess import call
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
from unidecode import unidecode
from django.utils.dateparse import parse_datetime
from .settings import *

def dokuwiki_2_md_convertor(ns, name, text):
    """
    Return text in markdown.
    Converts doku wiki text via DokuWiki-to-Markdown-Converter
    Needs create a file (in namespace ns)
    """
    txt_filepath = join(ns, name + '.txt')
    md_filepath = join(ns, name + '.md')

    with open(txt_filepath, 'w') as fd:
        fd.write(text)
    print('---------------------------- (%s)' % name)
    call(["php", converter_bin, txt_filepath])
    print('---------------------------- (DokuWiki convertor messages end)')
    with open(md_filepath, 'r') as fd:
        md_text = fd.read()
    md_text2 = re.sub(re_image_md, r'', md_text)    # remove inline image
    return re.sub(re_header_md, r'', md_text2)      # remove inline header

def get_image(ns, ns_short, text):
    try:
        name = re.search(re_image, text).group(1)
        # TODO: delete from text
    except:
        print("IMG %s se nepodařilo rozluštit" % text)
        return (None, None)

    img_dir = join(ns_short, 'img')
    if not isdir(img_dir):
        mkdir(img_dir)

    if ":" in name:
        # define by namespaces
        img_url = url['domain'] + url['media'] + name
        # TODO: delete namespace from name
    else:
        img_url = url['domain'] + url['media'] + ns + '/' + name

    try:
        urlretrieve(img_url, join(img_dir, name))
    except:
        print("IMG %s jsme nenalezli" % img_url)
        return (None, None)

    # TODO: resize img to 600x337

    return (name, img_url)


def webalize_title(title):
    x = re.sub(r' ', r'-', unidecode(title))
    return re.sub(r':', r'', unidecode(x))

def get_article(item):
    try:
        txt_url = re.sub(re_parse_url, re_paste_url, item['rdf:about'])
        date = parse_datetime(item.find('dc:date').string).strftime('%Y-%m-%d')
        title = item.find('title').string
        title_web = webalize_title(title)
        docu = str(urlopen(txt_url).read().decode("utf-8"))
        img_name, img_url = get_image(ns, ns_short, docu)
    except Exception as e:
        print('Přeskakuji %s: %s %s' % (title, txt_url, e))
        raise Exception()

    for subs in re_replace:
        docu = re.sub(subs[0], subs[1], docu, re.M)

    return {
        'title': title,
        'title_web': title_web,
        'www_url': item['rdf:about'],
        'txt_url': txt_url,
        'date': date,
        'content': {
            'docu': docu,
            'md': dokuwiki_2_md_convertor(ns_short, title_web, docu)
        },
        'img': img_name
    }

def scrapper():
    if not isfile(converter_bin):
        print('You need DokuWiki-to-Markdown-Converter from %s' % converter_git)
        call(['git', 'clone', converter_git])

    if isdir(ns_short):
        print("Dir %s already exists => overwrite" % ns_short)
    else:
        mkdir(ns_short)

    if isfile(filename):
        print("Use cached version of RSS feed")
        with open(filename, 'r') as fd:
            html = fd.read()
    else:
        html = urlopen( url['domain'] + url['ns_feed'] + ns )


    soup = BeautifulSoup( html, "lxml")
    items = soup.find_all('item')
    articles = []
    for item in items:
        try:
            article = get_article(item)
        except:
            print()
            continue
        articles.append(article)
    return articles

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

articles = scrapper()
export_2_cmd(articles)
export_2_jekyll(articles)
