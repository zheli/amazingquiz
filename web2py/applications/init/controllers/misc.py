#from default import updateFBAuth
import facebook
from google.tools import fetch

def push_greetings():
    #updateFBAuth(request.vars['signed_request'])
    graph = facebook.GraphAPI(session.app_token)
    user = graph.get_object('100001781330977')
    graph.put_object('100001781330977', 'feed',
            message='',
            picture= 'http://www.familyguyfun.com/images/31dd.jpg', caption= '',
            name='Greetings from Amazing Quiz!',
            link='http://apps.facebook.com/amazing_quiz/',
            description= 'Wish you a merry christmas',
            actions={'name':'Check who are you',
            'link':'http://apps.facebook.com/amazing_quiz/'}
            )
    return True

def get_app_auth():
    page = fetch('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=175543849124765&client_secret=71c2c6004acb13b998e0b7aed3caafd3')
    key, token = page.split('=')
    session.app_token = token
    return True
