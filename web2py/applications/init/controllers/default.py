# -*- coding: utf-8
#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

from facebook import GraphAPI, GraphAPIError
from fb_helpers import parse_signed_request

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    from urllib import urlencode, unquote_plus
    local_import('fbappauth')
    landing_url = APP_URL+URL(c='default', f='quiz')
    query = dict(client_id = CLIENT_ID, scope=APP_SCOPE, 
            redirect_uri=landing_url)
    login_url=unquote_plus(FB_AUTH_URL + urlencode(query))
    return dict(client_id = CLIENT_ID, login_url = XML(login_url), 
            landing_url = landing_url)

def quiz():
    return dict()

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
    from quiz_helpers import findMaxScore
    score = {'a1': 0,
            'a2' : 0,
            'a3': 0,
            'a4': 0,
            'a5': 0,
            'a6': 0,
            'a7': 0,
            'a8': 0,
            'a9': 0,
            'a10': 0,
            'a11': 0,
            }
    for i in request.vars:
        answer = request.vars[i]
        if answer == 'a1':
            score['a1']  = score['a1'] + 1
        elif answer == 'a2':
            score['a2']   = score['a2']  + 1
        elif answer == 'a3':
            score['a3']  = score['a3'] + 1
        elif answer == 'a4':
            score['a4']  = score['a4'] + 1
    answer = findMaxScore(score)
    character = db.characters(db.characters.answer == answer)
    return DIV(B('You are %s.' % character['name']), BR(), 
            IMG(_src=character['pic'], _height=320), BR(),
            P(character['description']))

def showRequest():
    return BEAUTIFY(request)

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


