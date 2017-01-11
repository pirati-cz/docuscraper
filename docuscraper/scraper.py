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

def find_main_img_in_text(text):
    """
    Finds main (cover) image in article text
    Returns image uri, image description and rest of the text
    """
    try:
        res1, text_2 = re.split(r'\s*\}\}', text, maxsplit=1)
        text_1, res2 = re.split(r'\{\{\s*', res1, maxsplit=1)
    except:
        print("Error", text)
        exit()
    rest = text_1 + text_2
    print(rest)
    try:
        uri, desc = re.split(r'\s*\|\s*', res2, maxsplit=1)
    except ValueError:
        uri = res2
        desc = ""
    return (uri, desc, rest)

def docu_uri_to_url(ns, uri):
    """
    From dokuwiki uri prepare url
    """
    uri2 = re.split('\?', uri)[0]
    if uri2.startswith(":"):
        uri2 = uri2[1:]

    try:
        # Is standard standalone url?
        urlopen(uri)
        img_url = uri2
    except:
        # Not a url
        if ":" in uri:
            # Defined by namespaces in dokuwiki, separated by :
            img_url = url['domain'] + url['media'] + re.sub(":", "/", uri2)
        else:
            # Uri reference to actual namespace
            img_url = url['domain'] + url['media'] + re.sub(":", "/", ns) + '/' + uri2
    img_name = re.split("/", img_url)[-1]
    return img_url, img_name

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

        img_uri, desc, rest = find_main_img_in_text(ns, ns_short, docu)
        img_url, img_name = docu_uri_to_url(img_uri)

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
            break
        except:
            print()
            continue
        articles.append(article)
    return articles
