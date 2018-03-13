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


def get_auth():
    acct_name, consumer_key, consumer_secret, access_token, access_token_secret = get_account_sequential()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return API(auth)


def get_user_objects_from_ids(follower_ids):
    batch_len = 100
    num_batches = len(follower_ids) / 100
    batches = (follower_ids[i:i+batch_len] for i in range(0, len(follower_ids), batch_len))
    all_data = []
    auth = []
    current_auth = get_auth()
    for batch_count, batch in enumerate(batches):
        if batch_count > 0 and batch_count % 50 == 0:
            del(current_auth)
            print("Getting new auth")
            current_auth = get_auth()
        print("Batch: " + str(batch_count))
        users_list = current_auth.lookup_users(user_ids=batch)
        users_json = (map(lambda t: t._json, users_list))
        all_data += users_json
    return all_data


if __name__ == "__main__":

    found_bots = load_json("output/found_bots.json")
    name_to_id = load_json("output/name_to_id.json")

    bot_ids = []
    for name in found_bots:
        if name in name_to_id:
            bot_ids.append(name_to_id[name])
    save_json(bot_ids, "output/bot_ids.json")
    all_objects = get_user_objects_from_ids(bot_ids)
    save_json(all_objects, "output/all_objects.json")

    bot_objects = {}
    for user in all_objects:
        if "id_str" in user:
            bot_objects[user["id_str"]] = user
    save_json(bot_objects, "output/bot_objects.json")

