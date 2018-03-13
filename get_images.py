from file_helpers import *
import requests
import json
import io
import os
import re
import sys
import shutil

def dump_images(image_urls, dirname):
    for id_str, p in image_urls.iteritems():
        filename = id_str + ".jpg"
        save_path = os.path.join(dirname, filename)
        if not os.path.exists(save_path):
            print("Getting picture from: " + p)
            response = requests.get(p, stream=True)
            with open(save_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

if __name__ == "__main__":
    save_dir = "images"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    images = {}
    all_data = load_json("output/bot_objects.json")
    for id_str, d in all_data.iteritems():
        if "profile_image_url" in d:
            image = d["profile_image_url"]
            images[id_str] = image
        if "profile_image_url_https" in d:
            image = d["profile_image_url_https"]
            images[id_str] = image
    dump_images(images, save_dir)
