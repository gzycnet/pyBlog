#coding:utf-8
import os.path
import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import datetime

from bson.objectid import ObjectId
import hashlib
import uuid

from importlib import import_module

from base import BaseHandler

from databaseCase import *

from apps.admin.views import *
from apps.account.views import *
from apps.blog.views import *
from apps.ucenter.views import *


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


from tornado.options import define, options
define("port", default=8800, help="run on the given port", type=int)



class IndexHandler(BaseHandler):
    def get(self):

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client

        db = client.pyblog
        articles = db.post.find().sort("date",-1).limit(20)


        tags = db.tags.find().limit(50)
        cateList = db.category.find()

        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)


        #self.render('blog/index.html',articles=articles,tags=tags,cateData=cateData)
        self.render('blog/home.html',articles=articles,tags=tags,cateData=cateData)

        #self.render('index.html')

    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error.\n" % status_code)



def include(module):
    res = import_module(module)
    urls = getattr(res, 'urls', res)
    return urls

def url_wrapper(urls):
    wrapper_list = []
    for url in urls:
        path, handles = url
        if isinstance(handles, (tuple, list)):
            for handle in handles:
                pattern, handle_class = handle
                wrap = ('/{0}{1}'.format(path, pattern), handle_class)
                wrapper_list.append(wrap)
        else:
            wrapper_list.append((path, handles))
    return wrapper_list


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        'login_url':'/account/login'
    }
    app = tornado.web.Application(
        url_wrapper([
            (r"/", IndexHandler),
            (r"", include('apps.blog.urls')),
            (r"ucenter/", include('apps.ucenter.urls')),
            (r"account/", include('apps.account.urls')),
            (r"admin/", include('apps.admin.urls')),
            (r".*", BaseHandler),
        ]),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()