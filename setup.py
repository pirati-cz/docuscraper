#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
from setuptools import (setup, find_packages)
from docu-scraper import (__version__, __author__, __email__, __license__, __doc__)

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

setup(
	# Basic
	name='docu-scraper',
	version=__version__,
	packages=find_packages(),
	# Entry ponit
	entry_points={
		'console_scripts': [
			'docuscraper = docuscraper:main',
		]
	},

	# Requirements
	install_requires=["wget", "dateutils", "markdown", "ConfigArgParse", "sh" ],

	package_data={
		'byro': []
	},

	# About
	author=str(__author__),
	author_email=__email__,
	description='Scraper for DocuWiki. Scrapes articles and convert into markdown (for jekyll/gh-pages)',
	license=__license__,
	long_description=__doc__,
	keywords="DocuWiki markdown",
	url='',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Natural Language :: English',
		'Natural Language :: Czech',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Utilities'
	]
)
