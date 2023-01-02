#import datetime as dt
import json as js
import pandas as pd
import datetime as dt
import matplotlib.colors as pltcolors
import matplotlib.pyplot as plt
import chart_config as cc

log = open("log.md", "a") #preparing log file...
today = dt.date.today()
log.write("\n")
log.write("### %s"%today)
log.write(":" + "\n")

player = js.load(open("config/sal1961.json"))

print("Let's plot some data from " + player["name"] + "'s games...", end="\n")

ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
ratings_evolution = pd.read_csv("data/" + player["username"] + "_ratings_evolution.csv", header=0, index_col=0)
ratings_evolution.index_name = "date"
games_count = pd.read_csv("data/" + player["username"] + "_games.csv", header=0, index_col=0)
games_count.index_name = "date"
games_time = pd.read_csv("data/" + player["username"] + "_time_analysis.csv", header=0, index_col=0)
expected_result = pd.read_csv("data/" + player["username"] + "_expected_results.csv", header=0, index_col=0)
expected_result_diff = pd.read_csv("data/" + player["username"] + "_expected_results_diff.csv", header=0, index_col=0)

half_color_map = pltcolors.ListedColormap(["white", "steelblue", "dodgerblue", "orange", "gold", "limegreen", "lime"])
color_map = pltcolors.ListedColormap(["r", "tab:orange", "gold",
									"khaki", "white", "steelblue", "dodgerblue",
									"limegreen", "lime"])

def get_data_lists(data):
	list = []
	for r in range(data.shape[0]):
		list.append(data.loc[data.index[r]])
	avg_list = [None for i in range(6)]
	for r in range(data.shape[0] - 12):
		avg = 0
		for i in range(12):
			avg += data.loc[data.index[r + i]]
		avg_list.append(avg / 12)
	for i in range(6):
		avg_list.append(None)
	return list, avg_list

def get_range(last_n, data_length):
	if last_n != 0:
		last = data_length - 1
		first = last - last_n
		return [first, last]
	else:
		return [0,data_length-1]

def ratings_by_game_texts(key, last_n):
	texts = [player["name"] + " 's " + key]
	if last_n != 0:
		texts[0] += " last " + str(last_n)
	texts[0] += " games: Rating history"
	texts.append("Games")
	texts.append("Rating")
	texts.append("12 games average")
	texts.append("games")
	return texts

def ratings_by_game(data, range, key, last_key, texts, y_axis):
	print("Plotting ratings by game...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data[range[0]:range[1]]["rating"])
	plt.plot(list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	if last_key == "all":
		cc.grid_and_ticks(True, y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	else:
		cc.auto_grid_and_ticks(True)
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot(player["username"] + "_rating_by_game_" + key + "_" + last_key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " rating evolution (" + key + ") was saved.\n")

def result_history_texts(key, last_n):
	texts = [player["name"] + " 's " + key]
	if last_n != 0:
		texts[0] += " last " + str(last_n)
	texts[0] += " games: Result history"
	texts.append("Games")
	texts.append("Cumulative result")
	texts.append("12 games average")
	texts.append("games")
	return texts

def result_history(data, range, key, last_key, texts, y_axis):
	print("Plotting result history by game...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data.iloc[range[0]:range[1]])
	plt.plot(list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	if last_key == "all":
		cc.grid_and_ticks(True, y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	else:
		cc.auto_grid_and_ticks(True)
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot(player["username"] + "_result_by_game_" + key + "_" + last_key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " result history (" + key + ") was saved.\n")

def histogram_texts(key):
	texts = [player["name"] + " 's " + key + " games: Rating histogram"]
	texts.append("Rating")
	texts.append("Games")
	return texts

def ranking_histogram(data, key, bins, texts):
	print("Plotting ratings histogram...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	data["rating"].plot(kind="hist", bins=bins, color=cc.colors[6])
	cc.format_and_background()
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.save_plot(player["username"] + "_rating_histogram_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " games histogram (" + key + ") was saved.\n")

def get_scatter_rating_difference(key, dates):
	list = [0]
	for d in range(1,len(dates)):
		last_rating = ratings_evolution.loc[dates[d-1]][key + "_mean"]
		list.append(ratings_evolution.loc[dates[d]][key + "_mean"] - last_rating)
	return list

def get_scatter_limits(data):
	minimum = min(data)
	maximum = max(data)
	if abs(minimum) > abs(maximum):
		return [minimum, minimum*-1]
	else:
		return [-maximum, maximum]

def game_count_scatter(texts, key, axis, week_interval):
	print("Plotting games count...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	games_count["x"] = pd.to_datetime(games_count.index, format="%Y-%m-%d")
	the_games = games_count[games_count[key] != 0]
	rating_diff = get_scatter_rating_difference(key, the_games.index.to_list())
	plot = plt.scatter(the_games["x"], the_games[key], c=rating_diff, cmap=color_map)
	cc.format_and_background()
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.grid_and_ticks(True, axis[0],axis[1],axis[2],axis[3])
	cc.ticks_week_locator(week_interval)
	c = plt.colorbar(plot)
	cc.build_color_bar(c, get_scatter_limits(rating_diff), "Daily rating difference")
	cc.save_plot(player["username"] + "_games_count_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " played games scatter (" + key + ") was saved.\n")

def expected_result_texts(key):
	texts = [player["name"] + " 's " + key + " expected result"]
	texts.append("By opponent rating")
	texts.append("Oponnent rating")
	texts.append("Winning chance")
	texts.append("By opponent rating difference")
	texts.append("Opponent rating difference")
	texts.append("Winning chance")
	texts.append("Games")
	return texts

def expected_result_scatter(texts, key):
	print("Plotting expected result scatter...", end="\r")
	f = plt.figure(num=None, figsize=(cc.d_w, cc.d_h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	f.suptitle(texts[0], fontname=cc.default_font, fontsize=14)
	data = expected_result[expected_result[key + "_g"] != 0]
	by_rating = plt.subplot2grid((2, 1), (0, 0))
	by_rating = plt.scatter(data.index, data[key + "_p"], c=data[key + "_g"], cmap=half_color_map)
	cc.format_and_background()
	cc.build_texts(texts[1], texts[2], texts[3])
	cc.grid_and_ticks(True, 0, 1, 0.25, 1)
	c = plt.colorbar(by_rating)
	cc.build_color_bar(c, [0, max(data[key + "_g"].tolist())], texts[7])
	data = expected_result_diff[expected_result_diff[key + "_g"] != 0]
	by_difference = plt.subplot2grid((2, 1), (1, 0))
	by_difference = plt.scatter(data.index, data[key + "_p"], c=data[key + "_g"], cmap=half_color_map)
	cc.format_and_background()
	cc.build_texts(texts[4], texts[5], texts[6])
	cc.grid_and_ticks(True, 0, 1, 0.25, 1)
	c = plt.colorbar(by_difference)
	cc.build_color_bar(c, [0, max(data[key + "_g"].tolist())], texts[7])
	cc.save_plot(player["username"] + "_expected_results_" + key, f)
	print("Charts were saved!                      ", end="\n")
	log.write("-- " + player["name"] + " expected results (" + key + ") was saved.\n")

def get_player_limits(text, key):
	offset = 0
	if key == "blitz":
		offset = 4
	elif key == "rapid":
		offset = 8
	limits = []
	list = text.split(",")
	for i in range(4):
		limits.append(int(list[i + offset]))
	return limits

def time_analysis_texts(key):
	texts = [player["name"] + " 's " + key + " games: Time analysis"]
	texts.append("Results")
	texts.append("")
	texts.append("Cumulative")
	texts.append("Rating variation")
	texts.append("Time of the day")
	texts.append("Rating variation")
	texts.append("Rating variation average")
	texts.append("Time of the day")
	texts.append("Variation average")
	return texts

def plot_time_analysis(key, texts):
	print("Plotting games time analysis...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	f.suptitle(texts[0], fontname=cc.default_font, fontsize=12)
	difference = plt.subplot2grid((2, 2), (0, 1))
	difference = games_time[key + "_res"].plot(kind="bar", color=cc.colors[1])
	cc.build_subplot_texts(texts[1], texts[2], texts[3])
	cc.auto_grid_and_ticks(False)
	difference = plt.subplot2grid((2, 2), (0, 0), rowspan=2)
	difference = games_time[key + "_diff"].plot(kind="bar", color=cc.colors[1])
	cc.build_subplot_texts(texts[4], texts[5], texts[6])
	cc.auto_grid_and_ticks(False)
	difference = plt.subplot2grid((2, 2), (1, 1))
	difference = games_time[key + "_diff_avg"].plot(kind="bar", color=cc.colors[1])
	cc.build_subplot_texts(texts[7], texts[8], texts[9])
	cc.auto_grid_and_ticks(False)
	cc.save_plot(player["username"] + "_time_analysis_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " games time analysis (" + key + ") was saved.\n")

def get_streaks(data):
	list = []
	current = None
	p = -1 #the current position on list
	for g in range(data.shape[0]):
		result = data.iloc[g]["points"]
		if current != result:
			list.append(result)
			current = result
			p += 1
		else:
			list[p] += result
	return list

def streaks_texts(key):
	texts = [player["name"] + " 's " + key + " games: Streak histogram"]
	texts.append("Streak size")
	texts.append("Streak count")
	return texts

def streaks_histogram(data, key, bins, texts):
	print("Plotting streak histogram...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list = get_streaks(data)
	plt.hist(list, color=cc.colors[1], bins=bins)
	cc.auto_grid_and_ticks(False)
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.save_plot(player["username"] + "_streak_histogram_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " games streak histogram (" + key + ") was saved.\n")

if player["plot_bullet"]:
	data = ratings[ratings["variant"]=="bullet"]
	points = data["points"].cumsum()
	length = data.shape[0]
	ratings_by_game(data, get_range(0, length), "bullet", "all", ratings_by_game_texts("bullet", 0), get_player_limits(player["ratings_limits"], "bullet"))
	result_history(points, get_range(0, length), "bullet", "all", result_history_texts("bullet", 0), get_player_limits(player["results_limits"], "bullet"))
	ratings_by_game(data, get_range(300, length), "bullet", "300", ratings_by_game_texts("bullet", 300), get_player_limits(player["ratings_limits"], "bullet"))
	result_history(points, get_range(300, length), "bullet", "300", result_history_texts("bullet", 300), get_player_limits(player["results_limits"], "bullet"))
	ranking_histogram(data, "bullet", 20, histogram_texts("bullet"))
	game_count_scatter([player["name"] + " 's " + " bullet games:", "Time", "Games"], "bullet", get_player_limits(player["games_limits"], "bullet"), 6)
	expected_result_scatter(expected_result_texts("bullet"), "bullet")
	plot_time_analysis("bullet", time_analysis_texts("bullet"))
	streaks_histogram(ratings[ratings["variant"]=="bullet"], "bullet", 15, streaks_texts("bullet"))

if player["plot_blitz"]:
	data = ratings[ratings["variant"]=="blitz"]
	points = data["points"].cumsum()
	length = data.shape[0]
	ratings_by_game(data, get_range(0, length), "blitz", "all", ratings_by_game_texts("blitz", 0), get_player_limits(player["ratings_limits"], "blitz"))
	result_history(points, get_range(0, length), "blitz", "all", result_history_texts("blitz", 0), get_player_limits(player["results_limits"], "blitz"))
	ratings_by_game(data, get_range(200, length), "blitz", "200", ratings_by_game_texts("blitz", 200), get_player_limits(player["ratings_limits"], "blitz"))
	result_history(points, get_range(200, length), "blitz", "200", result_history_texts("blitz", 200), get_player_limits(player["results_limits"], "blitz"))
	ranking_histogram(data, "blitz", 20, histogram_texts("blitz"))
	game_count_scatter([player["name"] + " 's " + " blitz games:", "Time", "Games"], "blitz", get_player_limits(player["games_limits"], "blitz"), 6)
	expected_result_scatter(expected_result_texts("blitz"), "blitz")
	plot_time_analysis("blitz", time_analysis_texts("blitz"))
	streaks_histogram(ratings[ratings["variant"]=="blitz"], "blitz", 15, streaks_texts("blitz"))

if player["plot_rapid"]:
	data = ratings[ratings["variant"]=="rapid"]
	points = data["points"].cumsum()
	length = data.shape[0]
	ratings_by_game(data, get_range(0, length), "rapid", "all", ratings_by_game_texts("rapid", 0), get_player_limits(player["ratings_limits"], "rapid"))
	result_history(points, get_range(0, length), "rapid", "all", result_history_texts("rapid", 0), get_player_limits(player["results_limits"], "rapid"))
	ratings_by_game(data, get_range(150, length), "rapid", "150", ratings_by_game_texts("rapid", 150), get_player_limits(player["ratings_limits"], "rapid"))
	result_history(points, get_range(150, length), "rapid", "150", result_history_texts("rapid", 150), get_player_limits(player["results_limits"], "rapid"))
	ranking_histogram(data, "rapid", 20, histogram_texts("rapid"))
	game_count_scatter([player["name"] + " 's " + " rapid games:", "Time", "Games"], "rapid", get_player_limits(player["games_limits"], "rapid"), 6)
	expected_result_scatter(expected_result_texts("rapid"), "rapid")
	plot_time_analysis("rapid", time_analysis_texts("rapid"))
	streaks_histogram(ratings[ratings["variant"]=="rapid"], "rapid", 15, streaks_texts("rapid"))


#closing log file...
log.write("\n")
log.close()

print("My work has ended...                          ", end="\n")
