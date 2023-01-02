import datetime as dt
import berserk as bk
import json as js
import pandas as pd

errors = [0,0,0] #ratings, evolution, games

#log = open("log.md", "a") #preparing log file...
#today = dt.date.today()
#log.write("\n")
#log.write("### %s"%today)
#log.write(":" + "\n")

config = js.load(open("config/lichess.json"))
player = js.load(open("config/rvalla.json"))

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

print("Obtaining player's activity from lichess...", end="\r")

feed = client.users.get_rating_history("rvalla")
print(feed[1]["points"][0])
