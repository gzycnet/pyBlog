#coding:utf-8


from base import BaseHandler

import hashlib
import datetime
import os.path
import uuid
import tornado.web
from databaseCase import *
from bson import ObjectId


class BlogHandler(BaseHandler):
    def get(self):



        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog


        articles = db.post.find().sort("date",-1).limit(20)



        tags = db.tags.find().sort('count',-1).limit(50)
        links = db.links.find({'showType':1}).limit(20)
        cateList = db.category.find()

        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)


        archives = db.post.aggregate([{'$group': {'_id': "$archive", 'count': {'$sum': 1}}}])
        result = []
        result2 = []
        for itme in archives:
            if itme['_id']:
                result.append({'date':datetime.datetime.strptime(itme['_id'],'%Y-%m'),'count':itme['count']})
            else:
                result2.append({'date':None,'count':itme['count']})

        result.sort(lambda x,y: cmp(x['date'], y['date']))
        result.reverse()
        result.extend(result2)


        self.render('blog/index.html',articles=articles,tags=tags,cateData=cateData,pageInfo=None,archives=result,links=links)

        #self.render('index.html')

    def write_error(self, status_code, **kwargs):
        self.write("Gosh darnit, user! You caused a %d error.\n" % status_code)



class BlogCategoryHandler(BaseHandler):
    def get(self,id):

        pageSize = 20

        try:
            page = int(self.get_argument('page',1))
        except:
            page = 1

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        posts = db.post

        option = {}

        if id !='':
            option = {"cate.id":ObjectId(id)}

        totalCount = posts.find(option).count()

        articles = posts.find(option).sort("date",-1).limit(pageSize).skip((page-1)*pageSize)

        pageInfo = dict()
        p = divmod(totalCount,pageSize)

        totalPage = p[0]
        if p[1]>0:
            totalPage += 1

        pageInfo['totalPage'] = totalPage
        pageInfo['totalCount'] = totalCount
        pageInfo['pageSize'] = pageSize
        pageInfo['pageNo'] = page
        pageInfo['pageList'] = range(1,totalPage+1)



        tags = db.tags.find().sort('count',-1).limit(50)
        links = db.links.find({'showType':1}).limit(20)
        cateList = db.category.find()

        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)


        archives = db.post.aggregate([{'$group': {'_id': "$archive", 'count': {'$sum': 1}}}])
        result = []
        result2 = []
        for itme in archives:
            if itme['_id']:
                result.append({'date':datetime.datetime.strptime(itme['_id'],'%Y-%m'),'count':itme['count']})
            else:
                result2.append({'date':None,'count':itme['count']})

        result.sort(lambda x,y: cmp(x['date'], y['date']))
        result.reverse()
        result.extend(result2)


        self.render('blog/index.html',articles=articles,pageInfo=pageInfo,tags=tags,cateData=cateData,archives=result,links=links)



class BlogTagsHandler(BaseHandler):
    def get(self,t):

        pageSize = 20

        try:
            page = int(self.get_argument('page',1))
        except:
            page = 1

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        posts = db.post

        option = {}


        if t !='':
            option = {"tags":t}

        totalCount = posts.find(option).count()

        articles = posts.find(option).sort("date",-1).limit(pageSize).skip((page-1)*pageSize)

        pageInfo = dict()
        p = divmod(totalCount,pageSize)

        totalPage = p[0]
        if p[1]>0:
            totalPage += 1

        pageInfo['totalPage'] = totalPage
        pageInfo['totalCount'] = totalCount
        pageInfo['pageSize'] = pageSize
        pageInfo['pageNo'] = page
        pageInfo['pageList'] = range(1,totalPage+1)



        tags = db.tags.find().sort('count',-1).limit(50)
        links = db.links.find({'showType':1}).limit(20)
        cateList = db.category.find()

        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)

        archives = db.post.aggregate([{'$group': {'_id': "$archive", 'count': {'$sum': 1}}}])

        result = []
        result2 = []
        for itme in archives:
            if itme['_id']:
                result.append({'date':datetime.datetime.strptime(itme['_id'],'%Y-%m'),'count':itme['count']})
            else:
                result2.append({'date':None,'count':itme['count']})

        result.sort(lambda x,y: cmp(x['date'], y['date']))
        result.reverse()
        result.extend(result2)

        self.render('blog/index.html',articles=articles,pageInfo=pageInfo,tags=tags,cateData=cateData,archives=result,links=links)



class BlogArchiveHandler(BaseHandler):
    def get(self,d):

        pageSize = 20

        try:
            page = int(self.get_argument('page',1))
        except:
            page = 1

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        posts = db.post

        option = {}

        if d !='':
            option = {"archive":d}

        totalCount = posts.find(option).count()

        articles = posts.find(option).sort("date",-1).limit(pageSize).skip((page-1)*pageSize)

        pageInfo = dict()
        p = divmod(totalCount,pageSize)

        totalPage = p[0]
        if p[1]>0:
            totalPage += 1

        pageInfo['totalPage'] = totalPage
        pageInfo['totalCount'] = totalCount
        pageInfo['pageSize'] = pageSize
        pageInfo['pageNo'] = page
        pageInfo['pageList'] = range(1,totalPage+1)



        tags = db.tags.find().sort('count',-1).limit(50)
        links = db.links.find({'showType':1}).limit(20)
        cateList = db.category.find()

        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)

        archives = db.post.aggregate([{'$group': {'_id': "$archive", 'count': {'$sum': 1}}}])
        result = []
        result2 = []
        for itme in archives:
            if itme['_id']:
                result.append({'date':datetime.datetime.strptime(itme['_id'],'%Y-%m'),'count':itme['count']})
            else:
                result2.append({'date':None,'count':itme['count']})

        result.sort(lambda x,y: cmp(x['date'], y['date']))
        result.reverse()
        result.extend(result2)

        self.render('blog/index.html',articles=articles,pageInfo=pageInfo,tags=tags,archives=result,cateData=cateData,links=links)

class ArticleDetailHandler(BaseHandler):
    def get(self,id):
        mongo = MongoCase()
        mongo.connect()
        client = mongo.client

        db = client.pyblog
        article = db.post.find_one({'_id':ObjectId(id)})

        count = 0
        if article.has_key('views'):
            count += article['views']

        db.post.update({'_id':ObjectId(id)},{'$set':{'views':count+1}})

        tags = db.tags.find().sort('count',-1).limit(50)
        cateList = db.category.find()


        ads0 = db.ads.find_one({'position':'0'})

        adsData = dict()
        adsData['ads0'] = ads0


        cateData = dict()
        cateData['menu'] = []
        cateData['side'] = []
        for c in cateList:
            if c['showMenu']:
               cateData['menu'].append(c)
            if c['showSide']:
                cateData['side'].append(c)


        archives = db.post.aggregate([{'$group': {'_id': "$archive", 'count': {'$sum': 1}}}])


        result = []
        result2 = []
        for itme in archives:
            if itme['_id']:
                result.append({'date':datetime.datetime.strptime(itme['_id'],'%Y-%m'),'count':itme['count']})
            else:
                result2.append({'date':None,'count':itme['count']})

        result.sort(lambda x,y: cmp(x['date'], y['date']))
        result.reverse()
        result.extend(result2)


        #archives.sort(key=lambda x:x["_id"])

        self.render('blog/article.html',article=article,tags=tags,cateData=cateData,archives=result,adsData=adsData)

class CommentHandler(BaseHandler):

    def post(self):
        id = self.get_argument('article','')
        username = self.get_argument('username','')
        email = self.get_argument('email','')
        homepage = self.get_argument('homepage','')
        content = self.get_argument('content','')
        if username == '' or content == '':
            self.render('error.html',msg=u'姓名和内容必填')

        else:

            mongo = MongoCase()
            mongo.connect()
            client = mongo.client
            db = client.pyblog

            article = db.post.find_one({'_id':ObjectId(id)})

            if article.has_key('commentList') and article['commentList']:
                commentList = article['commentList']
            else:
                commentList = []

            commentList.append({"email":email,"username":username, "homepage":homepage,"date":datetime.datetime.now(),
                    'content':content,'parentId':None,'isAudit':False})
            commentList.reverse()

            db.post.update({"_id":ObjectId(id)},{'$set':{'status':1,'commentList':commentList}})

            self.redirect('/a/'+id+'/')


class AddLinkHandler(BaseHandler):

    def get(self):
        user = self.current_user
        self.render('blog/link-add.html')


    def post(self):

        sitename = self.get_argument('sitename','')
        email = self.get_argument('email','')
        homepage = self.get_argument('homepage','')
        content = self.get_argument('content','')

        if sitename == '' or homepage == '':
            self.render('error.html',msg=u'网站名称和链接不能为空')

        else:
            mongo = MongoCase()
            mongo.connect()
            client = mongo.client
            db = client.pyblog
            try:
                db.links.insert({'sitename':sitename,'homepage':homepage,'email':email,'content':content,'addtime':datetime.datetime.now(),'isCheck':0,'showType':0})

                self.render('error.html',msg=u'链接提交成功，等待审核中。。')
            except:
                self.render('error.html',msg=u'提交失败！')



class AddAdsHandler(BaseHandler):

    def get(self):
        user = self.current_user
        self.render('blog/ads-add.html')


    def post(self):

        adname = self.get_argument('adname','')
        email = self.get_argument('email','')
        link = self.get_argument('link','')
        img = self.get_argument('img','')
        position = self.get_argument('position','0')
        content = self.get_argument('content','')

        if adname == '' or email == '' or link == '' or content == '':
            self.render('error.html',msg=u'广告名称和链接不能为空')

        else:
            mongo = MongoCase()
            mongo.connect()
            client = mongo.client
            db = client.pyblog
            try:
                db.ads.insert({'adname':adname,'link':link,'email':email,'content':content,'img':img,'position':position,'addtime':datetime.datetime.now(),'isCheck':0,'showType':0,'weight':99})

                self.render('error.html',msg=u'广告提交成功，等待审核中。。')
            except:
                self.render('error.html',msg=u'提交失败！')