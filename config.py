import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists('.env'):
    print('Importing environment from .env file')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1].replace("\"", "")


def getMultiDBConnURL(data_env, default_env):
    if data_env:
        if "," in data_env:
            list_env_url = data_env.split(",")
            env_url = {}
            for data_env_url in list_env_url:
                env_url_split = data_env_url.split("/")
                env_url[env_url_split[3]] = data_env_url
        else:
            env_url_split = data_env.split("/")
            env_url = {
                env_url_split[3]: data_env
            }
    elif default_env in (None, "") or data_env in (None, ""):
        return None
    else:
        env_url_split = default_env.split("/")
        env_url = {
            env_url_split[3]: default_env
        }
    return env_url


class Config(object):
    APP_NAME = os.environ.get('APP_NAME') or 'Flask-Base'
    FLASK_ENVIRONMENT = os.environ.get('FLASK_ENVIRONMENT')

    if FLASK_ENVIRONMENT != "production":
        DEBUG = os.environ.get('DEBUG') or False
    else:
        DEBUG = False

    SSL_DISABLE = (os.environ.get('SSL_DISABLE') or 'True') == 'True'
    WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED') or False
    DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
    X_EMAIL = os.environ.get('X_EMAIL')
    X_USERNAME = os.environ.get('X_USERNAME')
    X_PASSWORD = os.environ.get('X_PASSWORD')
    X_URL = os.environ.get('X_URL')
    OS_TYPE = os.environ.get('OS_TYPE')

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 1}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }

    SCHEDULER_API_ENABLED = True

    @staticmethod
    def init_app(app):
        print('THIS APP IS IN ' + str(app.config['FLASK_ENVIRONMENT']).upper() + ' MODE. \
                YOU SHOULD NOT SEE THIS IN PRODUCTION.')


CONFIG = Config
