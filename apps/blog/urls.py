#coding: utf-8

from __future__ import unicode_literals
from apps.blog.views import *
urls = [
    (r"blog/", BlogHandler),
    (r't/([%a-fA-F0-9]+|[\s\S]+|\w+)/$', BlogTagsHandler),
    (r'c/(\w+)/$', BlogCategoryHandler),
    (r'a/(\w+)/', ArticleDetailHandler),
    #(r'archive/([%a-fA-F0-9]+|[\s\S]+|\w+)/$', BlogArchiveHandler),
    (r'archive/(\d{4}-\d{2})/$', BlogArchiveHandler),
    (r'comment/$', CommentHandler),
    (r'addlink/$', AddLinkHandler),
]