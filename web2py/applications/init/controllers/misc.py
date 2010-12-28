#from default import updateFBAuth
import facebook
from gluon.tools import fetch

def push_greetings():
    #updateFBAuth(request.vars['signed_request'])
    graph = facebook.GraphAPI(session.app_token)
    user = graph.get_object('171657759516876')
    graph.put_object('171657759516876', 'feed',
            message='',
            picture= 'http://www.familyguyfun.com/images/31dd.jpg', caption= '',
            name='Greetings from Amazing Quiz!',
            link='http://apps.facebook.com/amazing_quiz/',
            description= 'Wish you a merry christmas',
#            privacy={'value':'ALL_FRIENDS'},
            actions={'name':'Check who are you',
            'link':'http://apps.facebook.com/amazing_quiz/'}
            )
    return True

def get_app_auth():
    page = fetch('https://graph.facebook.com/oauth/access_token?grant_type=client_credentials&client_id=171657759516876&client_secret=1ab56c84a1d338972c8786e49eaa7247')
    key, token = page.split('=')
    session.app_token = token
    return True
