# Preseason

During this stage, there two important things to handle: anime list compilation and team registration.

## Anime list compilation

### Prerequisites

Before we begin, we need the following:

1.  [Python 2.7+](https://www.python.org/downloads/)
2.  The month and year of the start of the current anime season. These are used in the MAL Advanced Search; we will run a script to retrieve its results.

### Compilation process

We will run a script to retrieve the results from MAL's Advanced Search. To generate the list of anime for the current season:

1.  Make sure you know the month and year of the current anime season
2.  View the Advanced Search page
    1.  View the [Anime Search](http://myanimelist.net/anime.php) page
    2.  Click Advanced Search
3.  Using the following settings for MAL's advanced search:
    -   Type: "TV"
    -   Start Date: month and year of the start of the season
    -   Columns: Start Date
4.  Click Search Anime
5.  Navigate to the next page of results
6.  Copy and paste the URL into `MAL_ADVANCED_SEARCH_URL` in `src/collect_series.py`
7.  Replace `show=<number>` with `show=%i`
8.  Run `python collect_series.py`

After these steps are done, you should find the files `series.txt` and `series_sorted.txt` in the folder where `collect_series.py` is located. You may need to fix the entries in those files to remove shows from future seasons and restore missing punctuation marks.

## Team registration

Throughout the registration period, we need to pay attention to three important documents:

1.  **Accepted Registrations:** This Google doc contains a list of currently accepted teams. If multiple people are performing registrations, then it is important that this document be kept updated.
2.  **Registrations, Errors, Username Changes, PMs Sent:** This Google doc contains various bits of information, outlined below.
    -   _Registrations:_ This is the list of teams that have yet to be registered.
    -   _Errors:_ This is a list of teams that have errors in their registration. FAL staff will handle contacting these teams to fix their errors.
    -   _Username Changes:_ This is a list of people who have changed their usernames. This is only important when the season begins.
    -   _PMs Sent:_ This is a record of PMs sent to teams regarding registration errors and late (re-)registrations.
3.  **Team Headcount:** This MAL thread contains the public list of teams that have been registered.

It is important that teams be registered regularly. People will be checking the team headcount thread to see if their teams are in, and they will become worried if they don't see their teams on that list.

### Prerequisites

These tasks need to be set up just once.

1.  The **Accepted Registrations** document; **Registrations, Errors, Username Changes, PMs Sent** document; and the **Team Headcount** thread need to be created. The first two will usually be handled by FAL staff. The Team Headcount thread needs to be posted and sticked to the [forum for the FAL club](http://myanimelist.net/forum/?clubid=379).
2.  Update `lists/anime_list.txt` with the contents of `series.txt` obtained from the anime compliation process.
3.  Update `lists/sequels.txt` with the sequels for the current season. Ask FAL staff to see which series should be in this file.
4.  In `fal.py` below the import statements, comment out all lines except `teams.create_teams` and `teams.headcount`. Update `teams.headcount` to the current anime season.

### Registration process

These steps will need to be done each time you begin to process team registration.

1.  Copy the contents of the **Accepted Registrations** document into `registration.txt`, which should be located in the project root directory. This needs to be done to sync your `registration.txt` with that generated from other FAL developers. If this step isn't done, then we risk omitting registrations done by other people.

    _Note:_ If you are the sole person responsible for registering teams, then you don't need to worry about this step.

2.  Append the pending team registrations in the **Registrations, Errors, Username Changes, PMs Sent** document to `registration.txt`. Make sure that `registration.txt` ends with two newlines; otherwise, the registration script won't parse the teams properly.
3.  Run `python fal.py`. If there is no error, then this should output three files:
    1.  `team_list.txt`, which will eventually replace `lists/team_list.txt` when registrations are closed
    2.  `lists/team_headcount.txt`, the BBCode that should be pasted into the **Team Headcount** thread
    3.  `lists/teams.obj`, a serialized representation of the registered teams

    If there are errors, then please correct them before rerunning `python fal.py`.
4.  Update the **Accepted Registrations** document with the contents of `registration.txt`.
5.  Update the **Team Headcount** thread with the contents of `lists/team_headcount.txt`.
6.  Update the last accepted team (the last team listed in `registrations.txt`) at the top of the **Registrations, Errors, Username Changes, PMs Sent** document.

## Close of team registration

When we no longer accept team registrations for the current season, we need to tidy up a few things and generate the team statistics to post on the MAL Contests board.

1.  Unsticky the **Team Headcount** thread.
2.  Replace `lists/team_list.txt` with the `team_list.txt` generated from the registration process.
3.  In `fal.py` below the import statements, comment out all lines except `teams.team_overview()`, `teams.team_stats(True)`, and `teams.team_dist(True)`.
4.  Run `python fal.py`. This should output the following files:
    -   `lists/team_overview.txt`, an overview of all the teams that have been registered for this season
    -   `lists/team_stats.txt`, which lists the series for this season and the number of teams who have them in their bench
    -   `lists/team_dist.txt`, which contains statistics about team composition
5.  Create a stickied thread in the [MAL Contests forum](http://myanimelist.net/forum/?board=13) called "FAL `<season>` `<year>` Team List" (replacing `season` and `year`). It will have three posts:
    1.  An announcement that registration is closed, the first half of the teams from `lists/team_overview.txt`, and a warning to users to report mistakes to FALbot before a certain time.
    2.  The second half of the teams from `lists/team_overview.txt`.
    3.  The statistics from `lists/team_stats.txt` and `lists/team_dist.txt`.

    For reference on what this thread should look like, please see the [FAL Spring 2015 Team List](http://myanimelist.net/forum/?topicid=1367256) thread.
