#coding:utf-8


from base import BaseHandler

import hashlib
import datetime
import os.path
import uuid
import tornado.web
from databaseCase import *
from bson import ObjectId


class RegHandler(BaseHandler):

    def get(self):
        user = self.current_user
        referer = self.get_argument('referer','/')
        if user:
            self.redirect(referer)
        else:
            self.render('reg.html',referer=referer)

    def post(self):
        email = self.get_argument('email','')
        password = self.get_argument('password','')
        password_repeat = self.get_argument('password_repeat','')
        type = self.get_argument('type','1')
        if email == '' or '-' in email:
            self.render('error.html',msg=u'非法账号 不能为空、且不能含有[-]')

        elif password == '' or password_repeat =='':
            self.render('error.html',msg=u'密码不能为空，且要6-18位!')
        elif password != password_repeat:
            self.render('error.html',msg=u'密码不一致！')

        #查询
        else:
            mongo = MongoCase()
            mongo.connect()
            client = mongo.client
            db = client.pyblog

            if db.user.find({"account":email}).count()>0:
                msg = email+u'已经注册过了'
                msg += u'<a href="/login">登录</a>'
                self.render('error.html',msg=msg)

            else:

                m = hashlib.md5()
                m.update(password)
                sign = m.hexdigest()
                mongo = MongoCase()
                mongo.connect()
                client = mongo.client
                db = client.pyblog
                item = {"account":email,"username":email, "password":sign,"regDate":datetime.datetime.now(),'status':'0','type':type,
                        "lastLoginDate":datetime.datetime.now(),"isActive":False,'isSupper':False}
                db.user.insert(item)

                self.set_secure_cookie("account", email)

                self.redirect('/ucenter/list')




class LoginHandler(BaseHandler):

    def get(self):
        user = self.current_user
        referer = self.get_argument('next','/')
        if user:
            self.redirect(referer)
        else:
            self.render('login.html',referer=referer)


    def post(self):

        email = self.get_argument('email','')
        password = self.get_argument('password','')

        if email == '' or password == '':
            self.render('error.html',msg=u'Email 密码 不能为空!')

        else:
            mongo = MongoCase()
            mongo.connect()
            client = mongo.client
            db = client.pyblog
            user = db.user.find({"account":email})
            if user.count()<1:
                self.render('error.html',msg=u'Email 不存在')
            else:
                m = hashlib.md5()
                m.update(password)
                sign = m.hexdigest()
                if user[0]['password'] != sign:
                    self.render('error.html',msg=u'密码错误')

                else:
                    self.set_secure_cookie("account", email)
                    if user[0]['isSupper']:
                        self.redirect('/admin/')
                    else:
                        self.redirect('/ucenter/list')



class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("account")
        #self.clear_cookie("email")
        self.redirect('/')
