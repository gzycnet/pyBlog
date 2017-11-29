#coding: utf-8

from __future__ import unicode_literals
from apps.account.views import *
urls = [
    (r'reg', RegHandler),
    (r'login', LoginHandler),
    (r'logout', LogoutHandler),
]