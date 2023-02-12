# Some analysis of Lichess data: data

In this folder the output files are saved. All filenames starts with the *lichess username*. Let's see
which data are stored in each file.  

## username_ratings_history.csv

The bigger file of the database. All rated downloaded games. Each line store a game with this data:

- date
- id (to look the game at lichess.org/id)
- variant (bullet, blitz...)
- time (time of the day hh:mm)
- pre_rating (player's rating when the game started)
- rating (player's rating when the game ended)
- difference (pre_rating - rating)
- result
- points (-1, 0, 1)
- color (player's color)
- opponent (opponent's rating)
- op_username (opponent's username)
- op_difference (player's rating - opponent's rating)
- moves_count (number of moves)
- moves (a string of all moves)
- opening (ECO code)

## username_ratings_evolution.csv

A file that stores the ratings data by date. Note that the fields are empty when the player
didn't play a game in certain variant. Each line store a date with this data:

- bullet_min (minumun bullet ranking of the day)
- bullet_max (yes, the maximum)
- bullet_mean (exactly, the mean value for the day)
- blitz_min
- blitz_max
- blitz_mean
- rapid_min
- rapid_max
- rapid_mean

## username_games_count.csv

A file that simply saves the number of games played by date.  

## username_time_analysis.csv

A file that stores game results information by time of the day.

## username_expected_result.csv and username_expected_result_diff.csv

A file that estimates, based on database results, the expected result of a game between the player and
a certain rating opponent.  

Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).