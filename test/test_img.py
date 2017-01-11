    #!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
"""

import unittest
from docuscraper.scraper import find_main_img_in_text, docu_uri_to_url

# test data
imgs = {
    # (name, desc, uri, url, wiki text)
    'url': ("Pirati_-_logotyp.jpg", "Logotyp Pirátů",
        "https://upload.wikimedia.org/wikipedia/commons/1/11/Pirati_-_logotyp.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/1/11/Pirati_-_logotyp.jpg",
        "{{https://upload.wikimedia.org/wikipedia/commons/1/11/Pirati_-_logotyp.jpg|Logotyp Pirátů}}"),
    'url-wiki': ("smlouvy.png", "Smlouvy",
        "https://www.pirati.cz/_media/tiskove-zpravy/smlouvy.png?300",
        "https://www.pirati.cz/_media/tiskove-zpravy/smlouvy.png",
        " {{https://www.pirati.cz/_media/tiskove-zpravy/smlouvy.png?300 |Smlouvy}} "),
    'name1': ("jmi-lidr.jpg", "",
        "jmi-lidr.jpg?300&nolink",
        "https://www.pirati.cz/_media/regiony/praha/tiskove-zpravy/jmi-lidr.jpg",
        " {{jmi-lidr.jpg?300&nolink }}"),
    'name2': ("jakub_michalek.jpg", "Lídr Pirátů v Praze Jakub Michálek",
        "jakub_michalek.jpg?200x250",
        "https://www.pirati.cz/_media/regiony/praha/tiskove-zpravy/jakub_michalek.jpg",
        " {{jakub_michalek.jpg?200x250 |Lídr Pirátů v Praze Jakub Michálek}} "),
    'namespace1': ("smlouvy.png", "Smlouvy",
        ":tiskove-zpravy:smlouvy.png?direct&250",
        "https://www.pirati.cz/_media/tiskove-zpravy/smlouvy.png",
        " {{:tiskove-zpravy:smlouvy.png?direct&250 |Smlouvy}} "),
    'namespace2': ("konference.jpg", "Piráti na tiskové konferenci",
        "regiony:praha:tiskove-zpravy:konference.jpg?300",
        "https://www.pirati.cz/_media/regiony/praha/tiskove-zpravy/konference.jpg",
        " {{regiony:praha:tiskove-zpravy:konference.jpg?300 |Piráti na tiskové konferenci}} ")
}
ns = 'regiony:praha:tiskove-zpravy'

class Find_img(unittest.TestCase):

    def test_url(self):
        uri, desc, rest = find_main_img_in_text(imgs['url'][4])
        self.assertEqual(imgs['url'][2], uri)
        self.assertEqual(imgs['url'][1], desc)

    def test_url_wiki(self):
        uri, desc, rest = find_main_img_in_text(imgs['url-wiki'][4])
        self.assertEqual(imgs['url-wiki'][2], uri)
        self.assertEqual(imgs['url-wiki'][1], desc)

    def test_name_1(self):
        uri, desc, rest = find_main_img_in_text(imgs['name1'][4])
        self.assertEqual(imgs['name1'][2], uri)
        self.assertEqual(imgs['name1'][1], desc)

    def test_name_2(self):
        uri, desc, rest = find_main_img_in_text(imgs['name2'][4])
        self.assertEqual(imgs['name2'][2], uri)
        self.assertEqual(imgs['name2'][1], desc)

    def test_namespace_1(self):
        uri, desc, rest = find_main_img_in_text(imgs['namespace1'][4])
        self.assertEqual(imgs['namespace1'][2], uri)
        self.assertEqual(imgs['namespace1'][1], desc)

    def test_namespace_2(self):
        uri, desc, rest = find_main_img_in_text(imgs['namespace2'][4])
        self.assertEqual(imgs['namespace2'][2], uri)
        self.assertEqual(imgs['namespace2'][1], desc)

class Uri_2_url(unittest.TestCase):

    def test_url(self):
        img_url, img_name = docu_uri_to_url(ns, imgs['url'][2])
        self.assertEqual(imgs['url'][3], img_url)
        self.assertEqual(imgs['url'][0], img_name)

    def test_url(self):
        img_url, img_name = docu_uri_to_url(ns, imgs['url-wiki'][2])
        self.assertEqual(imgs['url-wiki'][3], img_url)
        self.assertEqual(imgs['url-wiki'][0], img_name)

    def test_name_1(self):
        img_url, img_name = docu_uri_to_url(ns, imgs['name1'][2])
        self.assertEqual(imgs['name1'][3], img_url)
        self.assertEqual(imgs['name1'][0], img_name)

    def test_name_2(self):
        img_url, img_name = docu_uri_to_url(ns, imgs['name2'][2])
        self.assertEqual(imgs['name2'][3], img_url)
        self.assertEqual(imgs['name2'][0], img_name)

    def test_namespace_1(self):
        img_url, img_namespace = docu_uri_to_url(ns, imgs['namespace1'][2])
        self.assertEqual(imgs['namespace1'][3], img_url)
        self.assertEqual(imgs['namespace1'][0], img_namespace)

    def test_namespace_2(self):
        img_url, img_namespace = docu_uri_to_url(ns, imgs['namespace2'][2])
        self.assertEqual(imgs['namespace2'][3], img_url)
        self.assertEqual(imgs['namespace2'][0], img_namespace)
