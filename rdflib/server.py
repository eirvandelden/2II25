# -*- coding: utf-8 -*-
import cherrypy
#from rdflib import Namespace, BNode, Literal, RDF, URIRef
from mako.template import Template
from mako.lookup import TemplateLookup
# CherryPy needs an absolute path when dealing with static data
import os.path
#_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
_curdir = os.path.dirname(os.path.abspath(__file__))
# Our template lookup directory
lookup = TemplateLookup(directories=['templates'])
import database
db = database.database()

# GLOBAL
SITENAME = "edocol"
SUBTITLE = "<strong>E</strong>ducation <strong>Do</strong>cumentation <strong>Col</strong>laboration</div>"
VERSION = "0.05"
AUTHORS = ["Anson van Rooij", "Edin Dudojevic", "Etienne van Delden"]
BASEURL = "http://127.0.0.1:8080" # base url. without ending slash! for example: http://127.0.0.1:8080
      
      
#print db.get_all_user_info(str(7))
#db.get_all_user_info(str(0))
#db.get_user_property_value(str(0),'name')[0]
#print db.new_document(0,'Web Technology')

#print '---------------'
#print db.get_user_property_value('0','name')
#print db.get_user_property_value('0','email1')
#print db.get_user_property_value('0','password')
#print db.get_userid_from_email('anson@aol.co.uk')
#print db.get_user_property_value('1','follows')
#print db.get_last_x_dox(10)
#print db.get_document('0')

#pages = db.get_last_x_dox(10)


def stringToURL(string=""):
    before = "‡¿‚¬‰ƒ·¡È…Ë»Í ÎÀÏÃÓŒÔœÚ“Ù‘ˆ÷˘Ÿ˚€¸‹Á«íÒ"
    after  = "aAaAaAaAeEeEeEeEiIiIiIoOoOoOuUuUuUcC'n"
    i = 0
    blength = len(before)
    slength = len(string)
    # loop through the given string, checking for each character whether to replace it
    while 1<=slength and i<=slength:
        j = 0
        # check character
        while string[i]<>before[j] and j<=blength:
            j += 1
        # replace character
        if j<=blength:
            string[i] = after[j]
            
    return string

def readCookie():    
    return cherrypy.request.cookie

def checkUsername(username):
    ok = True
    if (len(username)<3):
        ok = False
    return ok
    
def checkPassword(password):
    ok = True
    if (len(password)<8):
        ok = False
    return ok
         
def loggedin():
    try:
        cookie = readCookie()

        id = cookie['id'].value
        email = cookie['email'].value
        password = cookie['pass'].value
        
        u = user(id)
        
        if u.email == email and u.password == password:
            return True
        else:
            return False
    except:
        return False
        
def isowner(id):
    cookie = readCookie()
    oid = cookie['id'].value
    return int(oid)==int(id)
    
# ------ data objects ----------
class page(object):
    def __init__(self, id):
        self.id = str(id)
        try:
            self.ownername = db.get_user_property_value(str(0), 'name')[0][2]
            
            pageinfo = db.get_document(str(id))

            self.ownerid = ''
            self.name = ''
            self.content = ''
            for x in pageinfo:
                #print x
                if x[0] == 'owner':
                    self.ownerid = x[1]
                elif x[0] == 'name':
                    self.name = x[1]
                elif x[0] == 'content':
                    self.content = x[1]
            self.ownername = db.get_user_property_value(self.ownerid,'name')[0][2]
                    
            if self.ownerid == '' or self.name == '':
                self.exists = False
            else:
                self.exists = True
        except:
            print "except ingegaan"
            self.ownername = ''
            self.ownerid = ''
            self.name = ''
            self.content = ''
            self.exists = False
                
class user(object):
    def __init__(self, id):
        self.id = str(id)
        try:
            #print db.get_user_property_value(str(id),'email')
            self.name = db.get_user_property_value(str(id),'name')[0][2]
            #print self.name
            #print db.get_user_property_value(str(id),'email3')[0]
            self.email = db.get_user_property_value(str(id),'email1')[0][2]+'@'+db.get_user_property_value(str(id),'email2')[0][2]+'.'+db.get_user_property_value(str(id),'email3')[0][2]
            #self.email = db.get_user_property_value(str(id),'email')[0][2]
            #print self.mail
            #print self.mail
            #db.get_user_property_value
            #self.email = ''
            self.exists = True
            self.pages = db.get_documents_from_user(str(id))
            self.password = db.get_user_property_value(str(id),'password')[0][2]
            
            fs = db.get_user_property_value(str(id),'follows')
            follows = []
            for f in fs:
                follows.append(f[2])
            self.follows = follows
                
            #print self.password
            #print self.pages
            #print 'user object created'
        except:
            #print 'user object NOT created'
            self.name = 'Non-existant'
            self.email = ''
            self.password = ''
            self.exists = False
    def name(self,name):
        try:
            # maybe some check on username
            db.set_user_property_value(self.id,'name',str(name))
            self.name = str(name)
            return 1
        except:
            return 0
    def password(self,passw):
        try:
            db.set_user_property_value(self.id,'password',str(passw))
            return 1
        except:
            return 0
    def email(self,passw):
        try:
            db.set_user_property_value(self.id,'email',str(passw))
            return 1
        except:
            return 0
            
class mainpage(object):
    nrld = 10 # Number of last documents to display
    def __init__(self):
        try:
            self.lastpages = db.get_last_x_dox_general(10)
        except:
            self.lastpages = []

# ------ end data objcts -------      
# ------------------------------
            
class Main(object):
    @cherrypy.expose
    def index(self):
        # header
        hdr = lookup.get_template('header.html')
        HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
        # sidebar1
        sb1 = lookup.get_template('sidebar1.html')
        SIDEBAR1 = sb1.render()
        # sidebar2
        sb2 = lookup.get_template('sidebar2.html')
        SIDEBAR2 = sb2.render()
        # footer
        f = lookup.get_template('footer.html')
        FOOTER = f.render()
        
        #..<head>..</head>
        h = lookup.get_template('head.html')
        HEAD = h.render(baseURL=BASEURL, pagename='Welcome to '+SITENAME+'!')
        # body
        b = lookup.get_template('main.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        sitename=SITENAME, version=VERSION, authors=AUTHORS,
                        main = mainpage())
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
            
class User(object):
    @cherrypy.expose
    def index(self):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='search/users/',baseURL=BASEURL)
        
    @cherrypy.expose
    def default(self,id,*args):
        u = user(id)
        #print u.__dict__
        #print dir(u)
        #print help(u)
        # header

        #print u.email
        #print db.get_all_user_info('0')
        
        hdr = lookup.get_template('header.html')
        HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
        # sidebar1
        sb1 = lookup.get_template('sidebar1.html')
        SIDEBAR1 = sb1.render()
        # sidebar2
        sb2 = lookup.get_template('sidebar2.html')
        SIDEBAR2 = sb2.render()
        # footer
        f = lookup.get_template('footer.html')
        FOOTER = f.render()
        
        #..<head>..</head>
        h = lookup.get_template('head.html')
        if u.exists:
            HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - User '+u.name)
        else:
            HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - Non-existant user')
        # body
        b = lookup.get_template('user.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        user=u)
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def edit(self,id,*args):
        try:
            u = user(id)
            if loggedin and isowner(u.id):
                # header
                hdr = lookup.get_template('header.html')
                HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
                # sidebar1
                sb1 = lookup.get_template('sidebar1.html')
                SIDEBAR1 = sb1.render()
                # sidebar2
                sb2 = lookup.get_template('sidebar2.html')
                SIDEBAR2 = sb2.render()
                # footer
                f = lookup.get_template('footer.html')
                FOOTER = f.render()
                
                #..<head>..</head>
                h = lookup.get_template('head.html')
                HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - User '+str(u.name))
                # body
                b = lookup.get_template('useredit.html')
                BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                                user=u)
                # </html>
                FOOT = '</html>'
                
                PAGE = HEAD + BODY + FOOT

                return PAGE
            else:
                r = lookup.get_template('redirect.html')
                return r.render(time=0,url='/user/'+str(id),baseURL=BASEURL)            
        except:
            print "edit except"
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/user/'+str(id),baseURL=BASEURL) 
    @cherrypy.expose
    def doEdit(self,id,username,email,password,*args):
        try:
            u = user(id)
            if loggedin and isowner(u.id):
                db.set_user_property_value(str(id), "name", str(username))
                db.set_user_property_value(str(id), "email", str(email))
                db.set_user_property_value(str(id), "password", str(password))
                
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/user/'+str(id)+'/',baseURL=BASEURL)
        except:
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/user/'+str(id)+'/',baseURL=BASEURL)

class Page(object):
    @cherrypy.expose
    def index(self):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/search/pages/',baseURL=BASEURL)
    @cherrypy.expose
    def default(self,id=0,name='testpage',*args):
        # create a page instance
        p = page(id)
        #print p
        # header
        hdr = lookup.get_template('header.html')
        HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
        # sidebar1
        sb1 = lookup.get_template('sidebar1.html')
        SIDEBAR1 = sb1.render()
        # sidebar2
        sb2 = lookup.get_template('sidebar2.html')
        SIDEBAR2 = sb2.render()
        # footer
        f = lookup.get_template('footer.html')
        FOOTER = f.render()
        
        #..<head>..</head>
        h = lookup.get_template('head.html')
        if p.exists:
            HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - '+str(p.name))
        else:
            HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - Non-existant page')
        # body
        b = lookup.get_template('page.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        page=p)
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def edit(self, id,*args):
        try:
            p = page(id)
            if loggedin and isowner(p.ownerid):
                # header
                hdr = lookup.get_template('header.html')
                HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
                # sidebar1
                sb1 = lookup.get_template('sidebar1.html')
                SIDEBAR1 = sb1.render()
                # sidebar2
                sb2 = lookup.get_template('sidebar2.html')
                SIDEBAR2 = sb2.render()
                # footer
                f = lookup.get_template('footer.html')
                FOOTER = f.render()
                
                #..<head>..</head>
                h = lookup.get_template('head.html')
                HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - Edit page: '+str(p.name))
                # body
                b = lookup.get_template('pageedit.html')
                BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                                page=p)
                # </html>
                FOOT = '</html>'
                
                PAGE = HEAD + BODY + FOOT

                return PAGE
            else:
                r = lookup.get_template('redirect.html')
                return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)            
        except:
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)            
            
    @cherrypy.expose
    def new(self,*args):
        # te fixen: messy template - form etc.
              
        # header
        hdr = lookup.get_template('header.html')
        HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
        # sidebar1
        sb1 = lookup.get_template('sidebar1.html')
        SIDEBAR1 = sb1.render()
        # sidebar2
        sb2 = lookup.get_template('sidebar2.html')
        SIDEBAR2 = sb2.render()
        # footer
        f = lookup.get_template('footer.html')
        FOOTER = f.render()
        
        #..<head>..</head>
        h = lookup.get_template('head.html')
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - New Page')
        # body
        b = lookup.get_template('pagenew.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        loggedin=loggedin())
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def save(self,id,name,content,*args):
        # cookie + checks
        # ...
        try:
            db.edit_document(str(id),str(name),str(content))
        
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)
        except:
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)

    @cherrypy.expose
    def newsave(self,title,content,tags,*args):
    
        # cookie read
        # ...
        cookie = readCookie()
        ownerid = cookie['id'].value
        ownername = db.get_user_property_value(str(ownerid),'name')[0][2]
        # Some checks
        # ...
        
       
        did = db.new_document(str(ownerid), str(title), str(content))
        #print db.get_document(did)
        
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/page/'+str(did),baseURL=BASEURL)
        
    @cherrypy.expose
    def delete(self,id,*args):
        # cookie + checks
        # ...
        try:
            db.delete_document(str(id))
        
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)
        except:
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/page/'+str(id),baseURL=BASEURL)
        
class Tag(object):
    @cherrypy.expose
    def index(self):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/search/tags/',baseURL=BASEURL)
    @cherrypy.expose
    def default(self,id,content,*args):
        return "Tag ID is %s" %id

class Comments(object):
    @cherrypy.expose
    def index(self):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/search/comments/',baseURL=BASEURL)
    @cherrypy.expose
    def default(self,id,*args):
        return "Comments ID is %s" % id
            
class RSS(object):
    @cherrypy.expose
    def index(self):
        return "Create your own RSS feed."
    @cherrypy.expose
    def default(self,id,*args):
        return "RSS ID is %s" %id
        
class Search(object):
    @cherrypy.expose
    def index(self):
        return """<h1>What do you want to search for?</h1>
        Search for
        <ul>
            <li><a href="users/">users</a>
            <li><a href="pages/">pages</a>
            <li><a href="comments/">comments</a>
            <li><a href="tags/">tags</a>
        </ul>
        """
    @cherrypy.expose
    def default(self,s,*args):
        if s == "users":
            return "Search for users."
        elif s == "pages":
            return "Search for pages."
        elif s == "comments":
            return "Search through comments."
        elif s == "tags":
            return "Search for tags."
        else:
            return "Search not specified."

class Login(object):
    @cherrypy.expose
    def index(self):
        return ""
    @cherrypy.expose
    def doLogin(self, email, password, *args):
        try:
            id = db.get_userid_from_email(str(email))[0]
            u = user(id)
            if u.password == str(password):
                cookie = cherrypy.response.cookie
                
                cookie['id'] = id
                cookie['id']['path'] = '/'
                cookie['id']['max-age'] = 3600
                
                cookie['email'] = email
                cookie['email']['path'] = '/'
                cookie['email']['max-age'] = 3600
                  
                cookie['pass'] = str(password)
                cookie['pass']['path'] = '/'
                cookie['pass']['max-age'] = 3600
                
                r = lookup.get_template('redirect.html')
                return r.render(time=0,url='/',baseURL=BASEURL)
                #return "login successful"
            else:
                r = lookup.get_template('redirect.html')
                return r.render(time=0,url='/',baseURL=BASEURL)
                #return "login failed"
        except:
            return "an error occured"
            
    @cherrypy.expose
    def doLogout(self,*args):
        cookie = cherrypy.request.cookie
        rcookie = cherrypy.response.cookie
        for name in cookie.keys():
            rcookie[name] = name
            rcookie[name]['path'] = '/'
            rcookie[name]['max-age'] = 0
            #rcookie[name]['expires'] = 0
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/',baseURL=BASEURL)
        
class Register(object):
    @cherrypy.expose
    def index(self):
        # header
        hdr = lookup.get_template('header.html')
        HEADER = hdr.render(sitename=SITENAME, subtitle=SUBTITLE, version=VERSION)
        # sidebar1
        sb1 = lookup.get_template('sidebar1.html')
        SIDEBAR1 = sb1.render()
        # sidebar2
        sb2 = lookup.get_template('sidebar2.html')
        SIDEBAR2 = sb2.render()
        # footer
        f = lookup.get_template('footer.html')
        FOOTER = f.render()
        
        #..<head>..</head>
        h = lookup.get_template('head.html')
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - User registration')
        # body
        b = lookup.get_template('register.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        )
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
        
    @cherrypy.expose
    def default(self, *args):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/register/',baseURL=BASEURL)
    
    @cherrypy.expose
    def doRegister(self, username, password, email, *args):
        try:
            r = lookup.get_template('redirect.html')
            #print username
            #print password
            #print email
            if checkUsername(username) and checkPassword(password):
                #print username
                #print password
                #print email
                userid = db.new_user(str(username), str(password), str(email))
                print "user CREATED"
                #id = database.db.new_user('username','password', 'someemail@edocol.com')
                #return 'registration was succesful! Added ID: '+str(userid)
                return r.render(time=0,url='/user/'+str(userid),baseURL=BASEURL)
            else:
                print "user NOT created"
                return r.render(time=0,url='/register/',baseURL=BASEURL)
                #return 'registration failed!'
            
        except:
            return 'error: registration failed!'
            r = lookup.get_template('redirect.html')
            #return r.render(time=0,url='/login/',baseURL=BASEURL)            

class Follow(object):
    @cherrypy.expose
    def index(self):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/',baseURL=BASEURL)
    @cherrypy.expose
    def default(self, *args):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/',baseURL=BASEURL)
    
    @cherrypy.expose
    def doFollow(self, id, *args):
        r = lookup.get_template('redirect.html')
        try:
            cookie = readCookie()
            lid = cookie['id'].value
            if loggedin and int(id) <> int(lid):
                db.follow_user(str(lid), str(id))
                return r.render(time=0,url='/user/'+str(id),baseURL=BASEURL)
            else:
                return r.render(time=0,url='/'+str(id),baseURL=BASEURL)
        except:
            return 'an error occured!'
            r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/',baseURL=BASEURL)
        
    @cherrypy.expose
    def doUnfollow(self, id, *args):
        r = lookup.get_template('redirect.html')
        cookie = readCookie()
        lid = cookie['id'].value
        try:           
            if loggedin and int(id) <> int(lid):
                db.delete_specific_user_property_value(str(lid),'follows',str(id))                
                return r.render(time=0,url='/user/'+str(id),baseURL=BASEURL)
            else:
                return r.render(time=0,url='/',baseURL=BASEURL)
        except:
            return 'an error occured!'
            r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/',baseURL=BASEURL)
            
if __name__ == '__main__':
    # Define the global configuration settings of CherryPy
    global_conf = {
        'global': { 'environment': 'production',
                    'engine.autoreload.on': True,
                    'engine.autoreload_frequency': 1,
                    'server.socket_host': '127.0.0.1',
                    'server.socket_port': 8080,
                    'request.show_tracebacks': True,
                  }}
    application_conf = {
        '/style.css': {
            'tools.staticfile.on': True,
            'tools.staticfile.filename': os.path.join(_curdir, 'templates/style.css')
        },
        '/images': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(_curdir, 'images')}
    }
    # Update the global CherryPy configuration
    cherrypy.config.update(global_conf)
    # Create an instance of the application
    root = Main()
    root.user = User()
    root.page = Page()
    root.tag = Tag()
    root.comments = Comments()
    root.rss = RSS()
    root.search = Search()
    root.login = Login()
    root.register = Register()
    root.follow = Follow()
    # mount the application on the '/' base path
    #cherrypy.tree.mount(root, '/', config = application_conf)
    cherrypy.quickstart(root, '/', config=application_conf)
    # Start the CherryPy HTTP server
    #cherrypy.quickstart(root)
    # Start the CherryPy engine
    #cherrypy.engine.start()