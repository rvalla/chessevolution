import datetime as dt
import json as js
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import chart_config as cc

log = open("log.md", "a") #preparing log file...
today = dt.date.today()
log.write("\n")
log.write("### %s"%today)
log.write(":" + "\n")

player = js.load(open("config/rvalla.json"))

print("Let's plot some data from " + player["name"] + "'s games...", end="\n")

ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
ratings_evolution = pd.read_csv("data/" + player["username"] + "_ratings_evolution.csv", header=0, index_col=0)
ratings_evolution.index_name = "date"
games_count = pd.read_csv("data/" + player["username"] + "_games.csv", header=0, index_col=0)
games_count.index_name = "date"

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
	f = figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data["rating"])
	plt.plot(range(data.shape[0]), list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(range(data.shape[0]), avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	cc.grid_and_ticks(y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot("rating_by_game_" + key, f)
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
	f = figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	list, avg_list = get_data_lists(data["points"].cumsum())
	plt.plot(range(data.shape[0]), list, color=cc.colors[6], linewidth=1.0, label=texts[4])
	plt.plot(range(data.shape[0]), avg_list, linewidth=2.5, color=cc.colors[0], label=texts[3])
	cc.grid_and_ticks(y_axis[0], y_axis[1], y_axis[2], y_axis[3])
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.build_legend()
	cc.save_plot("result_by_game_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " result history (" + key + ") was saved.\n")

def histogram_texts(key):
	texts = [player["name"] + " 's " + key + " games: Rating histogram"]
	texts.append("Rating")
	texts.append("Games")
	return texts

def ranking_histogram(data, key, bins, texts):
	print("Plotting ratings histogram...", end="\r")
	f = figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	data["rating"].plot(kind="hist", bins=bins, color=cc.colors[6])
	cc.format_and_background()
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.save_plot("rating_histogram_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " games histogram (" + key + ") was saved.\n")

def game_count_scatter(texts, key, y_axis, week_interval):
	print("Plotting games count...", end="\r")
	f = figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	games_count["x"] = pd.to_datetime(games_count.index, format="%Y-%m-%d")
	games_count[games_count[key] != 0].plot(kind="scatter", x="x", y=key, color=cc.colors[0])
	cc.format_and_background()
	cc.build_texts(texts[0], texts[1], texts[2])
	cc.grid_and_ticks(y_axis[0],y_axis[1],y_axis[2],y_axis[3])
	cc.ticks_week_locator(week_interval)
	cc.save_plot("games_count_" + key, f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " played games scatter (" + key + ") was saved.\n")


ratings_by_game(ratings[ratings["variant"]=="bullet"], "bullet", ratings_by_game_texts("bullet"), [700, 1500, 100, 1])
ratings_by_game(ratings[ratings["variant"]=="blitz"], "blitz",ratings_by_game_texts("blitz"), [900, 1500, 100, 1])
ratings_by_game(ratings[ratings["variant"]=="rapid"], "rapid",ratings_by_game_texts("rapid"), [1200, 1600, 100, 1])

result_history(ratings[ratings["variant"]=="bullet"], "bullet", result_history_texts("bullet"), [-200,100,50,1])
result_history(ratings[ratings["variant"]=="blitz"], "blitz", result_history_texts("blitz"), [-50,25,10,1])
result_history(ratings[ratings["variant"]=="rapid"], "rapid", result_history_texts("rapid"), [-15,10,5,1])

ranking_histogram(ratings[ratings["variant"]=="bullet"], "bullet", 20, histogram_texts("bullet"))
ranking_histogram(ratings[ratings["variant"]=="blitz"], "blitz", 20, histogram_texts("blitz"))
ranking_histogram(ratings[ratings["variant"]=="rapid"], "rapid", 20, histogram_texts("rapid"))

game_count_scatter([player["name"] + " 's " + " bullet games:", "Time", "Games"], "bullet", [0,110,25,1], 6)
game_count_scatter([player["name"] + " 's " + " blitz games:", "Time", "Games"], "blitz", [0,50,10,1], 6)
game_count_scatter([player["name"] + " 's " + " rapid games:", "Time", "Games"], "rapid", [0,10,2,1], 6)

#closing log file...
log.write("\n")
log.close()

print("My work has ended...                          ", end="\n")
