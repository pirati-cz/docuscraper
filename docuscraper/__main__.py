#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import sys

from .scraper import *
from .export import *

def main():
    articles = scrapper()
    export_2_cmd(articles)
    export_2_jekyll(articles)

if __name__ == "__main__":
	sys.exit(main())
