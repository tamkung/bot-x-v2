import os
import logging
import pytz
import uwsgi
from datetime import datetime
from config import CONFIG as ENV_CONFIG
from flask import Flask
from flask_apscheduler import APScheduler

SCHEDULER = APScheduler()
SERVICE_NAME = "backend"

BASEDIR = os.path.abspath(os.path.dirname(__file__))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(process)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z00",
)
LOGGER = logging.getLogger("python-logstash-logger")
LOGGER.setLevel(logging.INFO)

CURRENT_NOW = datetime.now(pytz.utc)


def convertStringToBoolean(string_bool):
    # Convert string to Boolean(first char in string is equal T)
    if str(string_bool)[:1].upper() == "T":
        return True
    else:
        return False


def createApp():
    app = Flask(__name__)
    app.config.from_object(ENV_CONFIG)
    app.config["WTF_CSRF_ENABLED"] = convertStringToBoolean(ENV_CONFIG.WTF_CSRF_ENABLED)
    app.config["SCHEDULER_TIMEZONE"] = "Asia/Bangkok"  # ตั้ง timezone เป็น UTC (หรืออื่น ๆ ที่ต้องการ)
    ENV_CONFIG.init_app(app)

    with app.app_context():
        SCHEDULER.init_app(app)

    # create directory tmp
    try:
        # Create target Directory
        os.mkdir("tmp")
    except FileExistsError:
        pass

    from app.test import TEST_BLUEPRINT
    from app.tweet import TWEET_BLUEPRINT

    app.register_blueprint(TEST_BLUEPRINT)
    app.register_blueprint(TWEET_BLUEPRINT)

    if ENV_CONFIG.DEBUG == "True":
        ENV_CONFIG.DEBUG = True
    else:
        ENV_CONFIG.DEBUG = False

    print(CURRENT_NOW)

    # start schedule
    from app.tweet.controller import receiveTweetLive
    print("start schedule")
    SCHEDULER.add_job(func=receiveTweetLive, trigger="interval", id="receiveTweetLive", name="receiveTweetLive", seconds=40, replace_existing=True, max_instances=10)
    SCHEDULER.start()

    return app
