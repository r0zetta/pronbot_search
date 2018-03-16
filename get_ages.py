from time_helpers import *
from process_tweet_object import *
from graph_helper import *
from process_text import *
from file_helpers import *

from collections import Counter
from datetime import datetime, date, time, timedelta

import sys
import json
import os
import io
import re
import time

def make_count_ranges(count_data, range_max, num_ranges):
    range_step = range_max/num_ranges
    ranges = {}
    labels = []
    for x in range(num_ranges):
        start_range = x * range_step
        end_range = x * range_step + range_step
        label = "%.02f" % start_range + " - " + "%.02f" % end_range
        labels.append(label)
        ranges[label] = {}
        ranges[label]["start"] = start_range
        ranges[label]["end"] = end_range
    counts = Counter()
    for count in count_data:
        for l in labels:
            if count > ranges[l]["start"] and count < ranges[l]["end"]:
                counts[l] += 1
                break
    return labels, counts

def make_age_ranges(age_data, num_ranges=40):
    range_max = int(max(age_data))
    range_step = range_max/num_ranges
    ranges = {}
    labels = []
    for x in range(num_ranges):
        start_range = x * range_step
        end_range = x * range_step + range_step
        start_years = seconds_to_days(start_range)/365.0
        end_years = seconds_to_days(end_range)/365.0
        label = "%.02f" % start_years + " - " + "%.02f" % end_years + " years"
        labels.append(label)
        ranges[label] = {}
        ranges[label]["start"] = start_range
        ranges[label]["end"] = end_range
    counts = Counter()
    for age in age_data:
        for l in labels:
            if age > ranges[l]["start"] and age < ranges[l]["end"]:
                counts[l] += 1
                break
    return labels, counts

if __name__ == "__main__":

    print("Loading data")
    bot_objects = load_json("output/bot_objects.json")

    account_ages = []
    other_stuff = {}
    stuff_list = ["statuses_count", "followers_count", "friends_count", "favourites_count"]

    print("Getting account ages.")
    for id_str, obj in bot_objects.iteritems():
        if "created_at" in obj:
            account_age = seconds_since_twitter_time(obj["created_at"])
            account_ages.append(account_age)
        for s in stuff_list:
            if s in obj:
                if s not in other_stuff:
                    other_stuff[s] = []
                other_stuff[s].append(obj[s])

    print("Creating ranges.")
    account_ages = sorted(account_ages)
    labels, counts = make_age_ranges(account_ages)
    with open("output/age_ranges.txt", "w") as f:
        for l in labels:
            f.write(l + "," + str(counts[l]) + "\n")

    for s, d in other_stuff.iteritems():
        dataset = sorted(d)
        for rm in [500, 700, 1000, 1300, 2000]:
            labels, counts = make_count_ranges(dataset, rm, 40)
            filename = "output/" + s + "_ranges_" + str(rm) + ".txt"
            with open(filename, "w") as f:
                for l in labels:
                    f.write(l + "," + str(counts[l]) + "\n")

