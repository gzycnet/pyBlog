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


from databaseCase import *

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


from tornado.options import define, options
define("port", default=8800, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("account")

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('error/404.html')
        elif status_code == 500:
            self.render('error/500.html')
        else:
            self.write('error:' + str(status_code))


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



class BlogHandler(BaseHandler):
    def get(self):

        mongo = MongoCase()
        mongo.connect()
        client = mongo.client
        db = client.pyblog
        articles = db.post.find().sort("date",-1).limit(20)


        tags = db.tags.find().limit(50)
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


        self.render('blog/index.html',articles=articles,tags=tags,cateData=cateData,links=links)

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



        tags = db.tags.find().limit(50)
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


        self.render('blog/index.html',articles=articles,pageInfo=pageInfo,tags=tags,cateData=cateData,links=links)



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



        tags = db.tags.find().limit(50)
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

        self.render('blog/index.html',articles=articles,pageInfo=pageInfo,tags=tags,cateData=cateData,links=links)


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

        self.render('blog/article.html',article=article,tags=tags,cateData=cateData)



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

            self.redirect('/a/'+id)



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
                self.redirect('/admin')
            else:
                self.render('error.html',msg=u'无权限删除！')
        else:
            self.render('error.html',msg=u'非法操作！')


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
                        self.redirect('/admin')
                    else:
                        self.redirect('/ucenter/list')



class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("account")
        #self.clear_cookie("email")
        self.redirect('/')


#文件上传（CKEditor使用）
class UploadHandler(BaseHandler):
    def post(self):
        imgfile = self.request.files.get('upload')
        callback = self.get_argument('CKEditorFuncNum')
        imgPath = []
        imgRoot = os.path.dirname(__file__)+'/static/uploads/'
        for img in imgfile:
            file_suffix = img['filename'].split(".")[-1]
            file_name=str(uuid.uuid1())+"."+file_suffix
            with open(imgRoot + file_name, 'wb') as f:
                f.write(img['body'])

            imgPath.append(file_name)

        self.write('<script type="text/javascript">window.parent.CKEDITOR.tools.callFunction('+callback+',"/static/uploads/'+imgPath[0]+'","")</script>')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    settings = {
        "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
        "xsrf_cookies": False,
        'login_url':'/account/login'
    }
    app = tornado.web.Application(
        handlers=[(r"/", IndexHandler),
                  (r'/blog/$', BlogHandler),
                  (r'/t/([%a-fA-F0-9]+|\w+)/$', BlogTagsHandler),
                  (r'/c/(\w+)/$', BlogCategoryHandler),
                  (r'/a/(\w+)', ArticleDetailHandler),
                  (r'/comment/post/$', CommentHandler),
                  (r'/ucenter/post$', PostArticleHandler),
                  (r'/ucenter/edit/(\w+)', EditArticleHandler),
                  (r'/ucenter/list$', AuthorArticleListHandler),
                  (r'/account/reg$', RegHandler),
                  (r'/account/login$', LoginHandler),
                  (r'/account/logout$', LogoutHandler),
                  (r'/admin', AdminHandler),
                  (r'/admin/upload/', UploadHandler),
                  (r'/auditUser/', AuditUserHandler),
                  (r'/admin/links', AdminLinksHandler),
                  (r'/auditLink/', AuditLinksHandler),
                  (r'/site/addlink', AddLinkHandler),
                  (r".*", BaseHandler),
                  ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
        **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()