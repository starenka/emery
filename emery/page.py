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
        data = pq(table)
        head = [pq(th).text() for th in data.find('th')] or None
        tds_in_row = len(pq(data.find('tr')).eq(0).find('th' if head else 'td'))
        return Dataset(
            *list(izip_longest(*[iter([pq(td).text() for td in data.find('td')])] * tds_in_row, fillvalue=None)),
            headers=head
        )

    @property
    def links(self):
        return self.get_links()

    def get_links(self, selector=None):
        selector = selector if selector else 'a'
        return [(one.text(), one.attr('href')) for one in self._get_elements(selector)]

    @property
    def tables(self):
        return self.get_tables()

    def get_tables(self, selector=None):
        selector = selector if selector else 'table'
        return map(Page.parse_table, map(lambda x: x.html(), self._get_elements(selector)))

    @property
    def images(self):
        return self.get_images()

    def get_images(self, selector=None):
        selector = selector if selector else 'img'
        return [(one.attr('alt'), one.attr('src')) for one in self._get_elements(selector)]

    @property
    def text(self):
        return pq(self.html).text()