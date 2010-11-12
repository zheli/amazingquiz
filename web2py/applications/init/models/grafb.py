# -*- coding: utf-8 -*- 

def getGraph():
    a_token = auth.settings.login_form.accessToken()
    return GraphAPI(a_token)
