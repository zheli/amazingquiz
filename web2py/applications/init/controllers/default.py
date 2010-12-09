# -*- coding: utf-8
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

# TODO: finish getFacebookAuth()

import facebook
import fb_helpers
import logging
logging.getLogger().setLevel(logging.DEBUG)

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

def publishResult():
    if session.oauth_token:
        graph = facebook.GraphAPI(session.oauth_token)
        user = graph.get_object('me')
        graph.put_object('me', 'feed', 
                message='just finished a quiz using Amazing Quiz!',
                picture= session.userCharacter['pic'], caption= '',
                name='%s is %s' % (user['first_name'], session.userCharacter['name']),
                link='http://apps.facebook.com/amazing_quiz/',
                description= session.userCharacter['description'],
                actions={'name':'Check who are you',
                'link':'http://apps.facebook.com/amazing_quiz/'}
                )
        return True
    else:
        return None


def showResult():
    response.title = APP_TITLE
    response.subtitle = 'Result for %s' % 'Which family guy characters are you?'
    #TODO:replace the following line with something that to do with the submission
    userCharacter = session.userCharacter = getQuizResultCharacter()
    
    updateUserCharacterInDB(session.userCharacter)
    return dict(client_id=CLIENT_ID, name=userCharacter['name'],
            pic=userCharacter['pic'],
            description=userCharacter['description'],
            characterId = userCharacter['id'])

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


def getFriendUsersResultWrapper():
    friendUsers = getUserFriendsInQuizUsers()
    wrapContent = []
    for user in friendUsers:
        photoUrl = u'https://graph.facebook.com/%s/picture?type=large' % user
        userRecord = db(db.fb_users.fb_uid == user).select(db.fb_users.ALL, orderby=db.fb_users.fb_uid).first()
        logging.debug(userRecord)
        userCharacter = db.characters[userRecord['character_id']]
        characterPhotoUrl = userCharacter.pic
        logging.debug(characterPhotoUrl)
        wrapContent.append(DIV(IMG(_src = photoUrl, _height=120), IMG(_src = characterPhotoUrl, _height=120)))
    return BEAUTIFY(wrapContent)


def getUserFriendsInQuizUsers():
    quizUsers = getQuizUsers()
    userFriends = getUserFriends()
    friendUsers = []
    for userFriend in userFriends:
        if userFriend[u'id'] in quizUsers:
            friendUsers.append(userFriend[u'id'])
    return friendUsers


def getUserFriends():
    friendList = []
    graph = facebook.GraphAPI(session.oauth_token)
    friends = graph.get_connections("me", "friends")
    return friends[u'data']


def getQuizUsers():
    userList = []
    QuizUsers = db().select(db.fb_users.ALL, orderby=db.fb_users.fb_uid)
    for user in QuizUsers:
        userList.append(unicode(user['fb_uid']))
    return userList
