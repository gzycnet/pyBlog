#coding: utf-8

from __future__ import unicode_literals
from apps.admin.views import *
urls = [
    (r"", AdminHandler),
    (r'auditUser/$', AuditUserHandler),
    (r'auditLink/$', AuditLinksHandler),
    (r'links$', AdminLinksHandler),
    (r'ads$', AdminAdsHandler),
    (r'upload/$', UploadHandler),
]