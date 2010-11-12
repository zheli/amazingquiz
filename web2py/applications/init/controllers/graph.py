# -*- coding: utf-8 -*-
from facebook import GraphAPI, GraphAPIError

@auth.requires_login()
def index():
    user = auth.user
    response.flash = T('You are %(name)s', dict(name=user['first_name']))
    if  len(request.args) >= 2 and request.args[0] == 'id':
        fb_id = request.args[1]
    else:
        fb_id = 'me'
    
    graph = getGraph()
    try:
        fb_obj = graph.get_object(fb_id, metadata=1)
    except GraphAPIError, e:
        response.flash = "%s [%s: %s]" % (T("Logging you out!"),__name__, e)
        redirect(auth.url(f='user', args='logout'))
    
    response.menu = [[k, False, URL(r=request, f='connection', args=[fb_id,k])] for k,v in  fb_obj['metadata']['connections'].items()]
    return dict(message=T('You are at  %(fb_id)s', dict(fb_id=fb_id)))

@auth.requires_login()
def connection():
    user = auth.user
    if not len(request.args) >= 2:
        return None
    fb_id = request.args[0]
    fb_connection_name = request.args[1]
    try:
        connections = getGraph().get_connections(fb_id, fb_connection_name)
    except GraphAPIError, e:
        response.flash = "%s [%s: %s]" % (T("Logging you out!"),__name__, e)
        redirect(auth.url(f='user', args='logout'))

    
    response.menu=[[v['name'], False, URL(r=request, f='index', args=['id', v['id']])]  for v in connections['data']]
    return dict(message=T('Looking list of %(conn_name)s of %(id)s', dict(conn_name=fb_connection_name, id=fb_id)))

