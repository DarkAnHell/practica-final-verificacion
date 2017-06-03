#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
import StringIO
from lxml import etree
import xml.etree.ElementTree as ET

def get_articles_by_date(date):
    # result will have a list of dicts with articles title as key and URL as value
    articles = list()
    parser = etree.HTMLParser()

    # All dates URL will start with this pattern
    URL = "http://elpais.com/tag/fecha/"
    # the date comes with the following formar dd/mm/yyyy
    try:
        d = date.split("/")
        URL += d[2] + d[1] + d[0]
    except Exception, e:
        raise Exception("invalid date format")

    r = requests.get(URL)
    if r.status_code != 200:
        raise Exception("something went wrong, status code != 200 OK. Status code: %d" % r.status_code)

    resp = r.text
    try:
        tree = etree.parse(StringIO.StringIO(resp), parser=parser)
        titles = map(unicode, tree.xpath('//h2[@class="articulo-titulo"]/a/text()'))
        articles_urls = tree.xpath('//h2[@class="articulo-titulo"]/a/@href')

#        if len(titles) != len(articles_urls):
#            raise Exception("something went wrong. Found: %d article titles and %d article URLs" % (len(titles), len(articles_urls)))
    except Exception, e:
        raise Exception("body doesn't contain valid HTML")

    for t, u in zip(titles, articles_urls):
        d = {"title": unicode(t), "url": "http:"+u}
        articles.append(d)
    return articles

def get_article_body(url):
    parser = etree.HTMLParser()
    content = ""
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("something went wrong, status code != 200 OK. Status code: %d" % r.status_code)
    resp = r.text

    tree = etree.parse(StringIO.StringIO(resp), parser=parser)
    body = tree.xpath('//*[@id="cuerpo_noticia"]/p')

    for element in body:
        content+= recursive_get_text(element)
    
    try:
        introduction = tree.xpath('//*[@id="articulo-introduccion"]/p')
        for element in introduction:
            content+= recursive_get_text(element)
    except:
        pass

    return content

def recursive_get_text(element):
    result=""
    for i in element.getchildren():
        result+=recursive_get_text(i)
    
    if(element.text):
        result+=element.text

    return result+" "

#print get_articles_by_date("30/05/2017")
#print get_article_body("http://economia.elpais.com/economia/2017/06/03/actualidad/1496488261_008848.html")
print get_article_body("http://cultura.elpais.com/cultura/2017/06/02/actualidad/1496411959_546950.html")
