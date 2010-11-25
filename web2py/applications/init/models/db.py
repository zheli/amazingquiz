# -*- coding: utf-8 -*- 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################


if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db = db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
migrate = True
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

mail.settings.server = 'logging' or 'smtp.gmail.com:587'  # your SMTP server
mail.settings.sender = 'you@gmail.com'         # your email
mail.settings.login = 'username:password'      # your credentials or None

auth.settings.hmac_key = 'sha512:12660f29-c206-409f-8215-ed11cc55ccf2'   # before define_tables()
# define the auth_table before call to auth.define_tables()
auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'

crud.settings.auth = None                      # =auth to enforce authorization on crud
auth.settings.login_next=URL(c='admin', f='index')

import sys, os
path = os.path.join(request.folder, 'modules')
if not path in sys.path:
    sys.path.append(path)

from fbappauth import *

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('characters',
        Field('name', 'string'),
        Field('pic', 'string'),
        Field('answer', 'string'),
        Field('description', 'text'))
db.define_table('fb_users',
        Field('fb_uid', 'string', length=30),
        Field('fb_token', 'string'),
        Field('character_id', db.characters))
#        Field('character_id', 'string'))

db.fb_users.fb_uid.requires = IS_NOT_EMPTY()
#db.fb_users.character_id.requires = IS_IN_DB(db, db.characters.id, '%(name)s')
db.fb_users.character_id.writable = db.fb_users.character_id.readable = False
db.fb_users.fb_token.requires = IS_NOT_EMPTY()
db.fb_users.fb_token.writable = db.fb_users.fb_token.readable = False
