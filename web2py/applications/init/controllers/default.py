# -*- coding: utf-8
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

# TODO: finish getFacebookAuth()

from facebook import GraphAPI, GraphAPIError
import fb_helpers

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    session.forget()
    from urllib import urlencode, unquote_plus
    #local_import('fbappauth')
    landing_url = APP_URL+URL(c='default', f='quiz')
    query = dict(client_id = CLIENT_ID, scope=APP_SCOPE, 
            redirect_uri=landing_url)
    login_url=unquote_plus(FB_AUTH_URL + urlencode(query))
    response.title = APP_TITLE
    return dict(client_id = CLIENT_ID, login_url = XML(login_url), 
            landing_url = landing_url)

def quiz():
    try:
        if not updateFBAuth(request.vars['signed_request']):
            return getFacebookAuth()
        else:
            characterIdFromLastResult = getCharacterIdFromLastResult()
    except KeyError:
        #When 'signed_request' is not provided
        return getFacebookAuth()

    response.title = APP_TITLE
    response.subtitle = 'Which family guy characters are you?'
    try:
        session.userCharacter = db.characters[characterIdFromLastResult]
    except:
        session.userCharacter = None
    return dict(character = session.userCharacter, client_id = CLIENT_ID)

def analyzer():
    try:
        signed_request = parse_signed_request(request.vars['signed_request'], CLIENT_SECRET)
    except:
        from urllib import urlencode
        query = dict(client_id = CLIENT_ID, scope=APP_SCOPE, 
                redirect_uri=APP_URL+URL(c='default', f='analyzer'))
        login_url=FB_AUTH_URL + urlencode(query)
        return '<script>top.location.href="' + login_url + '";</script>'
    graph = GraphAPI(access_token = signed_request['oauth_token'])
    currentUserInfo = graph.get_object('me')
    currentUserFriends = graph.get_connections('me', 'friends')
    return BEAUTIFY([currentUserInfo])

def update():
    #user = auth.user
    #graph = getGraph()
    #try:
    #    graph.put_object('me', 'feed', 
    #            message='just got the antivirus superhero badge!',
    #            picture=request.env.http_host + URL(r=request, c='static', f='pics/superman.png'),
    #            name='%s is the antivirus hero!' % user['first_name'], caption='Antivirus Heroes',
    #            link='http://apps.facebook.com/antivirusheroes/',
    #            description='Get the highest score by killing the most virus!',
    #            actions={'name':'Submit your Ad-Aware log file',
    #            'link':'http://apps.facebook.com/antivirusheroes/'}
    #            )
    #except GraphAPIError, e:
    #    response.flash = "%s [%s: %s]" % (T("Errors! Logging you out!"),__name__, e)
    #    redirect(auth.url(f='user', args='logout')
    try:
        signed_request = parse_signed_request(request.vars['signed_request'], CLIENT_SECRET)
    except:
        redirect_uri="redirect_uri=http://apps.facebook.com/antivirusheroes/default/update&"
        login_url="https://graph.facebook.com/oauth/authorize?client_id=139729456078929&" + redirect_uri + "scope=user_photos,publish_stream&"
        return '<script>top.location.href="' + login_url + '";</script>'
    
    graph = GraphAPI(access_token = signed_request['oauth_token'])
    return BEAUTIFY([request, signed_request])
    #redirect('http://www.facebook.com/')

def showResult():
    response.title = APP_TITLE
    response.subtitle = 'Result for %s' % 'Which family guy characters are you?'
    #TODO:replace the following line with something that to do with the submission
    userCharacter = session.userCharacter = getQuizResultCharacter()
    
    updateUserCharacterInDB(session.userCharacter)
    return dict(client_id=CLIENT_ID, name=userCharacter['name'],
            pic=userCharacter['pic'],
            description=userCharacter['description'])

def getQuizResultCharacter():
    #TODO: make it related to quiz answes, or NOT?:)
    from random import choice as randomChoice
    allCharacters = db().select(db.characters.ALL)
    return randomChoice(allCharacters)

def updateUserCharacterInDB(userCharacter):
    db(db.fb_users.fb_uid == session.user_id).update(character_id = userCharacter['id'])

def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()


def updateFBAuth(signed_request):
    from fb_helpers import signed_request_getTokenWithID
    try:
        session.oauth_token, session.user_id = signed_request_getTokenWithID(signed_request, CLIENT_SECRET)
        if updateFBToken() != True:
            addFBToken()
    except:
        return False
    return True


def addFBToken():
    return db.fb_users.insert(fb_uid = session.user_id, fb_token = session.oauth_token)


def updateFBToken():
    return db(db.fb_users.fb_uid == session.user_id).update(fb_token = session.oauth_token)


def getCharacterIdFromLastResult():
    return firstRecordCharacterId(sessionUserResultRecord())


def sessionUserResultRecord():
    return db(db.fb_users.fb_uid == session.user_id).select()


def firstRecordCharacterId(record):
    return record.first().character_id

def getResultWrapper():
    character_id = request.vars['character_id']
    character = db.characters[character_id]
    imageUrl = character.pic
    description = character.description
    return DIV(DIV(IMG(_src=imageUrl), _id="result_picture"), \
    DIV(P(description), _id="result_text"), _id="result_wrapper")
