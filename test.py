#!/usr/bin/env python3

import json


with open('test.json') as f:
    data = json.loads(f)

print(data)
