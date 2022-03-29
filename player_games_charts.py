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

player = js.load(open("config/augusr.json"))

print("Let's plot some data from " + player["name"] + "'s games...", end="\n")

ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
ratings_evolution = pd.read_csv("data/" + player["username"] + "_ratings_evolution.csv", header=0, index_col=0)
ratings_evolution.index_name = "date"
games_count = pd.read_csv("data/" + player["username"] + "_games.csv", header=0, index_col=0)
games_count.index_name = "date"

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

def ratings_by_game_texts(key):
	texts = [player["name"] + " 's " + key + " games: Rating history"]
	texts.append("Games")
	texts.append("Rating")
	texts.append("12 games average")
	texts.append("games")
	return texts

def ratings_by_game(data, key, texts, y_axis):
	print("Plotting ratings by game...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data["rating"])
	plt.plot(range(data.shape[0]), list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(range(data.shape[0]), avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	cc.grid_and_ticks(y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot(player["username"] + "_rating_by_game_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " rating evolution (" + key + ") was saved.\n")

def result_history_texts(key):
	texts = [player["name"] + " 's " + key + " games: Result history"]
	texts.append("Games")
	texts.append("Cumulative result")
	texts.append("12 games average")
	texts.append("games")
	return texts

def result_history(data, key, texts, y_axis):
	print("Plotting result history by game...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data["points"].cumsum())
	plt.plot(range(data.shape[0]), list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(range(data.shape[0]), avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	cc.grid_and_ticks(y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot(player["username"] + "_result_by_game_" + key, f)
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

def game_count_scatter(texts, key, y_axis, week_interval):
	print("Plotting games count...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	games_count["x"] = pd.to_datetime(games_count.index, format="%Y-%m-%d")
	the_games = games_count[games_count[key] != 0]
	rating_diff = get_scatter_rating_difference(key, the_games.index.to_list())
	plot = plt.scatter(the_games["x"], the_games[key], c=rating_diff, cmap=color_map)
	cc.format_and_background()
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.grid_and_ticks(y_axis[0],y_axis[1],y_axis[2],y_axis[3])
	cc.ticks_week_locator(week_interval)
	c = plt.colorbar(plot)
	cc.build_color_bar(c, get_scatter_limits(rating_diff))
	cc.save_plot(player["username"] + "_games_count_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " played games scatter (" + key + ") was saved.\n")

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

if player["plot_bullet"]:
	ratings_by_game(ratings[ratings["variant"]=="bullet"], "bullet", ratings_by_game_texts("bullet"), get_player_limits(player["ratings_limits"], "bullet"))
	result_history(ratings[ratings["variant"]=="bullet"], "bullet", result_history_texts("bullet"), get_player_limits(player["results_limits"], "bullet"))
	ranking_histogram(ratings[ratings["variant"]=="bullet"], "bullet", 20, histogram_texts("bullet"))
	game_count_scatter([player["name"] + " 's " + " bullet games:", "Time", "Games"], "bullet", get_player_limits(player["games_limits"], "bullet"), 6)

if player["plot_blitz"]:
	ratings_by_game(ratings[ratings["variant"]=="blitz"], "blitz",ratings_by_game_texts("blitz"), get_player_limits(player["ratings_limits"], "blitz"))
	result_history(ratings[ratings["variant"]=="blitz"], "blitz", result_history_texts("blitz"), get_player_limits(player["results_limits"], "blitz"))
	ranking_histogram(ratings[ratings["variant"]=="blitz"], "blitz", 20, histogram_texts("blitz"))
	game_count_scatter([player["name"] + " 's " + " blitz games:", "Time", "Games"], "blitz", get_player_limits(player["games_limits"], "blitz"), 6)

if player["plot_rapid"]:
	ratings_by_game(ratings[ratings["variant"]=="rapid"], "rapid",ratings_by_game_texts("rapid"), get_player_limits(player["ratings_limits"], "rapid"))
	result_history(ratings[ratings["variant"]=="rapid"], "rapid", result_history_texts("rapid"), get_player_limits(player["results_limits"], "rapid"))
	ranking_histogram(ratings[ratings["variant"]=="rapid"], "rapid", 20, histogram_texts("rapid"))
	game_count_scatter([player["name"] + " 's " + " rapid games:", "Time", "Games"], "rapid", get_player_limits(player["games_limits"], "rapid"), 6)

#closing log file...
log.write("\n")
log.close()

print("My work has ended...                          ", end="\n")
