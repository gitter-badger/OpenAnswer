import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
OAUTH_CREDENTIALS = {
    'facebook': {
        'id': os.environ['FB_OAUTH_ID'],
        'secret': os.environ['FB_OAUTH_SECRET'],
    },
    'google': {
        'id': os.environ['GO_OAUTH_ID'],
        'secret': os.environ['GO_OAUTH_SECRET'],
    },
    'slack': {
        'id': os.environ['SL_OAUTH_ID'],
        'secret': os.environ['SL_OAUTH_SECRET']
    }
}