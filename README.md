# Fantasy Anime League Engine

## Requirements

* [git-secret](https://git-secret.io/)

  * be sure to run `git secret reveal` after checking out master to decrypt files containing private keys for development
  * you may also need to run `git secret tell <your@email.com>` before being able to decrypt them

## Some general remarks

I wrote this script in a rush when I didn't have a lot of experience with python/programming. I wanted to do it object oriented from the start but for some reason this didn't work (got weird error messages). So I decided to just go with dictionaries. With new features I expanded these so they look pretty ugly now (especially the anime dictionary). I think to make the code much clearer it should be object oriented. Unfortunately I never had the time to do this myself.

The data structure of the anime dictionary (for each week) is like this at the moment:

```python
anime = {anime ID : title, [all_posts, new_posts], team count, [watch, compl, drop, score, favs], [all_threads, new_threads], [[simulcasts], simulcast_score], license]}
```

I tried to clean up the code as much as possible and also added some more comments. There are some things that still need to be fixed (see this file or my comments in the code). Though it might just make more sense to rewrite most of it (or all of it).

As said before, the whitelisted user-agent key can't be made public, otherwise other people will grab it for themselves, use it too much and the key will be blocked. It is very hard to get a blocked key unblocked or to get a new key, so this problem must be prevented. If there are ever any problems with the key please contact Xinil directly (since he gets lots of PMs from users it might be better if Naru or another mod he knows contacts him).

## Before the season starts

You can use `src/collect_series.py` to get a list of ID-title pairs. To get a new url go to the advanced search, then search for type "tv", start date is month and year of when the season starts. Make sure you select start date as displayed column, then search.

Note: The list will also contain series that air only later, so you need to remove them from the results. This should still be faster than manually collecting ID+title pairs.

`anime_list.txt` goes into the `lists` folder then.

## Registration

`team.py` has all functions for the registration (including the functions to generate statistics).

To use the functions in it use the main file `fal.py`

`registration.txt` needs to be in the home folder (not src). `team.py` generates a team list which will first be in the home folder as well. Only AFTER the registration is closed move this `team_list.txt` to the `lists` folder.

IMPORTANT NOTE: There need to be 1-2 newlines in `registration.txt` after the last team block, otherwise it won't recognize the last team. I never got around to fix this in the script.

All statistics are automatically generated into the `lists` folder.

If there's a restriction for sequels then you can write the restricted sequels in `lists/sequels.txt` and the script will automatically recognize if people have too many sequels in their team.

After the registration is closed run `src/check_usernames.py`

This will show you if there are errors in the usernames.

IMPORTANT NOTE: Usernames are case-sensitive. If they are wrong in the registration then there will be problems later with aces, wildcards and swaps! It's very hard to fix this after week 1 so best to check before week 1 and just run the registration again with the fixed names.

You can use the functions `team_stats` and `team_dist` to create statistics for the team list thread.

In `properties.py` you can set all properties for the current week (first half) AND the overall event (second half).

Make sure you don't forget to change the variables that need to be changed like additional points (in case the rules changed) or double_watching (this is different every season depending on how many players participate).

Change the thread ID for points criteria in `results.py` to the Rules thread of the current season.

The following folders need to be empty (make a backup of the data from last season somewhere else):

* `bannerdata`
* `data`
* `results`

Some series air before FAL starts. We don't treat watching etc. special so you can just count these stats as for any other series. But we subtract all forum posts that the series got BEFORE week 1. This means before week 1 starts the FAL staff needs to check all series and make a list of series that started early and how many posts they have. These posts are currently subtracted in the `scorer.py` (where forum posts are retrieved from the sub-boards). It's better to move this part to the properties or somewhere else so it's better accessible and won't be forgotten to be done.

## During the game

Weekly preparation (shortly after the deadline):

* Change the weekly properties in `properties.py`
* Get all aces from the google doc and put them in `aces.txt`
* Get all wildcards from the google doc and put them in `wildcards.txt`

The main file to run the script is `fal.py`

Running the script and generating the results:

* `scorer.main()` --> output `week_xx.zip` in `data/` and `week_xx_errors.txt` in `results/`
* `results.main()` --> output `week_xx_results.txt` in `results/`
* `details.main()` --> output `week_xx_details.txt` in `results/`
* `teams.banner_data()` --> output `weekx.txt` in `bannerdata/`

I made it so that once an output file is written, it CANNOT be overwritten (except for `bannerdata`). This should prevent accidental loss of existing data in case the script is run again and a mistake was made in the settings etc. To run the script again and generate results again, the already existing files need to be removed manually.

If there's a problem with the script and it stops running before creating data/results, the error file still needs to be removed manually.

It is possible to use existing data to fix errors like a missing ace. (Though generally it is just easier to run the entire thing again with the missing ace, if it's not too long after the deadline the numbers will probably not change a lot.)

In this case you need to add the False parameter to the scorer main function in `fal.py`:

> `scorer.main(False)`

If this is run, it will take the existing data file from this week (`week_xx.zip`), and save a corrected data file as `week_xx_new.zip`

After this is done you need to manually rename `week_xx_new.zip` to `week_xx.zip` (best to save the original `week_xx.zip` as a backup).

Only after this is renaming done you can run `results.main()`, `details.main()`, and `teams.banner_data()` again. Don't forget to remove old files or else they won't be overwritten and you'll still have the old broken results.

Points for nuke-ups/nuke-downs change depending on the week. At the moment this needs to be changed in the code directly (scorer/results/details). Should be done with a variable in properties.

If a user changes his name then the old and new username needs to be written in `lists/name_changes.txt` in the format:

> `old_username new_username`
