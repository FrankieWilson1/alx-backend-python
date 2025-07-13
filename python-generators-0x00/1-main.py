#!/usr/bin/python3
from itertools import islice
stream_users_modules = __import__('0-stream_users')

stream_users_function = stream_users_modules.stream_users

# iterate over the generator function and print only the first 6 rows

for user in islice(stream_users_function(), 6):
    print(user)