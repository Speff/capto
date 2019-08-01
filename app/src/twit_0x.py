import os
import twitter
import oauth2 as oauth
import urllib.parse

from db_0x import *

__all__ = ['get_twitter_auth', 'get_twitter_access_tokens', 'get_twitter_info']

def get_twitter_info(session_user):
    access_token, access_token_secret = get_user_twitter_credentials(session_user)
    if any(v is None for v in [access_token, access_token_secret]):
        return 'Failed - no access tokens found', None, None

    twit_api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
            consumer_secret=os.environ['CONSUMER_SECRET'],
            access_token_key=access_token,
            access_token_secret=access_token_secret)
    try:
        user = twit_api.VerifyCredentials()
        return 'ok', user.name, user.screen_name
    except Exception as e:
        print(e)
        return "twitter auth not accepted" + e, None, None

def get_twitter_auth():
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    
    request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=" + os.environ['CALLBACK_URL']
    authorize_url = 'https://api.twitter.com/oauth/authorize'

    try:
        client = oauth.Client(consumer)

        resp, content = client.request(request_token_url, "GET")
        if resp['status'] != '200':
            return ("Twitter unavailable", None, None)
        
        request_token = dict(urllib.parse.parse_qsl(content))
        oauth_token_secret = request_token["oauth_token_secret".encode("utf-8")].decode("utf-8")

        auth_url = f'{authorize_url}?oauth_token={str(request_token["oauth_token".encode("utf-8")].decode("utf-8"))}'

        return ('ok', oauth_token_secret, auth_url)
    except Exception as e:
        return(f'Twitter auth url failed: {e}', None, None)

def get_twitter_access_tokens(oauth_token, oauth_token_secret, verifier):
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(verifier)
    
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    
    client = oauth.Client(consumer, token)
    
    try:
        resp, content = client.request(access_token_url, "POST")
        access_token_dict = dict(urllib.parse.parse_qsl(content))
    except Exception as e:
        return None, None
    
    access_token = "%s" % access_token_dict['oauth_token'.encode("utf-8")].decode("utf-8")
    access_token_secret = "%s" % access_token_dict['oauth_token_secret'.encode("utf-8")].decode("utf-8")

    return access_token, access_token_secret
