#!/usr/bin/python3.7

import jikanpy

import re
import time
import configparser

jikan = jikanpy.Jikan()


def check(name):
    """Check if the profile exists based on the name"""
    print(name)

    try:
        user = jikan.user(name)
        assert name.lower() == user["username"].lower()
    except jikanpy.exceptions.APIException:
        print(f"username doesn't exist anymore: {name}")


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    f_name = "lists/team_headcount.txt"
    names = re.findall(r"\[b\](.+?)\[/b\]\n", open(f_name).read())

    for name in names:
        check(name)
        time.sleep(config.getint('jikanpy', 'request-interval'))


if __name__ == "__main__":
    main()
