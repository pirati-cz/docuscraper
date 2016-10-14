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
    return md_text

def get_image(ns, ns_short, text):
    name = re.search(re_image, text).group(1)
    img_url = url['domain'] + url['media'] + ns + '/' + name
    img_dir = join(ns_short, 'img')
    if not isdir(img_dir):
        mkdir(img_dir)
    urlretrieve(img_url, join(img_dir, name))
    return (name, img_url)

def get_article(item):
    txt_url = re.sub(re_parse_url, re_paste_url, item['rdf:about'])
    date = parse_datetime(item.find('dc:date').string).strftime('%Y-%m-%d')
    title = item.find('title').string
    title_web = re.sub(r' ', r'-', unidecode(title))
    docu = str(urlopen(txt_url).read().decode("utf-8"))

    img_name, img_url = get_image(ns, ns_short, docu)

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
        article = get_article(item)
        articles.append(article)
        break
    return articles

articles = scrapper()

print("Now we have article in var articles")
