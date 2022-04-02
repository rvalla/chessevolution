import datetime as dt
import json as js
import pandas as pd

log = open("log.md", "a") #preparing log file...
today = dt.date.today()
log.write("\n")
log.write("### %s"%today)
log.write(":" + "\n")

player = js.load(open("config/augusr.json"))

print("Let's analyze some data from " + player["name"] + "'s games...", end="\n")

ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
ratings_evolution = pd.read_csv("data/" + player["username"] + "_ratings_evolution.csv", header=0, index_col=0)
ratings_evolution.index_name = "date"
games_count = pd.read_csv("data/" + player["username"] + "_games.csv", header=0, index_col=0)
games_count.index_name = "date"

print("The data were loaded!", end="\n")

#preparing dataframes...
hours_index = ["00","01","02","03","04","05","06","07","08","09","10","11","12",
				"13","14","15","16","17","18","19","20","21","22","23"]
hours_columns = ["bullet_g", "bullet_w", "bullet_d", "bullet_l", "bullet_res", "bullet_diff", "bullet_diff_avg",
				"blitz_g", "blitz_w", "blitz_d", "blitz_l", "blitz_res", "blitz_diff", "blitz_diff_avg",
				"rapid_g", "rapid_w", "rapid_d", "rapid_l", "rapid_res", "rapid_diff", "rapid_diff_avg",
				"_g", "_w", "_d", "_l", "_res", "_diff", "_diff_avg"]
hours = pd.DataFrame(0, index=hours_index, columns=hours_columns)

def analyze_day_time():
	for g in range(ratings.shape[0]):
		print("I am analyzing game " + str(g), end="\r")
		key = None
		variant = ratings.iloc[g]["variant"]
		if variant == "bullet" or variant == "blitz" or variant == "rapid":
			time = ratings.iloc[g]["time"].split(":")[0]
			result = ratings.iloc[g]["points"]
			hours.loc[time][variant + "_g"] += 1
			hours.loc[time][variant + "_res"] += result
			hours.loc[time][variant + "_diff"] += ratings.iloc[g]["difference"]
			if result == 1:
				hours.loc[time][variant + "_w"] += 1
			elif result == -1:
				hours.loc[time][variant + "_l"] += 1
			else:
				hours.loc[time][variant + "_d"] += 1
	hours["bullet_diff_avg"] = hours["bullet_diff"] / hours["bullet_g"]
	hours["blitz_diff_avg"] = hours["blitz_diff"] / hours["blitz_g"]
	hours["rapid_diff_avg"] = hours["rapid_diff"] / hours["rapid_g"]
	hours["_g"] = hours["bullet_g"] + hours["blitz_g"] + hours["rapid_g"]
	hours["_w"] = hours["bullet_w"] + hours["blitz_w"] + hours["rapid_w"]
	hours["_d"] = hours["bullet_d"] + hours["blitz_d"] + hours["rapid_d"]
	hours["_l"] = hours["bullet_l"] + hours["blitz_l"] + hours["rapid_l"]
	hours["_res"] = hours["bullet_res"] + hours["blitz_res"] + hours["rapid_res"]
	hours["_diff"] = hours["bullet_diff"] + hours["blitz_diff"] + hours["rapid_diff"]
	hours["_diff_avg"] = (hours["bullet_diff"] + hours["blitz_diff"] + hours["rapid_diff"]) / 3

analyze_day_time()
hours.to_csv("data/" + player["username"] + "_time_analysis.csv", index=True, index_label="hours")

log.write("-- Analyzing games time performance for " + player["name"] + "\n")
log.close()

print("All files saved!          ", end="\n")

print("My work has ended...                          ", end="\n")
