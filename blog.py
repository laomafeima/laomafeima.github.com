#!/usr/bin/env python3
# coding: utf-8


import jinja2
import os
from configparser import ConfigParser
from hashlib import md5
from html.parser import HTMLParser

from markdown import Markdown
from pypinyin import pinyin as too_pinyin, Style as PinyinStyle
from jinja2 import Template


config = """
[base]
markdown = ./markdown/
blog_url = /blog/%%s.html
tag_url = /tag/%%s.html
"""

blog_item_tpl = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="markdown-hash" content="{{ hash }}">

    <title>{{ title }}</title>

    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/main.css">
    <link rel="stylesheet" href="/static/markdown.css">
</head>
<body>
<header>
    <a href="/" class="logo-link">
        <img alt="img" src="/static/favicon.png">
    </a>
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
    <a href="/about.html" target="_blank" class="muted">关于老馬</a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""

index_tpl = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>老馬</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
<header>
    <a href="/" class="logo-link">
        <img alt="img" src="/static/favicon.png">
    </a>
</header>
<div class="content">
    <ul class="posts">
        {% for item in seq %}
        <li><dev class="post-name"><small class="datetime muted">{{ item.date }}</small><a href="{{ item.url }}">{{ item.title }}</a></dev></li>
        {% endfor %}
    </ul>
</div>
<footer>
    <a href="/about.html" target="_blank" class="muted">关于老馬</a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""

tag_tpl = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ tag_group.tag }}</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/main.css">
</head>
<body>
<header>
    <h2 class="tag-big"># {{ tag_group.tag }}</h2>
</header>
<div class="content">
    <ul class="posts">
        {% for item in tag_group.blogs %}
        <li><dev class="post-name"><small class="datetime muted">{{ item.date }}</small><a href="{{ item.url }}">{{ item.title }}</a></dev></li>
        {% endfor %}
    </ul>
</div>
<footer>
    <a href="/about.html" target="_blank" class="muted">关于老馬</a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""
tags_tpl = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>标签</title>
    <link rel="icon" type="image/png" href="/static/favicon.png">
    <link rel="stylesheet" href="/static/main.css">
    <link rel="stylesheet" href="/static/markdown.css">
</head>
<body>
<header>
    <a href="/" class="logo-link">
        <img alt="img" src="/static/favicon.png">
    </a>
</header>
<div class="bottom">
    {% for tag in tags %}
    <a href="{{ tag.url}}" class="tag" ># {{ tag.tag }}</a>
    {% endfor %}
</div>
<footer>
    <a href="/about.html" target="_blank" class="muted">关于老馬</a>
</footer>
<script src="/static/min.js"></script>
</body>
</html>
"""




class Blog(object):


    def __init__(self):
        self.config = None
        self.blog_item_tpl = None
        self.index_tpl = None
        self.tag_tpl = None
        self.tags_tpl = None
        self.blogs = []

    def config_parser(self):
        cfg = ConfigParser()
        cfg.read_string(config)
        self.config = cfg
    
    def tpl_parser(self):
        self.blog_item_tpl = Template(blog_item_tpl)
        self.index_tpl = Template(index_tpl)
        self.tag_tpl = Template(tag_tpl)
        self.tags_tpl = Template(tags_tpl)


    def get_markdown(self):
        markdown = Markdown(extensions=['tables', 'meta', 'fenced_code'])
        return markdown

    def start(self):
        self.config_parser()
        self.tpl_parser()
        self.loop_item()
        self.index_parser()


    def index_parser(self):
        blogs = sorted(self.blogs, key=lambda d: d['date'], reverse=True)
        tags = {}
        for i in blogs:
            for tag in i['tags']:
                if tag['tag'] in tags.keys():
                    tags[tag['tag']]["blogs"].append(i)
                else:
                    tags[tag['tag']] = {
                            "tag": tag['tag'],
                            "url":tag['url'],
                            "blogs": [i],
                            }
        self.write_index(blogs)
        self.write_tag(tags)
    
    def write_index(self, blogs):
        html = self.index_tpl.render(seq=blogs)
        f = open("index.html", "w")
        f.write(html)
        f.close()


    def write_tag(self, tags):
        for tag_group in tags.values():
            html = self.tag_tpl.render(tag_group=tag_group)
            f = open(self.get_tag_path(tag_group), "w")
            f.write(html)
            f.close()

        html = self.tags_tpl.render(tags=tags.values())
        f = open("./tags.html", "w")
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
        md_file = open(file_path,'rb')
        content = md_file.read()
        text = content.decode("utf-8")
        item = self.markdown_parser(text)
        md_file.close()
        if item is None:
                return None
        item['hash'] = md5(content).hexdigest()
        self.write_blog(item)
        del(item['content'])
        self.blogs.append(item)

    def write_blog(self, item):
        html = self.blog_item_tpl.render(**item)
        html_path = self.get_blog_path(item)
        if not os.path.exists(html_path) or\
                self.get_html_hash(html_path) != item['hash']:
            f = open(html_path, "w")
            f.write(html)
            f.close()


    def get_html_hash(self, html_path):
        f = open(html_path, "r")
        html = MyHTMLParser()
        html.feed(f.read())
        if "hash" in html.data.keys():
            return html.data['hash']


    def get_blog_path(self, item):
        url = item['url']
        return ".%s"%url

    def markdown_parser(self, text):
        md = self.get_markdown()
        html = md.convert(text)
        if not all([(i in md.Meta.keys()) for i in ["title", "date"]]):
            return None
        result = {}
        result['title'] = ",".join(md.Meta['title'])
        result['date'] = ",".join(md.Meta['date'])
        result['tags'] = self.get_md_tags(md.Meta['tags']) if "tags" in md.Meta.keys() else []
        result['url'] = self.get_url(result['title'], md.Meta)
        result['content'] = html
        return result

    def get_md_tags(self, tags):
        tags = "".join(tags).split(",")
        url = self.config.get("base", "tag_url")
        return [{"tag": i.strip(), "url": url%i.strip()} for i in tags]


    def get_url(self, title, meta):
        if "url" in meta.keys():
            url = ",".join(meta['url'])
        else:
            pinyin = self.get_pinyin(title)
            url = "-".join(pinyin)
            url = self.config.get("base", "blog_url") % url
        return url



    def get_pinyin(self, word):
        pinyin = too_pinyin(word, style=PinyinStyle.NORMAL)
        return [str(i.pop()).strip() for i in pinyin]



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
    Blog().start()


if __name__ == "__main__":
    main()
