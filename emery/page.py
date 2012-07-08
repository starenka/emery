#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import izip_longest

import requests
from BeautifulSoup import BeautifulSoup
from html5tidy import tidy
from pyquery import PyQuery as pq
from tablib import Dataset


class Page(object):
    def __init__(self, url=None, html=None, fix_html=True):
        if html:
            self.html = html
        else:
            self.html = requests.get(url).content
        if fix_html:
            self.html = self._fix_document(self.html)

    def _fix_document(self, doc, use_soup=False):
        if use_soup:
            soup = BeautifulSoup(doc)
            soup.prettify()
            doc = unicode(soup)
        else:
            doc = tidy(doc)
        return doc

    def _get_elements(self, selector):
        return map(lambda x: pq(x), pq(self.html).find(selector))

    @staticmethod
    def parse_table(table):
        """
            parses html table into tablib object
        """
        data = pq(table)
        head = [pq(th).text() for th in data.find('th')] or None
        #determine how many cells are in a single row
        tds_in_row = len(pq(data.find('tr')).eq(0).find('th' if head else 'td'))
        #get all cells and split'em by rows
        tds_by_row = list(izip_longest(*[iter([pq(td).text() for td in data.find('td')])] * tds_in_row, fillvalue=None))
        return Dataset(*tds_by_row, headers=head)

    @property
    def links(self):
        """
            returns all links on a page as a list of (title, href) tuples
        """
        return self.get_links()

    def get_links(self, selector=None):
        """
            returns all links matching given selector as a list of (title, href) tuples
        """
        selector = selector if selector else 'a'
        return [(one.text(), one.attr('href')) for one in self._get_elements(selector)]

    @property
    def tables(self):
        return self.get_tables()

    def get_tables(self, selector=None):
        """
            returns all tables on page as a list of tablib objects
            you can represent such table using list(), .json, .yaml, .csv, .xls
            for more details check tablib docs https://github.com/kennethreitz/tablib/#exports
        """
        selector = selector if selector else 'table'
        return map(Page.parse_table, map(lambda x: x.html(), self._get_elements(selector)))

    @property
    def images(self):
        """
            returns all links on a page as a list of (alt, src) tuples
        """
        return self.get_images()

    def get_images(self, selector=None):
        """
            returns all links matching given selector as a list of (alt, src) tuples
        """
        selector = selector if selector else 'img'
        return [(one.attr('alt'), one.attr('src')) for one in self._get_elements(selector)]

    @property
    def text(self):
        """
            returns text representation of page
        """
        return pq(self.html).text()