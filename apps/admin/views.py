#coding:utf-8


from base import BaseHandler

import hashlib
import datetime
import os.path
import uuid
import tornado.web
from databaseCase import *
from bson import ObjectId


#管理后台主页
class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find({"account":user})
        if user and userInfo.count():
            if userInfo[0]['isSupper']:
                userList = db.user.find({"isSupper":False})

                self.render('admin.html',userList=userList,userInfo=userInfo[0])
            else:
                self.redirect('/')
        else:
            self.clear_cookie('account')
            self.render('error.html',msg=u'非法用户！')

#审核用户
class AuditUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = user=self.current_user
        action = self.get_argument('action','')
        id = self.get_argument('id','')
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find({'account':user})
        if action != '' and id != ''and userInfo.count>0:
            if userInfo[0]['isSupper']:
                if action == 'delete':
                    db.user.remove({'_id':ObjectId(id)})
                    db.profile.remove({'_id':ObjectId(id)})
                elif action == 'deActive':
                    db.user.update({'_id':ObjectId(id)},{'$set':{'isActive':False,'status':1}})

                elif action == 'active':
                    db.user.update({'_id':ObjectId(id)},{'$set':{'isActive':True}})
                elif action == 'audit':
                    db.user.update({'_id':ObjectId(id)},{'$set':{'isActive':True,'status':2}})
                self.redirect('/admin/')
            else:
                self.render('error.html',msg=u'无权限删除！')
        else:
            self.render('error.html',msg=u'非法操作！')

#链接管理
class AdminLinksHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find({"account":user})
        if user and userInfo.count():
            if userInfo[0]['isSupper']:
                linkList = db.links.find()

                self.render('admin-link.html',linkList=linkList,userInfo=userInfo[0])
            else:
                self.redirect('/')
        else:
            self.clear_cookie('account')
            self.render('error.html',msg=u'非法用户！')

#审核链接
class AuditLinksHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = user=self.current_user
        action = self.get_argument('action','')
        id = self.get_argument('id','')
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find({'account':user})
        if action != '' and id != ''and userInfo.count>0:
            if userInfo[0]['isSupper']:
                if action == 'delete':
                    db.links.remove({'_id':ObjectId(id)})
                elif action == 'deActive':
                    db.links.update({'_id':ObjectId(id)},{'$set':{'isCheck':0,'showType':0}})

                elif action == 'active':
                    db.links.update({'_id':ObjectId(id)},{'$set':{'isCheck':1,'showType':1}})
                elif action == 'audit':
                    db.user.update({'_id':ObjectId(id)},{'$set':{'showType':1}})
                self.redirect('/admin/links')
            else:
                self.render('error.html',msg=u'无权限删除！')
        else:
            self.render('error.html',msg=u'非法操作！')

#广告管理
class AdminAdsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find({"account":user})
        if user and userInfo.count():
            if userInfo[0]['isSupper']:
                AdsList = db.ads.find()

                self.render('admin-ads.html',AdsList=AdsList,userInfo=userInfo[0])
            else:
                self.redirect('/')
        else:
            self.clear_cookie('account')
            self.render('error.html',msg=u'非法用户！')

#文件上传（CKEditor使用）
class UploadHandler(BaseHandler):
    def post(self):
        imgfile = self.request.files.get('upload')
        callback = self.get_argument('CKEditorFuncNum')
        imgPath = []
        imgRoot = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))+'/static/uploads/'
        for img in imgfile:
            file_suffix = img['filename'].split(".")[-1]
            file_name=str(uuid.uuid1())+"."+file_suffix
            with open(imgRoot + file_name, 'wb') as f:
                f.write(img['body'])

            imgPath.append(file_name)

        self.write('<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction('+callback+',"/static/uploads/'+imgPath[0]+'","")</script>')
