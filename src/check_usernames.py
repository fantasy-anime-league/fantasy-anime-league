#!/usr/bin/python3.7

import re
import time
import jikanpy

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
    f_name = "lists/team_headcount.txt"
    names = re.findall(r"\[b\](.+?)\[/b\]\n", open(f_name).read())

    for name in names:
        check(name)
        time.sleep(3)


if __name__ == "__main__":
    main()
