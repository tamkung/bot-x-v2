from flask import Blueprint

from app.tweet.controller import receiveTweetLive

TWEET_BLUEPRINT = Blueprint('tweet', __name__, url_prefix="/tweet")

TWEET_BLUEPRINT.add_url_rule("", "receiveTweetLive", view_func=receiveTweetLive, methods=["GET"])