#coding: utf-8

from __future__ import unicode_literals
from apps.blog.views import *
urls = [
    (r"blog/", BlogHandler),
    (r't/([%a-fA-F0-9]+|\w+)/$', BlogTagsHandler),
    (r'c/(\w+)/$', BlogCategoryHandler),
    (r'a/(\w+)', ArticleDetailHandler),
    (r'comment/$', CommentHandler),
    (r'addlink/$', AddLinkHandler),
]