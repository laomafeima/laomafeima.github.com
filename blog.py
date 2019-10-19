#!/usr/bin/env python3
# coding: utf-8


import os
from configparser import ConfigParser
from hashlib import md5
from html.parser import HTMLParser

from markdown import Markdown
from pypinyin import pinyin as too_pinyin, Style as PinyinStyle
from jinja2 import Template


doc_item_tpl = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="markdown-hash" content="{{ hash }}">

    <title>{{ title }}</title>

    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
    <div id="go-back" onclick="javascript:history.back(-1);">↼</div>
</header>
<div class="markdown-body">
    {{ content}}
</div>
<div class="bottom">
    {% for tag in tags %}
    <a href="{{ tag.url}}" class="tag" ># {{ tag.tag }}</a>
    {% endfor %}
    <time datetime="{{ date }}">{{ date }}</time>
</div>
<footer>
    <a href="/notes.html" target="_blank" class="muted"><i>笔记</i></a>
    <i>/</i>
    <a href="/tags.html" target="_blank" class="muted"><i>标签</i></a>
    <i>/</i>
    <a href="/about.html" target="_blank" class="muted"><i>关于</i></a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""

index_tpl = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老馬</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
    <h2 class="logo-text">{{ blog_name }}</h2>
</header>
<div class="content">
    <ul class="posts">
        {% for item in seq %}
        <li><div class="post-name"><small class="datetime muted">{{ item.date }}</small><a href="{{ item.url }}">{{ item.title }}</a></div></li>
        {% endfor %}
    </ul>
</div>
<footer>
    <a href="/notes.html" target="_blank" class="muted"><i>笔记</i></a>
    <i>/</i>
    <a href="/tags.html" target="_blank" class="muted"><i>标签</i></a>
    <i>/</i>
    <a href="/about.html" target="_blank" class="muted"><i>关于</i></a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""

tag_tpl = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ tag_group.tag }}</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
    <h2 class="tag-big"># {{ tag_group.tag }}</h2>
</header>
<div class="content">
    <ul class="posts">
        {% for item in tag_group.docs %}
        <li><div class="post-name"><small class="datetime muted">{{ item.date }}</small><a href="{{ item.url }}">{{ item.title }}</a></div></li>
        {% endfor %}
    </ul>
</div>
<footer>
    <a href="/notes.html" target="_blank" class="muted"><i>笔记</i></a>
    <i>/</i>
    <a href="/tags.html" target="_blank" class="muted"><i>标签</i></a>
    <i>/</i>
    <a href="/about.html" target="_blank" class="muted"><i>关于</i></a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""
tags_tpl = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>标签</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
<header>
    <h2 class="logo-text">标签</h2>
</header>
<div class="bottom">
    {% for tag in tags %}
    <a href="{{ tag.url}}" class="tag" ># {{ tag.tag }}</a>
    {% endfor %}
</div>
<footer>
    <a href="/notes.html" target="_blank" class="muted"><i>笔记</i></a>
    <i>/</i>
    <a href="/about.html" target="_blank" class="muted"><i>关于</i></a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""


class Blog(object):

    def get_dict(self):
        return self.__dict__

    def __init__(self, config, blog_name=None):
        self.blog_name = blog_name
        self.config = config
        self.doc_item_tpl = None
        self.index_tpl = None
        self.tag_tpl = None
        self.tags_tpl = None
        self.docs = []
        self.tags = {}

    def tpl_parser(self):
        self.doc_item_tpl = Template(doc_item_tpl)
        self.index_tpl = Template(index_tpl)
        self.tag_tpl = Template(tag_tpl)
        self.tags_tpl = Template(tags_tpl)


    def start(self):
        self.tpl_parser()
        self.loop_item()
        self.sort()
        self.write_doc()
        if self.config.has_option("base", "index_path"):
            self.write_index()
        if self.config.has_option("base", "tags_path"):
            self.write_tags()

    def sort(self):
        self.docs = sorted(self.docs, key=lambda d: d.date, reverse=True)
        for i in self.docs:
            for tag in i.tags:
                if tag['tag'] in self.tags.keys():
                    self.tags[tag['tag']]["docs"].append(i)
                else:
                    self.tags[tag['tag']] = {
                            "tag": tag['tag'],
                            "url":tag['url'],
                            "docs": [i],
                            }
    
    def write_doc(self):
        for i in self.docs:
            i.write()

    def write_index(self):
        html = self.index_tpl.render(blog_name=self.blog_name, seq=self.docs)
        index = self.config.get("base", "index_path")
        f = open(index, "w")
        f.write(html)
        f.close()

    def write_tags(self):
        tags_path = self.config.get("base", "tags_path")
        for tag_group in self.tags.values():
            html = self.tag_tpl.render(tag_group=tag_group)
            f = open(self.get_tag_path(tag_group), "w")
            f.write(html)
            f.close()

        html = self.tags_tpl.render(tags=self.tags.values())
        f = open(tags_path, "w")
        f.write(html)
        f.close()

    def get_tag_path(self, item):
        url = item['url']
        return ".%s"%url


    def loop_item(self):
        md_dir = self.config.get("base", "markdown")
        for i in os.listdir(md_dir):
            if not i.endswith(".md"):
                continue
            file_path = os.path.join(md_dir, i)
            self.item_parser(file_path)


    def item_parser(self, file_path):
        out_path_tpl = self.config.get("base", "html_path")
        doc_url = self.config.get("base", "doc_url")
        tag_url = self.config.get("base", "tag_url")
        doc = Document(file_path, out_path_tpl, doc_url, tag_url,
                self.doc_item_tpl)
        if doc.parser():
            self.docs.append(doc)

class Utils(object):

    def get_pinyin(word):
        pinyin = too_pinyin(word, style=PinyinStyle.NORMAL)
        return [str(i.pop()).strip() for i in pinyin]

    def get_markdown():
        markdown = Markdown(extensions=['tables', 'meta', 'fenced_code',
            'nl2br', 'sane_lists'])
        return markdown


class Document(dict):

    def get_dict(self, name):
        return self.__dict__

    def __init__(self, in_path, out_path_tpl, doc_url, tag_url, html_tpl):
        self.in_path = in_path
        self.out_path_tpl = out_path_tpl
        self.doc_url = doc_url
        self.tag_url = tag_url
        self.html_tpl = html_tpl
        self.has_update = False
        self.out_path = ""
        self.hash = ""
        self.html = ""
        self.title = ""
        self.tags = []
        self.date = ""
        self.url = ""

    def parser(self):
        md_file = open(self.in_path,'rb')
        content = md_file.read()
        text = content.decode("utf-8")
        md_file.close()
        if self.markdown_parser(text) is False:
            return False
        self.hash = md5(content).hexdigest()
        if self.hash != self.get_html_hash(self.out_path):
            self.has_update = True
        return True

    def get_html_hash(self, html_path):
        if not os.path.exists(html_path):
            return ""
        f = open(html_path, "r")
        html = MyHTMLParser()
        html.feed(f.read())
        if "hash" in html.data.keys():
            return html.data['hash']
        return ""

    def write(self):
        if self.has_update:
            f = open(self.out_path, "w")
            f.write(self.html)
            f.close()

    def markdown_parser(self, text):
        md = Utils.get_markdown()
        self.content = md.convert(text)
        if not all([(i in md.Meta.keys()) for i in ["title", "date"]]):
            return False
        result = {}
        self.title = ",".join(md.Meta['title'])
        self.date = ",".join(md.Meta['date'])
        self.tags = self.get_md_tags(md.Meta['tags']) if "tags" in md.Meta.keys() else []
        self.html = self.html_tpl.render(self.__dict__)

        pinyin = Utils.get_pinyin(self.title)
        file_name = "-".join(pinyin)
        self.url = self.doc_url % file_name
        self.out_path = self.out_path_tpl % file_name
        return True

    def get_md_tags(self, tags):
        tags = "".join(tags).split(",")
        return [{"tag": i.strip(), "url": self.tag_url % i.strip()} for i in tags]


class MyHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.data = {}

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            if len(attrs) > 1 and len(attrs[0]) > 1 and attrs[0][0] == "name" \
                    and attrs[0][1] == "markdown-hash":
                self.data['hash'] = attrs[1][1]

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

def main():
    annual_config = """
[base]
markdown = ./markdown/annual/
html_path = ./annual/%%s.html
tag_path = ./tag/%%s.html
index_path = ./annual/index.html
doc_url = /annual/%%s.html
tag_url = /tag/%%s.html
"""
    annual = Blog(config_parser(annual_config), "年度目标")
    annual.start()

    note_config = """
[base]
markdown = ./markdown/note/
html_path = ./blog/%%s.html
tag_path = ./tag/%%s.html
index_path = ./notes.html
tags_path = ./tags.html
doc_url = /blog/%%s.html
tag_url = /tag/%%s.html
"""
    note = Blog(config_parser(note_config), "笔记")
    note.start()



    blog_config = """
[base]
markdown = ./markdown/
html_path = ./blog/%%s.html
tag_path = ./tag/%%s.html
index_path = ./index.html
tags_path = ./tags.html
doc_url = /blog/%%s.html
tag_url = /tag/%%s.html
"""
    blog = Blog(config_parser(blog_config), "老馬")
    blog.tags = note.tags
    blog.start()

def config_parser(config):
    cfg = ConfigParser()
    cfg.read_string(config)
    return cfg


if __name__ == "__main__":
    main()
