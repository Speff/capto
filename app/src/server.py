import sys
import signal
import time
import os
import json
from datetime import datetime

import uuid
from flask import Flask, request, session
from flask_restful import Resource, Api, reqparse

from twit_0x import *
from db_0x import *
from discord_auto import *

app = Flask(__name__)
api = Api(app)
app.secret_key = os.environ["0XIA_COOKIE_AUTH"].encode("utf-8")

# /0xia_guid/ is the site identifier for a user
class Heartbeat(Resource):
    def get(self):
        if request.method == "GET":
            twit_signed_in = None

            if '0xia_guid' in session:
                guid = session['0xia_guid']
                twit_signed_in = db_check_twit_signin(guid)
            else:
                ret_uuid = str(uuid.uuid4())
                session['0xia_guid'] = ret_uuid
                twit_signed_in = False

            return {
                    'status': 'yes',
                    'id': session['0xia_guid'],
                    'twit_authed': twit_signed_in}, 200
        else:
            return {'status': 'Forbidden'}, 403

class Check_Twitter_Signin(Resource):
    def get(self):
        if request.method != "GET" or '0xia_guid' not in session:
            return {'status': 'Unauthorized'}, 401

        endpoint_status = 'ok'
        auth_url = None
        
        signin_status = db_check_twit_signin(session['0xia_guid'])
        if signin_status == 'not signed in':
            endpoint_status, oauth_token_secret, auth_url = get_twitter_auth()
            if endpoint_status == 'ok':
                endpoint_status = db_store_oauth_secret(
                        session['0xia_guid'], oauth_token_secret)

        if endpoint_status != 'ok':
            return {
                    'status': endpoint_status,
                    'twit_status': signin_status}, 500
        else:
            return {
                    'status': 'ok',
                    'twit_status': signin_status,
                    'auth_url': auth_url}, 201

class Authorize_Twitter(Resource):
    def get(self):
        if request.method == 'GET' and "0xia_guid" in session:
            # Get these from the callback
            oauth_token = request.args.get("oauth_token")
            oauth_verifier = request.args.get('oauth_verifier')
            # Get this from db
            oauth_token_secret = db_get_oauth_token_secret(session['0xia_guid'])


            if any(v is None for v in [oauth_token, oauth_token_secret, oauth_verifier]):
                return {'status': 'Not all oath vars set'}, 500

            access_token, access_token_secret = get_twitter_access_tokens(
                    oauth_token, oauth_token_secret, oauth_verifier)

            if access_token is None or access_token_secret is None:
                return {'status': 'Access token issue'}, 500

            status = db_store_access_tokens(
                    session['0xia_guid'], access_token, access_token_secret)
            if status != 'ok':
                return {'status': 'Access token not stored'}, 500

            return { "status": "Authenticated", }, 201
        else:
            return {"status": "Access Denied"}, 403

class Get_Twitter_Self_Info(Resource):
    def get(self):
        if '0xia_guid' not in session:
            return {"status": "Not Authenticated"}, 200

        status, twit_name, twit_sn = get_twitter_info(session['0xia_guid'])

        if status != 'ok':
            return {"status": status}, 200

        status = db_store_twit_sn(session['0xia_guid'], twit_sn)
        if status != 'ok':
            return {"status": status}, 200

        return {
                "status": "Authenticated",
                "twitter_name": twit_name}, 200

class Add_WebHook(Resource):
    def post(self):
        if '0xia_guid' not in session:
            return {"status": "Not Authenticated"}, 200

        parser = reqparse.RequestParser(trim=True)
        parser.add_argument(
                'hook_uid',
                type=uid_type,
                required=False,
                help='Webhook UID (UID)')
        parser.add_argument(
                'label',
                type=label_type,
                help='Webhook Label (string)')
        parser.add_argument(
                'webhook_url',
                type=webhook_url_type,
                help='Webhook URL (string)')
        parser.add_argument(
                'twit_target',
                type=str,
                help='Twitter target user (string)')
        parser.add_argument(
                's_fav',
                type=yes_no_type,
                help='Choose favorites (Yes/No)')
        parser.add_argument(
                's_post',
                type=yes_no_type,
                help='Choose posts (Yes/No)')
        parser.add_argument(
                'grab_type',
                type=yes_no_type,
                help='Grab media only? (Yes/No)')
        args = parser.parse_args(strict=True)

        if not validate_args(args):
            return {"status": "Invalid arguments"}, 400

        twit_user = db_get_twit_sn(session['0xia_guid'])
        if twit_user is None:
            return {"status": 'Twitter login expired'}, 400

        # Generate a hook uid if it hasn't been provided
        if args['hook_uid'] is None:
            args['hook_uid'] = str(uuid.uuid4())

        store_result = db_store_webhook(args['hook_uid'], twit_user, args['label'],
                args['webhook_url'], args['twit_target'], args['s_fav'],
                args['s_post'], args['grab_type'])
        if store_result == 'ok':
            return {'status': 'webhook stored'}, 201
        else:
            return {'status': 'webhook not stored',
                    'error': store_result}, 500
        
        return None

class Get_Webhooks(Resource):
    def get(self):
        if '0xia_guid' not in session:
            return {"status": "Not Authenticated"}, 200

        twit_user = db_get_twit_sn(session['0xia_guid'])
        if twit_user is None:
            return {"status": 'Twitter login expired'}, 400

        webhooks = db_get_webhooks(twit_user)
        if webhooks is None:
            return {"status": 'No webhooks found'}, 204

        return {
                "status": "ok",
                "webhooks": webhooks}, 200

api.add_resource(Heartbeat, '/r_u_alive')
api.add_resource(Check_Twitter_Signin, '/check_twit_signin')
api.add_resource(Authorize_Twitter, '/auth_twit')
api.add_resource(Get_Twitter_Self_Info, '/get_twit_name')
api.add_resource(Add_WebHook, '/add_hook')
api.add_resource(Get_Webhooks, '/get_hooks')

def handler(signum, frame):
    sys.exit(1)

if __name__ == '__main__':
    print('Server started')
    signal.signal(signal.SIGTERM, handler)

    app.run(debug=True, host='0.0.0.0', port=1123)
