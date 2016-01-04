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
import database as db

# GLOBAL
SITENAME = "edocol"
SUBTITLE = "<strong>E</strong>ducation <strong>Do</strong>cumentation <strong>Col</strong>laboration</div>"
VERSION = "0.03"
AUTHORS = ["Anson van Rooij", "Edin Dudojevic", "Etienne van Delden"]
BASEURL = "http://127.0.0.1:8080" # base url. without ending slash! for example: http://127.0.0.1:8080
        
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
    if (len(password)>=8):
        ok = False
    return ok
    
        
def loggedin():
    try:
        cookie = readCookie()
        #id = cookie['id'].value
        username = cookie['user'].value
        password = cookie['pass'].value
        #n = fte.get_user_property_value(int(id),'name')[0]
        #p = fte.get_user_property_value(int(id),'password')[0]
        if username=='user' and password=='pass':
            return True
        else:
            return False
    except:
        return False
    
def isowner():
    return True
    
# data objects -----------------
class page(object):
    def __init__(self, id):
        self.id = str(id)
        self.ownerid = '0'
        self.ownername = 'edocol'
        self.name = 'Some pagename'
        self.content = '..............content............'
        self.exists = False
                
class user(object):
    def __init__(self, id):
        self.id = str(id)
        try:
            self.name = db.getpropertyvalue(int(id),'name')[0]
            #self.email = fte.get_user_property_value(int(id),'email')[0]
            self.exists = True
            print 'user object created'
        except:
            print 'user object NOT created'
            self.name = 'Non-existant'
            self.email = ''
            self.exists = False
    def name(self,name):
        try:
            # maybe some check on username
            db.setpropertyvalue(self.id,'name',str(name))
            self.name = str(name)
            return 1
        except:
            return 0
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
                        sitename=SITENAME, version=VERSION, authors=AUTHORS)
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
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - User '+u.name)
        # body
        b = lookup.get_template('user.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        user=u, loggedin=loggedin())
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def edit(self,id,*args):
        PAGES=[["0","Webtechnology","content.."],["1","Samenvatting Webtechnology","Hoofdstuk 1 - RDF .."]]
        name = fte.get_user_property_value(int(id),"name")
        if name==[]:
            name = ["edocol"]
         
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
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - User '+name[0])
        # body
        b = lookup.get_template('useredit.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        userid=id, username=name[0], nrpages=len(PAGES), userpages=PAGES)
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def doEdit(self,id,username,*args):
        fte.set_user_property_value(int(id), "name", str(username))
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
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - '+p.name)
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
        pagequery = ["0","Webtechnology","content.."]
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
        HEAD = h.render(baseURL=BASEURL, pagename=SITENAME+' - Edit page: '+pagequery[1])
        # body
        b = lookup.get_template('pageedit.html')
        BODY = b.render(header=HEADER, sidebar1=SIDEBAR1, sidebar2=SIDEBAR2, footer=FOOTER, # Base elements
                        pageid='0', pagename=pagequery[1], pagecontent=pagequery[2], ownerid=0, pageowner='edocol')
        # </html>
        FOOT = '</html>'
        
        PAGE = HEAD + BODY + FOOT

        return PAGE
    @cherrypy.expose
    def new(self,*args):
    
              
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
    def save(self,id,content,*args):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/page/'+id,baseURL=BASEURL)

    @cherrypy.expose
    def newsave(self,title,content,*args):
        r = lookup.get_template('redirect.html')
        return r.render(time=0,url='/page/'+id,baseURL=BASEURL)
        
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
    def doLogin(self, username, password,*args):
        if username=="user" and password=="pass":
            cookie = cherrypy.response.cookie
            
            cookie['user'] = username
            cookie['user']['path'] = '/'
            cookie['user']['max-age'] = 3600
              
            cookie['pass'] = password
            cookie['pass']['path'] = '/'
            cookie['pass']['max-age'] = 3600
            
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/',baseURL=BASEURL)
        else:
            r = lookup.get_template('redirect.html')
            return r.render(time=0,url='/',baseURL=BASEURL)
            
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
    def doRegister(self, username, password,*args):
        try:
            if checkUsername(username) and checkPassword(password):
                id = usermethods.new(str(username),str(password), 'someemail@edocol.com')
                return 'registration was succesful! Added ID: '+str(id)
            else:
                return 'registration failed!'
              
            #r = lookup.get_template('redirect.html')
            #return r.render(time=0,url='/login/',baseURL=BASEURL)
        except:
            return 'error: registration failed!'
            r = lookup.get_template('redirect.html')
            #return r.render(time=0,url='/login/',baseURL=BASEURL)            
            
if __name__ == '__main__':
    # Define the global configuration settings of CherryPy
    global_conf = {
        'global': { #'environment': 'production',
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
    # mount the application on the '/' base path
    #cherrypy.tree.mount(root, '/', config = application_conf)
    cherrypy.quickstart(root, '/', config=application_conf)
    # Start the CherryPy HTTP server
    #cherrypy.quickstart(root)
    # Start the CherryPy engine
    #cherrypy.engine.start()