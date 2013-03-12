#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime

from flask import Flask
from flask import render_template
from flask.ext.cache import Cache

import t

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route("/")
@app.route('/<twitter_id>')
@cache.cached(timeout=300)
def twitter_timeline(twitter_id='chuangbo'):
    return render_template('tweets.html', user=t.api.get_user(twitter_id), tweets=t.api.user_timeline(twitter_id))

@app.template_filter()
def friendly_time(dt, past_="ago", 
    future_="from now", 
    default="just now"):
    """
    Returns string representing "time since"
    or "time until" e.g.
    3 days ago, 5 hours from now etc.
    """

    now = datetime.utcnow()
    if now > dt:
        diff = now - dt
        dt_is_past = True
    else:
        diff = dt - now
        dt_is_past = False

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s %s" % (period, \
                singular if period == 1 else plural, \
                past_ if dt_is_past else future_)

    return default

if __name__ == "__main__":
    app.run()

