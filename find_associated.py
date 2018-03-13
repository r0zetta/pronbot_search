from file_helpers import *
import requests
import json
import io
import os
import re
import sys
import shutil

if __name__ == "__main__":
    query = ""
    if (len(sys.argv) > 1):
        query = sys.argv[1]

    associations = load_json("output/interactions.json")
    found = []
    for source, target in associations.iteritems():
        if query.lower() in source.lower():
            for t in target:
                found.append(t)
        else:
            if query.lower() in [t.lower() for t in target]:
                found.append(source)

    for f in found:
        print f

