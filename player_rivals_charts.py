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

rival = "AugusR"
player = js.load(open("config/rvalla.json"))

print("Let's plot some data from " + player["name"] + "'s games vs " + rival + "...", end="\n")

ratings = pd.read_csv("data/" + player["username"] + "_ratings_history.csv")
vs_history = ratings[ratings["op_username"]==rival]

def score_by_game_texts():
	texts = [player["name"] + " vs. " + rival]
	texts[0] += " score history"
	texts.append("Games")
	texts.append("Score")
	return texts

def score_by_game(texts):
	print("Plotting score by game...", end="\r")
	f = plt.figure(num=None, figsize=(cc.w, cc.h), dpi=cc.image_resolution, facecolor=cc.background_figure, edgecolor='k')
	f.suptitle(texts[0], fontname=cc.default_font, fontsize=14)
	score = vs_history["points"].cumsum().to_list()
	all = plt.subplot2grid((1, 2), (0, 0))
	plt.plot(score, color=cc.colors[6], linewidth=2.0, label="")
	cc.auto_grid_and_ticks(True)
	cc.build_texts("", texts[1], texts[2])
	by_type = plt.subplot2grid((1, 2), (0, 1))
	keys = ["bullet","blitz","rapid","classical","correspondence"]
	for i in range(5):
		score = vs_history[vs_history["variant"]==keys[i]]["points"].cumsum().to_list()
		plt.plot(score, color=cc.colors[i+5], linewidth=2.0, label=keys[i])
	cc.auto_grid_and_ticks(True)
	cc.build_texts("", texts[1], texts[2])
	cc.build_legend()
	cc.save_plot(player["username"] + "_vs_" + rival + "_score_history", f)
	print("Charts were saved!                    ", end="\n")
	log.write("-- " + player["name"] + " rival score was saved.\n")

score_by_game(score_by_game_texts())

#closing log file...
log.write("\n")
log.close()

print("My work has ended...                          ", end="\n")
