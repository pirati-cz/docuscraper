    #!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
"""

import hashlib
import unittest
import shutil, tempfile
from os import path
from io import StringIO
from unittest.mock import patch

from docuscraper.scraper import find_main_img_in_text, docu_uri_to_url
from docuscraper.export import get_image

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
        " {{regiony:praha:tiskove-zpravy:konference.jpg?300 |Piráti na tiskové konferenci}} "),
    'fb': ("1452505_10151955999839039_1256076451_n.jpg", "",
        "https://scontent-a-ams.xx.fbcdn.net/hphotos-frc3/q71/s720x720/1452505_10151955999839039_1256076451_n.jpg",
        "https://scontent-a-ams.xx.fbcdn.net/hphotos-frc3/q71/s720x720/1452505_10151955999839039_1256076451_n.jpg",
        "{{https://scontent-a-ams.xx.fbcdn.net/hphotos-frc3/q71/s720x720/1452505_10151955999839039_1256076451_n.jpg?480 |}}"),
    'no-img': (None, None, None, None, " Zde není obrázek  ")
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

    @unittest.skip("Non actual link (403)")
    def test_fb(self):
        uri, desc, rest = find_main_img_in_text(imgs['fb'][4])
        self.assertEqual(imgs['fb'][2], uri)
        self.assertEqual(imgs['fb'][1], desc)

    def test_no_img(self):
        with patch('sys.stderr', new=StringIO()) as fakeOutput:
            uri, desc, rest = find_main_img_in_text(imgs['no-img'][4])
            self.assertIn('ERROR', fakeOutput.getvalue().strip())
        self.assertEqual(imgs['no-img'][2], uri)
        self.assertEqual(imgs['no-img'][1], desc)

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

    @unittest.skip("Non actual link (403)")
    def test_fb(self):
        img_url, img_namespace = docu_uri_to_url(ns, imgs['fb'][2])
        self.assertEqual(imgs['fb'][3], img_url)
        self.assertEqual(imgs['fb'][0], img_namespace)

class Download(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    @unittest.skip()
    def test_download(self):
        url = imgs['url-wiki'][3]
        name = imgs['url-wiki'][0]
        get_image(url, name, dir=self.test_dir)
        digest1 ='43150ac39cd996c4e267051e567a2edb'
        digest2 = hashlib.md5(open(join(self.test_dir, name), 'rb').read()).hexdigest()
        self.assertEqual(digest1, digest2)
