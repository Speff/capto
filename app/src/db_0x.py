import psycopg2
from psycopg2.extras import RealDictCursor

__all__ = ['db_store_oauth_secret', 'db_check_twit_signin',
        'db_get_oauth_token_secret', 'db_store_access_tokens', 
        'get_user_twitter_credentials', 'db_store_webhook', 'db_store_twit_sn',
        'db_get_twit_sn', 'db_get_webhooks']

pg_connect_info = "dbname=da_db user=da_user password=docker host=db"

def db_get_webhooks(twit_sn):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        pg_cur.execute(\
                """ SELECT                                               """ \
                """     hook_uid,                                        """ \
                """     label,                                           """ \
                """     url,                                             """ \
                """     twit_target,                                     """ \
                """     favorites,                                       """ \
                """     posts,                                           """ \
                """     media_only,                                      """ \
                """     extract(epoch from time_added) AS time_added,    """ \
                """     extract(epoch from time_queried) AS time_queried """ \
                """ FROM webhooks                                        """ \
                """ WHERE                                                """ \
                """     twit_sn=%s;                                      """ ,
                (twit_sn,))

        ret = pg_cur.fetchall()
        if ret is None:
            return None
        else: 
            return ret
    except Exception as e:
        print(f'Error retreiving webhooks for user {session_user}\n{e}')
        return None
    finally:
        pg_con.close()

def db_store_twit_sn(session_user, twit_sn):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ INSERT INTO user_status  """ \
                """     (user_0x,            """ \
                """     twit_sn)             """ \
                """ VALUES (%s, %s)          """ \
                """ ON CONFLICT (user_0x)    """ \
                """ DO UPDATE                """ \
                """ SET                      """ \
                """     twit_sn=%s,          """ \
                """     last_visited=Now();  """ ,
                (session_user, twit_sn, twit_sn))
        pg_con.commit()
        return 'ok'
    except Exception as e:
        return f'Store username/session failed: {e}'
    finally:
        pg_con.close()

def db_get_twit_sn(session_user):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ SELECT twit_sn    """ \
                """ FROM user_status  """ \
                """ WHERE             """ \
                """     user_0x=%s;   """ ,
                (session_user,))

        ret = pg_cur.fetchone()
        if ret is None:
            return None
        else: 
            return ret[0]
    except Exception as e:
        print(f'Error retreiving twit credentials for user {session_user}\n{e}')
        return None
    finally:
        pg_con.close()

def get_user_twitter_credentials(session_user):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ SELECT                                  """ \
                """     access_token,                       """ \
                """     access_token_secret                 """ \
                """ FROM user_keys                          """ \
                """ WHERE                                   """ \
                """     user_0x=%s                          """ \
                """     AND access_token IS NOT NULL        """ \
                """     AND access_token_secret IS NOT NULL """ ,
                (session_user,))

        ret = pg_cur.fetchone()
        if ret is None:
            return None, None
        else: 
            return ret[0], ret[1]
    except Exception as e:
        print(f'Error retreiving twit credentials for user {session_user}\n{e}')
        return None, None
    finally:
        pg_con.close()


def db_store_webhook( hook_uid, twit_sn, label, webhook_url, twit_target,
        favorites, posts, media_only):

    query = None
    existing_hooks = db_get_webhooks(twit_sn)

    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        if existing_hooks is None:
            query = \
                    """ INSERT INTO webhooks                 """ \
                    """     (hook_uid,                       """ \
                    """     twit_sn,                         """ \
                    """     label,                           """ \
                    """     url,                             """ \
                    """     twit_target,                     """ \
                    """     favorites,                       """ \
                    """     posts,                           """ \
                    """     media_only)                      """ \
                    """ VALUES                               """ \
                    """     (%s, %s, %s, %s, %s, %s, %s, %s) """ \
                    """ ON CONFLICT DO NOTHING;              """ 
            pg_cur.execute(query,
                    (hook_uid, twit_sn, label, webhook_url, twit_target,
                        favorites, posts, media_only))
        else:
            uid_list = []
            for hook in existing_hooks: uid_list.append(hook['hook_uid'])
            if hook_uid in uid_list:
                # Only replace hook if the conflicting hook belongs to submitting
                # user
                query = \
                        """ INSERT INTO webhooks                 """ \
                        """     (hook_uid,                       """ \
                        """     twit_sn,                         """ \
                        """     label,                           """ \
                        """     url,                             """ \
                        """     twit_target,                     """ \
                        """     favorites,                       """ \
                        """     posts,                           """ \
                        """     media_only)                      """ \
                        """ VALUES                               """ \
                        """     (%s, %s, %s, %s, %s, %s, %s, %s) """ \
                        """ ON CONFLICT (hook_uid)               """ \
                        """ DO UPDATE                            """ \
                        """     SET twit_sn=%s,                  """ \
                        """         label=%s,                    """ \
                        """         url=%s,                      """ \
                        """         twit_target=%s,              """ \
                        """         favorites=%s,                """ \
                        """         posts=%s,                    """ \
                        """         media_only=%s;               """
                pg_cur.execute(query, (hook_uid, twit_sn, label, webhook_url,
                    twit_target, favorites, posts, media_only, twit_sn, label,
                    webhook_url, twit_sn, favorites, posts, media_only))
            else:
                query = \
                        """ INSERT INTO webhooks                 """ \
                        """     (hook_uid,                       """ \
                        """     twit_sn,                         """ \
                        """     label,                           """ \
                        """     url,                             """ \
                        """     twit_target,                     """ \
                        """     favorites,                       """ \
                        """     posts,                           """ \
                        """     media_only)                      """ \
                        """ VALUES                               """ \
                        """     (%s, %s, %s, %s, %s, %s, %s, %s) """ \
                        """ ON CONFLICT DO NOTHING;              """ 
                pg_cur.execute(query,
                        (hook_uid, twit_sn, label, webhook_url, twit_target,
                            favorites, posts, media_only))
            pg_con.commit()
        return 'ok'
    except Exception as e:
        return f'Webhook insert failed: {e}'
    finally:
        pg_con.close()

def db_store_oauth_secret(session_user, oauth_token_secret):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ INSERT INTO user_keys                """ \
                """     (user_0x,                        """ \
                """     oauth_token_secret)              """ \
                """ VALUES (%s, %s)                      """ \
                """ ON CONFLICT (user_0x)                """ \
                """ DO UPDATE SET oauth_token_secret=%s; """ ,
                (session_user, oauth_token_secret, oauth_token_secret))
        pg_con.commit()
        return 'ok'
    except Exception as e:
        return f'Pg oauth secret insert failed: {e}'
    finally:
        pg_con.close()

def db_store_access_tokens(session_user, access_token, access_token_secret):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ UPDATE user_keys                   """ \
                """ SET                                """ \
                """     access_token=%s,               """ \
                """     access_token_secret=%s         """ \
                """ WHERE user_0x=%s;                  """ ,
                (access_token, access_token_secret, session_user))
        pg_con.commit()
        return 'ok'
    except Exception as e:
        return f'Pg access token insert failed: {e}'
    finally:
        pg_con.close()

def db_check_twit_signin(session_user):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ SELECT COUNT(*)                         """ \
                """ FROM user_keys                          """ \
                """ WHERE                                   """ \
                """     user_0x=%s                          """ \
                """     AND access_token IS NOT NULL        """ \
                """     AND access_token_secret IS NOT NULL """ \
                """ LIMIT 1;                                """ ,
                (session_user,))
        if pg_cur.fetchone()[0] == 1:
            return 'signed in'
        else:
            return 'not signed in'

    except Exception as e:
        return f'Pg twit sign-in check failed: {e}'
    finally:
        pg_con.close()

def db_get_oauth_token_secret(session_user):
    try:
        pg_con = psycopg2.connect(pg_connect_info)
        pg_cur = pg_con.cursor()
        pg_cur.execute(\
                """ SELECT oauth_token_secret     """ \
                """ FROM user_keys                """ \
                """ WHERE user_0x=%s              """ ,
                (session_user,))

        ret = pg_cur.fetchone()[0]
        return ret
    except Exception as e:
        print(f'Error retreiving oauth token for user {session_user}\n{e}')
        return None
    finally:
        pg_con.close()
