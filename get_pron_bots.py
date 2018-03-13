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

def query_screen_names(screen_names):
    print("Querying " + str(len(screen_names)) + " screen names.")
    auth_api = get_auth()
    batch_len = 100
    batches = (screen_names[i:i+batch_len] for i in range(0, len(screen_names), batch_len))
    all_json = []
    for batch_count, batch in enumerate(batches):
        print("Batch: " + str(batch_count))
        users_list = auth_api.lookup_users(screen_names=batch)
        users_json = (map(lambda t: t._json, users_list))
        all_json += users_json
    return all_json

def query_ids(ids):
    print("Querying " + str(len(ids)) + " ids.")
    auth_api = get_auth()
    batch_len = 100
    batches = (ids[i:i+batch_len] for i in range(0, len(ids), batch_len))
    all_json = []
    for batch_count, batch in enumerate(batches):
        print("Batch: " + str(batch_count))
        users_list = auth_api.lookup_users(user_ids=batch)
        users_json = (map(lambda t: t._json, users_list))
        all_json += users_json
    return all_json

def record_info(user_object):
    global name_to_id, id_to_name
    d = user_object
    if d is not None:
        if "id_str" in d and d["id_str"] is not None and "screen_name" in d and d["screen_name"] is not None:
            screen_name = d["screen_name"]
            id_str = d["id_str"]
            if screen_name is not None and id_str is not None:
                name_to_id[screen_name] = id_str
                id_to_name[id_str] = screen_name

def get_friends_ids(target, auth_api):
    print("Getting friends list for " + target)
    try:
        return auth_api.friends_ids(target)
    except:
        print("Account " + target + " was not accessible.")
        return []

def get_followers_ids(target, auth_api):
    print("Getting followers list for " + target)
    try:
        return auth_api.followers_ids(target)
    except:
        print("Account " + target + " was not accessible.")
        return []

def get_auth():
    acct_name, consumer_key, consumer_secret, access_token, access_token_secret = get_account_sequential()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return API(auth)

def get_porn_bot_friends(target):
    global interactions
    a = get_auth()
    friends = get_friends_ids(target, a)
    del(a)
    if len(friends) > 0:
        bots = get_bots_from_ids(friends)
        if bots is not None and len(bots) > 0:
            if target not in interactions:
                interactions[target] = Counter()
            for b in bots:
                interactions[target][b] += 1
        return bots

def get_porn_bot_followers(target):
    global interactions
    a = get_auth()
    friends = get_followers_ids(target, a)
    del(a)
    if len(friends) > 0:
        bots = get_bots_from_ids(friends)
        if bots is not None and len(bots) > 0:
            for b in bots:
                if b not in interactions:
                    interactions[b] = Counter()
                interactions[b][target] += 1
        return bots

def get_bots_from_names(name_list):
    global found_bots, bot_objects
    print("Getting bots from names.")
    print("Received " + str(len(name_list)) + " names.")
    print("Checking for previously queried names.")
    unqueried = []
    for d in name_list:
        if d not in name_to_id:
            unqueried.append(d)
    print("Got " + str(len(unqueried)) + " unqueried names.")
    ret = []
    if len(unqueried) > 0:
        users = query_screen_names(unqueried)
        print("Retrieved " + str(len(users)) + " user objects")
        if len(users) > 0:
            for user in users:
                record_info(user)
                if is_pron_bot(user):
                    if user["screen_name"] not in found_bots:
                        print("Found new bot: " + user["screen_name"])
                        ret.append(user["screen_name"])
                        found_bots.append(user["screen_name"])
                        bot_objects[user["id_str"]] = user
    return ret

def get_bots_from_ids(id_list):
    global found_bots, bot_objects
    print("Getting bots from ids.")
    print("Received " + str(len(id_list)) + " ids.")
    print("Checking for previously queried ids.")
    unqueried = []
    for d in id_list:
        if d not in id_to_name:
            unqueried.append(d)
    print("Got " + str(len(unqueried)) + " unqueried ids.")
    ret = []
    if len(unqueried) > 0:
        users = query_ids(unqueried)
        print("Retrieved " + str(len(users)) + " user objects")
        if len(users) > 0:
            for user in users:
                record_info(user)
                if is_pron_bot(user):
                    if user["screen_name"] not in found_bots:
                        print("Found new bot: " + user["screen_name"])
                        ret.append(user["screen_name"])
                        found_bots.append(user["screen_name"])
                        bot_objects[user["id_str"]] = user
    return ret

def is_pron_bot(user):
    desc_matches = ["Check this", "How do you like my site", "How do you like me", "You love it harshly", "Do you like fast", "Do you like it gently", "Come to my site", "Come in", "Come on", "Come to me", "I want you", "You want me", "Your favorite", "Waiting you", "Waiting you at", "me2url.info", "url4.pro", "click2go.info", "move2.pro", "zen5go.pro", "go9to.pro"]
    found = False
    if "description" in user:
        for d in desc_matches:
            if d in user["description"]:
                found = True
    if "verified" in user and user["verified"] == True:
        found = False
    if "followers_count" in user and user["followers_count"] > 500:
        found = False
    return found

def dump_list(var, filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        for v in var:
            f.write(v + u"\n")

def countdown_timer(val):
    countdown = val
    step = 1
    while countdown > 0:
        msg = "Time left: " + str(countdown)
        sys.stdout.write(msg)
        sys.stdout.flush()
        time.sleep(step)
        sys.stdout.write("\r")
        countdown -= step
    return

def get_bots_recursive(names):
    global queried
    new_bots = []
    for count, target in enumerate(names):
        if target not in queried:
            if count % 10 == 0:
                print("Saving data...")
                save_json(queried, "output/queried.json")
                save_json(name_to_id, "output/name_to_id.json")
                save_json(id_to_name, "output/id_to_name.json")
                save_json(found_bots, "output/found_bots.json")
                save_json(bot_objects, "output/bot_objects.json")
                save_json(interactions, "output/interactions.json")
                save_gephi_csv(interactions, "output/interactions.csv")
                dump_list(found_bots, "output/bots.txt")
            print("Bots found so far: " + str(len(found_bots)))
            print("Accounts queried so far: " + str(len(queried)))
            print("Sleeping")
            countdown_timer(23)
            print(str(count) + "/" + str(len(names)) + ": " + target)
            queried.append(target)
            bots = get_porn_bot_friends(target)
            if bots is not None and len(bots) > 0:
                for bot in bots:
                    if bot not in queried:
                        if bot not in new_bots:
                            new_bots.append(bot)
            bots = get_porn_bot_followers(target)
            if bots is not None and len(bots) > 0:
                for bot in bots:
                    if bot not in queried:
                        if bot not in new_bots:
                            new_bots.append(bot)
    if len(new_bots) > 0:
        get_bots_recursive(new_bots)


if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")

    print("Loading saved data.")
    interactions = {}
    if os.path.exists("output/interactions.json"):
        interactions = load_json("output/interactions.json")

    found_bots = []
    if os.path.exists("output/found_bots.json"):
        found_bots = load_json("output/found_bots.json")

    queried = []
    if os.path.exists("output/queried.json"):
        queried = load_json("output/queried.json")

    name_to_id = {}
    if os.path.exists("output/name_to_id.json"):
        name_to_id = load_json("output/name_to_id.json")

    id_to_name = {}
    if os.path.exists("output/id_to_name.json"):
        id_to_name = load_json("output/id_to_name.json")

    bot_objects = {}
    if os.path.exists("output/bot_objects.json"):
        bot_objects = load_json("output/bot_objects.json")

# Start by checking the initial list for bots
    print("Checking initial list.")
    print("Gettings ids from initial account list.")
    unqueried = []
    print("Already queried: " + str(len(queried)))
    for n in found_bots:
        if n not in queried:
            unqueried.append(n)
    print("Unqueried: " + str(len(unqueried)))

# Check if any of this list of accounts is not yet known to be a bot
    unsure = []
    sure = []
    for name in unqueried:
        if name not in found_bots:
            unsure.append(name)
        else:
            sure.append(name)
    print("Checking " + str(len(unsure)) + " unsure accounts.")
    verified = get_bots_from_names(unsure)
    sure += verified

# Then recursively check accounts being followed by those
    print("Entering recursive bot search.")
    get_bots_recursive(sure)

# Save everything and exit
    save_json(queried, "output/queried.json")
    save_json(name_to_id, "output/name_to_id.json")
    save_json(id_to_name, "output/id_to_name.json")
    save_json(found_bots, "output/found_bots.json")
    save_json(bot_objects, "output/bot_objects.json")
    save_json(interactions, "output/interactions.json")
    save_gephi_csv(interactions, "output/interactions.csv")
    dump_list(found_bots, "output/bots.txt")

