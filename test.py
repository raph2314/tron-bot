#!/usr/bin/env python3

import json
from parser import Game

with open('test.json') as f:
    data = json.loads(f)

print(data)
