# Midseason

We're ready for the FAL season! Let's get started!

## Setup

Each week we'll need to prepare the script to handle swaps, aces, wildcards, and other changes.

### `properties.py`

As you may have guessed, this file contains properties that the script will need in order to run. It is divided into two sections: properties that need to be set up just once and properties that need to change each week. The descriptions of the properties are straightfoward, and you can obtain their values from FAL staff.

### `aces.txt`

This file contains the aces for each team. FAL staff can help you determine what needs to be udpated.

### `wildcards.txt`

This file contains the wildcards that each team uses for this week. Similar to `aces.txt`, FAL staff can help you determine what needs to be updated in this file.

### `lists/name_changes.txt`

If a user changes their name midgame, then the old and new username needs to be written in this file in the following format:

>   `old_username new_username`

### `fansubsXX.txt`

Usually counted only on the fifth week, this file contains a list of anime and the number of regions in which it is simulcast. FAL staff can help you update this file.

### `fal.py`

This is the main script that gets run. Make sure that the only methods that get run are:

-   `scorer.main()`
-   `results.main()`
-   `details.main()`
-   `teams.banner_data()`

### `data/week_xx.zip`

These zip files contain the data from the previous weeks. You'll need these to make sure we can properly tally the scores. If another person has the data from a previous week, then you'll need to contact that person. It may help to upload the data to a mutually agreed place such as an FTP server or a Google Drive folder.

## Running the script

When you run `python fal.py`, the following files should be generated:

-   `scorer.main()` should output `week_xx.zip` in `data/` and `week_xx_errors.txt` in `results/`
-   `results.main()` should output `week_xx_results.txt` in `results/`
-   `details.main()` should output `week_xx_details.txt` in `results/`
-   `teams.banner_data()` should output `weekx.txt` in `bannerdata/`

With the exception of `bannerdata`, when an output file is written, it _cannot_ be overwritten. This is designed to prevent accidental loss of existing data in case the script is rerun to fix a mistake in the settings. To rerun the script to regenerate results, the already existing files need to be removed manually. Don't forget to remove old files or else they won't be overwritten and you'll still have the old broken results.

If you want to avoid retrieving new scores and instead reuse the existing data file from this week (`week_xx.zip`), then you in `fal.py` you can use `scorer.main(False)`, which should output `week_xx_new.zip` (instead of the usual `week_xx.zip`). After this is done you need to manually rename `week_xx_new.zip` to `week_xx.zip` (and optionally save the original `week_xx.zip` as a backup).

When you encounter errors while running the script, you'll need to fix them. Usually, they are errors related to extracting data from HTML with regular expressions (which is [a bad idea](http://stackoverflow.com/a/1732454/2073440) in general, but it gets the job done).

Here is an example error you might encounter:

```
Traceback (most recent call last):
  File "fal.py", line 20, in <module>
    scorer.main()
  File "src\scorer.py", line 695, in main
    score, new_posts, detailed_info, new_threads = get_score(a_id, a_info, week, httpconn)
  File "src\scorer.py", line 360, in get_score
    watching, completed, dropped, a_score, favorites = process_stats(a_id, a_info[0], httpconn)
  File "src\scorer.py", line 100, in process_stats
    score = re.search('Score:</span> ([\d\\.N/A]+)', response).group(1)
AttributeError: 'NoneType' object has no attribute 'group'
```

The above error says that the script is unable to obtain the score for an anime because the regular expression no longer matches the HTML. In this case, the HTML for the score changed to:

```html
<span class="dark_text">Score:</span>
  <span itemprop="ratingValue">N/A</span>
```

so the regular expression needs to be fixed to handle the new HTML.

Points for nuke-ups/nuke-downs change depending on the week. At the moment this needs to be changed in the code directly (scorer/results/details). Eventually this should be refactored to be handled outside of the code.

## After running the script

If the script is being run for the first time for a season, then you may want to extra careful and (have the FAL team assist you to) double-check the results to make sure everything looks okay.

If this script is being run for the first week, then you'll need to create a stickied thread for an overview of the results for the entire FAL season in the FAL forums [like this](http://myanimelist.net/forum/?topicid=1435288). This depends on a few things:

-   If you decide to host the `week_xx_details.txt` file on the FTP server, then you'll need to upload that file there as well. If not, then change the details link to point to wherever you decide to host the `week_xx_details.txt` file.
-   Each week you'll need to create a thread for the results in the MAL Contests forum (e.g. [this thread](http://myanimelist.net/forum/?topicid=1435295)). This thread should link to a different thread where users can obtain their banner, which will be explained below. Talk to FAL staff about the location of this banner thread.

## Banners

In addition to hosting the FAL contest itself, FAL staff allows teams to use banners on their profiles, signatures, blogs, and elsewhere on the Internet. Picked from a banner contest, these banners will automatically show each individual team's name and rank. Teams can customize them by changing the link to the banner.

In the past, MAL allowed users to use PHP links inside links. Now that PHP is disallowed, users need to submit a request for a banner. We will then generate banners for those users.

Here are the steps to generate banners:

0.  Make sure you have access to FTP server so that you can upload the banner results. If you need access, contact FAL staff.
1.  Make sure that `bannerdata/weekx.txt` is uploaded to FTP under the `data/` folder. The banner script needs this to generate the rankings on the banners.
2.  Visit the banners thread for the current season. For example, [this is the banner thread](http://myanimelist.net/forum/?topicid=1435306) for the Fall 2015 season. Take a note of which users have requested banners.
3.  Update `bannerdata/banners-input.txt` with any new requests.
4.  Run `python bannerdata/generatebanners.py`. This will call a PHP script that will generate the banners server-side.
5.  After this is done, make a post in the banners thread saying that all banners up to this point have been generated. This will serve as a bookmark for the next time you generate banners.
