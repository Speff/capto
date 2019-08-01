CREATE TABLE user_status(
    user_0x TEXT UNIQUE NOT NULL,
    twit_sn TEXT NOT NULL,
    last_visited TIMESTAMP NOT NULL DEFAULT NOW(),
    status TEXT
);

CREATE TABLE user_keys(
    user_0x TEXT UNIQUE NOT NULL,
    oauth_token_secret TEXT,
    access_token TEXT,
    access_token_secret TEXT
);

CREATE TABLE webhooks(
    hook_uid TEXT NOT NULL UNIQUE,
    twit_sn TEXT NOT NULL,
    label TEXT DEFAULT 'N/A',
    url TEXT NOT NULL,
    twit_target TEXT NOT NULL,
    favorites BOOL DEFAULT False,
    posts BOOL DEFAULT False,
    media_only BOOL DEFAULT False,
    time_added TIMESTAMP NOT NULL DEFAULT NOW(),
    time_queried TIMESTAMP NOT NULL DEFAULT NOW() - interval '1 day'
);
