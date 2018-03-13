from authentication_keys import *
from time_helpers import *
from process_tweet_object import *
from graph_helper import *
from process_text import *
from file_helpers import *

from tweepy import OAuthHandler
from tweepy import API
from collections import Counter
from datetime import datetime, date, time, timedelta

import sys
import json
import os
import io
import re
import time

if __name__ == "__main__":

    found_bots = load_json("output/found_bots.json")
    name_to_id = load_json("output/name_to_id.json")

    bot_ids = []
    unknown = []
    for name in found_bots:
        if name in name_to_id:
            bot_ids.append(name_to_id[name])
        else:
            unknown.append(name)
    save_json(unknown, "unknown.json")
    save_json(bot_ids, "bot_ids.json")

