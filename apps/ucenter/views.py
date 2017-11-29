#coding:utf-8


from base import BaseHandler

import hashlib
import datetime
import os.path
import uuid
import tornado.web
from databaseCase import *
from bson import ObjectId


class PostArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        acc = db.user.find_one({"account":user})
        if acc and int(acc['status'])<2 :

            self.render('error.html',msg=u'您的账号待审核，还不能发布文章！')

        else:
            cateList = db.category.find()
            self.render('post.html',referer = self.request.path,user=self.current_user,userInfo=acc,cateList=cateList)



    def post(self):
        #author = self.get_argument('author')
        author = self.current_user
        title = self.get_argument('title')
        content = self.get_argument('content')
        description = self.get_argument('description')
        tags = self.get_argument('tags')
        tags = tags.split(',')
        cate = self.get_argument('cate','None')

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client

        db = client.pyblog
        posts = db.post
        if cate != 'None':
            t = db.category.find_one(ObjectId(cate))
            new_post = {"author":author,"title":title,'content':content,'description':description,'tags':tags,'date':datetime.datetime.now(),'updateDate':datetime.datetime.now(),'status':0,'cate':{'id':ObjectId(cate),'name':t['name']},'views':0,'likes':0,'unlikes':0}
        else:
            new_post = {"author":author,"title":title,'content':content,'description':description,'tags':tags,'date':datetime.datetime.now(),'updateDate':datetime.datetime.now(),'status':0,'cate':None,'views':0,'likes':0,'unlikes':0}
        posts.insert(new_post)

        for t in tags:
            if t != '':
                try:
                    db.tags.insert({'name':t})
                except:
                    pass

        #self.render('index.html')
        self.redirect('/ucenter/list')



class AuthorArticleListHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        userInfo = db.user.find_one({"account":user})
        if userInfo:

            articles = db.post.find({"author":user})
            statusList = ['未审核','待修改','待审核','拒绝','通过']

            self.render('list.html',articles=articles,referer = self.request.path,statusList=statusList,userInfo=userInfo)

        else:
            self.render('error.html',msg=u'无权限！ >> <a href="/account/login">登录</a>')


class EditArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id):
        user=self.current_user
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        article = db.post.find_one({'_id':ObjectId(id)})

        userInfo = db.user.find_one({"account":user})
        if article['author']!= user:
            msg = u'无权编辑'
            self.render('error.html',msg=msg)
        else:
            cateList = db.category.find()
            self.render('edit.html',article=article,referer = self.request.path,cateList=cateList,userInfo=userInfo)


    @tornado.web.authenticated
    def post(self,*args, **kwargs):
        id = self.get_argument('id')
        title = self.get_argument('title')
        description = self.get_argument('description')
        content = self.get_argument('content')
        tags = self.get_argument('tags','')
        oldTags = self.get_argument('oldTags','')
        mark = 0
        if oldTags != tags:
            mark +=1
        tags = tags.strip(',').split(',')
        cate = self.get_argument('cate')
        dateStr = self.get_argument('date')

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        article = db.post.find_one({'_id':ObjectId(id)})

        newData = dict()

        newData['title'] = title
        newData['content'] = content
        newData['description'] = description
        newData['tags'] = tags
        newData['updateDate'] = datetime.datetime.now()
        newData['status'] = 2

        try:
            if '.' in dateStr:
                d = datetime.datetime.strptime(dateStr,'%Y-%m-%d %H:%M:%S.%f')
            else:
                d = datetime.datetime.strptime(dateStr,'%Y-%m-%d %H:%M:%S')
            newData['date'] = d
        except:
            pass


        if article['cate'] == None and cate !='None':
            t = db.category.find_one(ObjectId(cate))
            newData['cate'] = {'id':ObjectId(cate),'name':t['name']}

        db.post.update({'_id':ObjectId(id)},{'$set':newData})

        if mark >0:
            for t in tags:
                if t != '':
                    try:
                        db.tags.insert({'name':t})
                    except:
                        pass


        self.redirect('/ucenter/list')
