from time_helpers import *
from alphabet_detector import AlphabetDetector
import re

def is_bot_name(name):
    ret = True
    if re.search("^([A-Z]?[a-z]{1,})?[\_]?([A-Z]?[a-z]{1,})?[\_]?[0-9]{,9}$", name):
        ret = False
    if re.search("^[\_]{,3}[A-Z]{2,}[\_]{,3}$", name):
        ret = False
    if re.search("^[A-Z]{2}[a-z]{2,}$", name):
        ret = False
    if re.search("^([A-Z][a-z]{1,}){3}[0-9]?$", name):
        ret = False
    if re.search("^[A-Z]{1,}[a-z]{1,}[A-Z]{1,}$", name):
        ret = False
    if re.search("^[A-Z]{1,}[a-z]{1,}$", name):
        ret = False
    if re.search("^([A-Z]?[a-z]{1,}[\_]{1,}){1,}[A-Z]?[a-z]{1,}$", name):
        ret = False
    if re.search("^[A-Z]{1,}[a-z]{1,}[\_][A-Z][\_][A-Z]{1,}[a-z]{1,}$", name):
        ret = False
    if re.search("^[a-z]{1,}[A-Z][a-z]{1,}[A-Z][a-z]{1,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{1,}[A-Z][a-z]{1,}[A-Z]{1,}$", name):
        ret = False
    if re.search("^([A-Z][\_]){1,}[A-Z][a-z]{1,}$", name):
        ret = False
    if re.search("^[\_][A-Z][a-z]{1,}[\_][A-Z][a-z]{1,}[\_]?$", name):
        ret = False
    if re.search("^[A-Z][a-z]{1,}[\_][A-Z][\_][A-Z]$", name):
        ret = False
    if re.search("^[A-Z][a-z]{2,}[0-9][A-Z][a-z]{2,}$", name):
        ret = False
    if re.search("^[A-Z]{1,}[0-9]?$", name):
        ret = False
    if re.search("^[A-Z][a-z]{1,}[\_][A-Z]$", name):
        ret = False
    if re.search("^[A-Z][a-z]{1,}[A-Z]{2}[a-z]{1,}$", name):
        ret = False
    if re.search("^[\_]{1,}[a-z]{2,}[\_]{1,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{2,}[\_][A-Z][a-z]{2,}[\_][A-Z]$", name):
        ret = False
    if re.search("^[A-Z]?[a-z]{2,}[0-9]{2}[\_]?[A-Z]?[a-z]{2,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{2,}[A-Z]{1,}[0-9]{,2}$", name):
        ret = False
    if re.search("^[\_][A-Z][a-z]{2,}[A-Z][a-z]{2,}[\_]$", name):
        ret = False
    if re.search("^([A-Z][a-z]{1,}){2,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{2,}[\_][A-Z]{2}$", name):
        ret = False
    if re.search("^[a-z]{3,}[0-9][a-z]{3,}$", name):
        ret = False
    if re.search("^[a-z]{4,}[A-Z]{1,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{3,}[A-Z][0-9]{,9}$", name):
        ret = False
    if re.search("^[A-Z]{2,}[\_][A-Z][a-z]{3,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{3,}[A-Z]{1,3}[a-z]{3,}$", name):
        ret = False
    if re.search("^[A-Z]{3,}[a-z]{3,}[0-9]?$", name):
        ret = False
    if re.search("^[A-Z]?[a-z]{3,}[\_]+$", name):
        ret = False
    if re.search("^[A-Z][a-z]{3,}[\_][a-z]{3,}[\_][A-Za-z]{1,}$", name):
        ret = False
    if re.search("^[A-Z]{2,}[a-z]{3,}[A-Z][a-z]{3,}$", name):
        ret = False
    if re.search("^[A-Z][a-z]{2,}[A-Z][a-z]{3,}[\_]?[A-Z]{1,}$", name):
        ret = False
    if re.search("^[A-Z]{4,}[0-9]{2,9}$", name):
        ret = False
    if re.search("^[A-Z]{1,2}[a-z]{3,}[A-Z]{1,2}[a-z]{3,}[0-9]{1,9}$", name):
        ret = False
    if re.search("^[A-Z]+[a-z]{3,}[0-9]{1,9}$", name):
        ret = False
    if re.search("^([A-Z]?[a-z]{2,})+[0-9]{1,9}$", name):
        ret = False
    if re.search("^([A-Z]?[a-z]{2,})+\_?[a-z]+$", name):
        ret = False
    return ret

def get_screen_name(status):
    if "user" in status:
        user_data = status["user"]
        if "screen_name" in user_data:
            return user_data["screen_name"]

def get_mentioned(status):
    mentioned = []
    if "entities" in status:
        entities = status["entities"]
        if "user_mentions" in entities:
            for item in entities["user_mentions"]:
                if item is not None:
                    mention = item['screen_name']
                    if mention is not None:
                        if mention not in mentioned:
                            mentioned.append(mention)
    if len(mentioned) > 0:
        return mentioned

def get_quoted(status):
    if "quoted_status" in status:
        orig_tweet = status["quoted_status"]
        if "user" in orig_tweet:
            if orig_tweet["user"] is not None:
                user = orig_tweet["user"]
                if "screen_name" in user:
                    if user["screen_name"] is not None:
                            return user["screen_name"]

def get_retweeted(status):
    if "retweeted_status" in status:
        orig_tweet = status["retweeted_status"]
        if "user" in orig_tweet:
            if orig_tweet["user"] is not None:
                user = orig_tweet["user"]
                if "screen_name" in user:
                    if user["screen_name"] is not None:
                        return user["screen_name"]

def get_replied(status):
    if "in_reply_to_screen_name" in status:
        if status["in_reply_to_screen_name"] is not None:
            return status["in_reply_to_screen_name"]

def get_interactions(status):
    interactions = set()
    screen_name = get_screen_name(status)
    if screen_name is None:
        return
    mentioned = get_mentioned(status)
    if mentioned is not None:
        for m in mentioned:
            interactions.add(m)
    quoted = get_quoted(status)
    if quoted is not None:
        interactions.add(quoted)
    retweeted = get_retweeted(status)
    if retweeted is not None:
        interactions.add(retweeted)
    replied = get_replied(status)
    if replied is not None:
        interactions.add(replied)
    interactions = [x.lower() for x in interactions]
    return interactions

def get_hashtags(status):
    hashtags = []
    if "entities" in status:
        entities = status["entities"]
        if "hashtags" in entities:
            for item in entities["hashtags"]:
                if item is not None:
                    if "text" in item:
                        tag = item['text']
                        if tag is not None:
                            if tag not in hashtags:
                                hashtags.append(tag.lower())
    hashtags = [x.lower() for x in hashtags]
    return hashtags

def get_urls(status):
    ret = []
    if "entities" in status:
        entities = status["entities"]
        if "urls" in entities:
            for item in entities["urls"]:
                if item is not None:
                    if "expanded_url" in item:
                        url = item['expanded_url']
                        if url is not None:
                            if url not in ret:
                                ret.append(url)
    return ret

def get_image_urls(status):
    ret = []
    if "entities" in status:
        entities = status["entities"]
        if "media" in entities:
            for item in entities["media"]:
                if item is not None:
                    if "media_url" in item:
                        url = item['media_url']
                        if url is not None:
                            if url not in ret:
                                ret.append(url)
    return ret

def get_text(status):
    if "full_text" in status:
        return status["full_text"]
    if "text" in status:
        return status["text"]

def is_egg(status):
    if "user" in status:
        user = status["user"]
        if "default_profile" in user and user["default_profile"] is not None:
            if user["default_profile"] == False:
                return False
        if "default_profile_image" in user and user["default_profile_image"] is not None:
            if user["default_profile_image"] == False:
                return False
    return True

def get_account_age_days(status):
    ret = 0
    if "user" in status:
        user = status["user"]
        created_at = user["created_at"]
        ret = seconds_to_days(seconds_since_twitter_time(created_at))
    return ret

def get_tweet_count(status):
    ret = 0
    if "user" in status:
        user = status["user"]
        ret = user["statuses_count"]
    return ret

def get_tweets_per_day(status):
    ret = 0
    account_age_days = get_account_age_days(status)
    num_tweets = get_tweet_count(status)
    if account_age_days > 0 and num_tweets > 0:
        ret = account_age_days / float(num_tweets)
    return ret

def get_friends_count(status):
    ret = 0
    if "user" in status:
        user = status["user"]
        if "friends_count" in user:
            ret = user["friends_count"]
    return ret

def get_profile_image_url(status):
    if "user" in status:
        user = status["user"]
        if "profile_image_url" in user:
            return user["profile_image_url"]

def get_user_id(status):
    if "user" in status:
        user = status["user"]
        if "id_str" in user:
            return user["id_str"]

def get_followers_count(status):
    ret = 0
    if "user" in status:
        user = status["user"]
        if "followers_count" in user:
            ret = user["followers_count"]
    return ret

def is_new_account_bot(status):
    ret = False
    ad = AlphabetDetector()
    susp_score = 0
    egg = is_egg(status)
    if "user" not in status:
        return
    user = status["user"]
    sn = user["screen_name"]
    n = user["name"]
    bot_name = is_bot_name(sn)
    tweets = user["statuses_count"]
    friends = user["friends_count"]
    followers = user["followers_count"]
    created_at = user["created_at"]
    location = user["location"]
    time_obj = twitter_time_to_object(created_at)
    created_year = int(time_obj.strftime("%Y"))
    if egg == True:
        susp_score += 50
    if bot_name == True:
        susp_score += 100
    if created_year < 2017:
        susp_score -= 300
    if len(location) > 0:
        susp_score -= 150
    if len(sn) == 15:
        susp_score += 100
    if tweets == 0:
        susp_score += 50
    if tweets > 0:
        susp_score -= 50
    if tweets > 20:
        susp_score -= 100
    if friends == 21:
        susp_score += 100
    if friends == 0:
        susp_score += 50
    if friends != 21:
        susp_score -= 50
    if friends > 40:
        susp_score -= 100
    if friends > 100:
        susp_score -= 100
    if followers == 0:
        susp_score += 50
    if followers > 0:
        susp_score -= 200
    if len(n) < 3:
        susp_score += 100
    if ad.only_alphabet_chars(n, "CYRILLIC"):
        susp_score += 200
    if ad.only_alphabet_chars(n, "ARABIC"):
        susp_score += 200
    if ad.is_cjk(n):
        susp_score += 200
    if ad.only_alphabet_chars(n, "LATIN"):
        susp_score -= 100
    if susp_score > 0:
        return True
    else:
        return False
