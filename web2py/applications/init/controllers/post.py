# -*- coding: utf-8 -*-
from facebook import GraphAPI, GraphAPIError

@auth.requires_login()
def index():
    user = auth.user
    graph = getGraph()
    try:
        graph.put_object('1603106506', 'feed', message = 'Awesome blog!', link='http://blog.systemsthoughts.com',
                        description = 'Test posting stuff on facebook stream', 
                        picture='http://bestuff.com/images/images_of_stuff/64x64crop/robot-chicken-159468.jpg')
    except GraphAPIError, e:
        response.flash = "%s [%s: %s]" % (T("Logging you out!"),__name__, e)
        redirect(auth.url(f='user', args='logout'))

    return True

@auth.requires_login()
def getFeed():
    user = auth.user
    connection = getGraph().get_connections('me', 'feed')
    print(connection['data'][0]['id'])

    return True

@auth.requires_login()
def comment():
    getGraph().put_object('326200042_502910060313', 'comments', message='comment by myself')

    return True
