#coding: utf-8

from __future__ import unicode_literals
from apps.ucenter.views import *
urls = [
    (r'post$', PostArticleHandler),
    (r'edit/(\w+)', EditArticleHandler),
    (r'list$', AuthorArticleListHandler),
]