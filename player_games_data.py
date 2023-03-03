import datetime as dt
import berserk as bk
import json as js
import pandas as pd

errors = [0,0,0] #ratings, evolution, games

log = open("log.md", "a") #preparing log file...
today = dt.date.today()
log.write("\n")
log.write("### %s"%today)
log.write(":" + "\n")

config = js.load(open("config/lichess.json"))
player = js.load(open("config/augusr.json"))

print("Let's get some data from " + player["name"] + "'s games...", end="\n")
print("Starting a lichess API client...", end="\r")

session = bk.TokenSession(config["token"])
client = bk.Client(session=session)

print("The API client is ready!        ", end="\n")

#preparing requested period...
start_date = dt.datetime(player["start_year"], player["start_month"], player["start_day"])
end_date = dt.datetime(player["end_year"], player["end_month"], player["end_day"])
start_date_m = bk.utils.to_millis(start_date)
end_date_m = bk.utils.to_millis(end_date)
period = pd.date_range(start_date, end_date - dt.timedelta(days=1))
period_index = period.format()

print("Obtaining games from lichess...", end="\r")

the_games = client.games.export_by_player(player["username"], rated=True, since=start_date_m, until=end_date_m, max=config["maxgames"], moves=True, opening=True)
games = list(the_games)

print("The games are ready!            ", end="\n")

#preparing dataframes...
ratings_columns = ["date", "id", "variant", "time","pre_rating","rating","difference","result","points","color",
					"opponent", "op_username", "op_difference", "moves_count", "moves", "opening"]
ratings_evolution_columns = ["bullet_min", "bullet_max", "bullet_mean",
							"blitz_min", "blitz_max", "blitz_mean",
							"rapid_min", "rapid_max", "rapid_mean"]
games_count_columns = ["bullet", "blitz", "rapid", "classical", "correspondence"]
if player["previous_data"]:
	past_ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
	past_ratings_evolution = pd.read_csv("data/" + player["username"] + "_ratings_evolution.csv", header=0, index_col=0)
	past_ratings_evolution.index_name = "date"
	past_games_count = pd.read_csv("data/" + player["username"] + "_games_count.csv", header=0, index_col=0)
	past_games_count.index_name = "date"
ratings = pd.DataFrame(index=range(len(games)), columns=ratings_columns)
ratings_evolution = pd.DataFrame(index=period_index, columns=ratings_evolution_columns)
ratings_evolution.index_name = "date"
games_count = pd.DataFrame(0,index=period_index, columns=games_count_columns)
games_count.index_name = "date"

def ratings_data(games):
	global errors
	for g in range(len(games)):
		print("I am processing ratings for game " + str(g), end="\r")
		moves = games[g]["moves"]
		if not moves == "":
			moves_count = round(len(moves.split(" "))/2)
			ratings.iloc[g]["moves_count"] = moves_count
			ratings.iloc[g]["moves"] = moves
			ratings.iloc[g]["id"] = games[g]["id"]
			ratings.iloc[g]["opening"] = games[g]["opening"]["eco"]
			ratings.iloc[g]["variant"] = games[g]["speed"]
			date = games[g]["createdAt"] + dt.timedelta(hours=player["timezone_diff"])
			ratings.iloc[g]["date"] = date.strftime("%Y-%m-%d")
			ratings.iloc[g]["time"] = date.strftime("%H:%M")
			if games[g]["players"]["white"]["user"]["name"] == player["username"]:
				ratings.iloc[g]["pre_rating"] = games[g]["players"]["white"]["rating"]
				ratings.iloc[g]["opponent"] = games[g]["players"]["black"]["rating"]
				ratings.iloc[g]["op_username"] = games[g]["players"]["black"]["user"]["name"]
				ratings.iloc[g]["color"] = "white"
				try:
					if games[g]["winner"] == "white":
						ratings.iloc[g]["result"] = "win"
						ratings.iloc[g]["points"] = 1
					elif games[g]["winner"] == "black":
						ratings.iloc[g]["result"] = "loss"
						ratings.iloc[g]["points"] = -1
				except:
					ratings.iloc[g]["result"] = "draw"
					ratings.iloc[g]["points"] = 0
				try:
					ratings.iloc[g]["difference"] = games[g]["players"]["white"]["ratingDiff"]
					ratings.iloc[g]["rating"] = ratings.iloc[g]["pre_rating"] + ratings.iloc[g]["difference"]
				except:
					ratings.iloc[g]["difference"] = 0
					errors[0] += 1
			else:
				ratings.iloc[g]["pre_rating"] = games[g]["players"]["black"]["rating"]
				ratings.iloc[g]["opponent"] = games[g]["players"]["white"]["rating"]
				ratings.iloc[g]["op_username"] = games[g]["players"]["white"]["user"]["name"]
				ratings.iloc[g]["color"] = "black"
				try:
					if games[g]["winner"] == "black":
						ratings.iloc[g]["result"] = "win"
						ratings.iloc[g]["points"] = 1
					elif games[g]["winner"] == "white":
						ratings.iloc[g]["result"] = "loss"
						ratings.iloc[g]["points"] = -1
				except:
					ratings.iloc[g]["result"] = "draw"
					ratings.iloc[g]["points"] = 0
				try:
					ratings.iloc[g]["difference"] = games[g]["players"]["black"]["ratingDiff"]
					ratings.iloc[g]["rating"] = ratings.iloc[g]["pre_rating"] + ratings.iloc[g]["difference"]
				except:
					ratings.iloc[g]["difference"] = 0
					errors[0] += 1
	ratings["op_difference"] = ratings["opponent"] - ratings["rating"]
	m = "-- Rankings evolution for " + player["name"] + " was analyzed..." + "\n"
	m += "   I noted " + str(errors[0]) + " errors this time." + "\n"
	log.write(m)
	print("All ratings have been processed!                  ", end="\n")
	print("I noted " + str(errors[0]) + " errors this time...", end="\n")

def get_ratings_evolution():
	global errors
	print("Let's check how rankings evolved...", end="\r")
	for d in period:
		key = d.strftime("%Y-%m-%d")
		played_at_date = ratings[ratings["date"] == key]
		played_bullet = played_at_date[played_at_date["variant"] == "bullet"]
		ratings_evolution.loc[key]["bullet_min"] = played_bullet["rating"].min()
		ratings_evolution.loc[key]["bullet_max"] = played_bullet["rating"].max()
		ratings_evolution.loc[key]["bullet_mean"] = played_bullet["rating"].mean()
		played_blitz = played_at_date[played_at_date["variant"] == "blitz"]
		ratings_evolution.loc[key]["blitz_min"] = played_blitz["rating"].min()
		ratings_evolution.loc[key]["blitz_max"] = played_blitz["rating"].max()
		ratings_evolution.loc[key]["blitz_mean"] = played_blitz["rating"].mean()
		played_rapid = played_at_date[played_at_date["variant"] == "rapid"]
		ratings_evolution.loc[key]["rapid_min"] = played_rapid["rating"].min()
		ratings_evolution.loc[key]["rapid_max"] = played_rapid["rating"].max()
		ratings_evolution.loc[key]["rapid_mean"] = played_rapid["rating"].mean()
	m = "-- " + player["name"] + "'s ratings evolution was analysed..." + "\n"
	log.write(m)
	print("I finished rankings evolution analysis!        ", end="\n")

def games_played():
	global errors
	print("I am counting games now...", end="\r")
	for g in range(len(games)):
		if ratings.iloc[g]["variant"] == "bullet":
			games_count.loc[ratings.iloc[g]["date"]]["bullet"] += 1
		elif ratings.iloc[g]["variant"] == "blitz":
			games_count.loc[ratings.iloc[g]["date"]]["blitz"] += 1
		elif ratings.iloc[g]["variant"] == "rapid":
			games_count.loc[ratings.iloc[g]["date"]]["rapid"] += 1
		elif ratings.iloc[g]["variant"] == "classical":
			games_count.loc[ratings.iloc[g]["date"]]["classical"] += 1
		elif ratings.iloc[g]["variant"] == "correspondence":
			games_count.loc[ratings.iloc[g]["date"]]["correspondence"] += 1
	m = "-- " + player["name"] + "'s games were counted..." + "\n"
	log.write(m)
	print("I counted all games!        ", end="\n")

ratings_data(games)
get_ratings_evolution()
games_played()

#closing log file...
log.write("\n")
log.close()

#ready to concat and save files...
print("Saving files to /data...", end="\r")
if player["previous_data"]:
	all_ratings = pd.concat([past_ratings, ratings], names=ratings_columns, ignore_index=True)
	all_evolution = pd.concat([past_ratings_evolution, ratings_evolution], names=ratings_evolution_columns)
	all_games_count = pd.concat([past_games_count, games_count], names=games_count_columns)
else:
	all_ratings = ratings
	all_evolution = ratings_evolution
	all_games_count = games_count
all_ratings.dropna(how='all', inplace=True) 
all_ratings.sort_values(by=["date","time"], axis=0, inplace=True)
all_ratings.to_csv("data/" + player["username"] + "_ratings_history.csv", index=False)
all_evolution.to_csv("data/" + player["username"] + "_ratings_evolution.csv")
all_games_count.to_csv("data/" + player["username"] + "_games_count.csv")
print("All files saved!          ", end="\n")

print("My work has ended...                          ", end="\n")
print("I processed a total of " + str(len(games)) + " games!", end="\n")
