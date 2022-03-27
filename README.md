# Some analysis of Lichess data

I am studying chess. I am reading some books and playing over the board, but most of the time
I am playing, solving puzzles and analyzing games on [Lichess](https://lichess.org). At this moment
there are more than 8000 games on my history there. I decided to check some things using the
[Lichess API](https://lichess.org/api). Perhaps this code can be useful for you too.  

## running the code

The code will be always divided into scripts which obtain data from *Lichss API* (and save it to */data*) and
scripts to plot different charts. So, if you run *player_games_charts.py* it will asume that there are *.csv*
files in */data* and a player's *.json* file in */config*.  
When you run *player_games_data.py* you need a *lichess.json* file in */config* which contains your api token.  

### lichess file
```
{
	"api_client": "berserk-downstream",
	"token": "No, I won't tell you my token.",
	"maxgames": 10000
}

```

### player's file
```
{
	"name": "Rodrigo Valla",
	"username": "rvalla",
	"start_year": 2021,
	"start_month": 9,
	"start_day": 1,
	"end_year": 2022,
	"end_month": 3,
	"end_day": 1,
	"previous_data" : true
}

```

## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Lichess**](https://lichss.org): the best place to learn and play chess.  
- [**Python**](https://www.python.org/): the programming language I used.  
- [**Berserk**](https://github.com/ZackClements/berserk): the client I used to comunicate with *Lichess API*.  

Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
