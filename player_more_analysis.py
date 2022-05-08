import datetime as dt
import json as js
import pandas as pd

log = open("log.md", "a") #preparing log file...
today = dt.date.today()
log.write("\n")
log.write("### %s"%today)
log.write(":" + "\n")

player = js.load(open("config/rvalla.json"))

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
expected_result_columns = ["bullet_g", "bullet_r", "bullet_p", "blitz_g", "blitz_r", "blitz_p",
							"rapid_g", "rapid_r", "rapid_p"]
expected_result = pd.DataFrame(0, index=[500 + x * 20 for x in range(116)], columns=expected_result_columns)
expected_result_diff = pd.DataFrame(0, index=[-1500 + x * 20 for x in range(151)], columns=expected_result_columns)

def analyze_day_time():
	for g in range(ratings.shape[0]):
		print("I am analyzing game " + str(g), end="\r")
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
	print("I finished analyzing day times...                    ", end="\n")

analyze_day_time()
hours.to_csv("data/" + player["username"] + "_time_analysis.csv", index=True, index_label="hours")
log.write("-- Analyzing games time performance for " + player["name"] + "\n")

def get_expected_rows(opponent, difference):
	r = opponent // 20 - 25
	rd = (difference + 10) // 20 + 75
	return [int(r), int(rd)]

def get_expected_results():
	for g in range(ratings.shape[0]):
		print("I am analyzing expected results. Game: " + str(g), end="\r")
		rows = get_expected_rows(ratings.iloc[g]["opponent"], ratings.iloc[g]["op_difference"])
		variant = ratings.iloc[g]["variant"]
		if variant == "bullet" or variant == "blitz" or variant == "rapid":
			result = ratings.iloc[g]["points"] + 1
			expected_result.iloc[rows[0]][variant + "_g"] += 1
			expected_result.iloc[rows[0]][variant + "_r"] += result
			expected_result_diff.iloc[rows[1]][variant + "_g"] += 1
			expected_result_diff.iloc[rows[1]][variant + "_r"] += result
	expected_result["bullet_p"] = (expected_result["bullet_r"] / expected_result["bullet_g"]) / 2
	expected_result["blitz_p"] = (expected_result["blitz_r"] / expected_result["blitz_g"]) / 2
	expected_result["rapid_p"] = (expected_result["rapid_r"] / expected_result["rapid_g"]) / 2
	expected_result_diff["bullet_p"] = (expected_result_diff["bullet_r"] / expected_result_diff["bullet_g"]) / 2
	expected_result_diff["blitz_p"] = (expected_result_diff["blitz_r"] / expected_result_diff["blitz_g"]) / 2
	expected_result_diff["rapid_p"] = (expected_result_diff["rapid_r"] / expected_result_diff["rapid_g"]) / 2
	print("I finished analyzing win probability...                    ", end="\n")

get_expected_results()
expected_result.to_csv("data/" + player["username"] + "_expected_results.csv", index=True, index_label="opponent_rating")
expected_result_diff.to_csv("data/" + player["username"] + "_expected_results_diff.csv", index=True, index_label="rating_difference")

log.close()

print("All files saved!          ", end="\n")

print("My work has ended...                          ", end="\n")
