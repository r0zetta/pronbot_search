from file_helpers import *

import sys
import json
import os
import io
import re

if __name__ == "__main__":

    name_to_id = load_json("output/name_to_id.json")

    id_to_name = {}
    for name, id_str in name_to_id.iteritems():
        id_to_name[id_str] = name
    save_json(id_to_name, "output/id_to_name.json")

