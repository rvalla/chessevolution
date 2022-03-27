from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.ticker as tk
import matplotlib.dates as mdates
import numpy as np

w = 8
h = 4.5
d_w = 8
d_h = 6.5
chart_path = "charts/"
default_font = "Oswald" #Change this if you don't like it or is not available in your system
legend_font = "Myriad Pro" #Change this to edit legends' font
background_plot = "silver" #Default background color for charts
background_figure = "white" #Default background color for figures
major_grid_color = "dimgrey" #Default colors for grids...
minor_grid_color = "dimgray"
colors = ["tab:red", "tab:blue", "tab:green", "limegreen", "orange", "indianred", "teal", "darkslategray", \
			"mediumseagreen", "orangered", "goldenrod", "dimgrey", "whitesmoke", "mediumpurple", "indigo"]
a_colors = ["forestgreen", "darkgreen", "lightseagreen", "teal", "tab:blue", "darkblue", "indigo", \
			"mediumpurple", "firebrick", "darkred"]
alphaMGC = 0.7
alphamGC = 0.9
image_resolution = 120
legend_text_size = 8
plot_scale = "linear"
date_format = mdates.DateFormatter("%d/%m")

def save_plot(name, figure):
	if (plot_scale != "linear"):
		plt.yscale(plot_scale)
	plt.tight_layout(rect=[0, 0, 1, 1])
	plt.savefig(chart_path + name + ".png", facecolor=figure.get_facecolor())
	plt.close(figure)

def grid_and_ticks(y_min, y_max, ticks_interval, ticks_divisor):
	plt.grid(which='both', axis='both')
	plt.minorticks_on()
	plt.grid(True, "major", "y", ls="-", lw=0.8, c=major_grid_color, alpha=alphaMGC)
	plt.grid(True, "minor", "y", ls="--", lw=0.3, c=minor_grid_color, alpha=alphamGC)
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=major_grid_color, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minor_grid_color, alpha=alphamGC)
	yticks, ylabels = get_ticks_labels(y_min, y_max + ticks_interval, ticks_interval, ticks_divisor)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.yticks(yticks, ylabels)
	plt.gca().set_facecolor(background_plot)

def format_and_background():
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.gca().set_facecolor(background_plot)

def x_grid_and_ticks():
	plt.grid(which='both', axis='x')
	plt.minorticks_on()
	plt.grid(True, "major", "x", ls="-", lw=0.8, c=major_grid_color, alpha=alphaMGC)
	plt.grid(True, "minor", "x", ls="--", lw=0.3, c=minor_grid_color, alpha=alphamGC)
	plt.xticks(fontsize=6)
	plt.yticks(fontsize=6)
	plt.gca().set_facecolor(background_plot)

def get_ticks_labels(y_min, y_max, interval, divisor):
	values = []
	if y_min < 0 and y_max > 0:
		a = np.arange(0, y_max, interval)
		b = a[:0:-1] * (-1)
		values = np.concatenate((b, a),axis=0)
	else:
		values =  np.arange(y_min, y_max, interval)
	labels = (values / divisor).tolist()
	return values, labels

def build_texts(title, x_axis, y_axis):
	plt.title(title, fontname=default_font)
	plt.xlabel(x_axis, fontname=legend_font)
	plt.ylabel(y_axis, fontname=legend_font)

def build_axis_texts(axis, title, x_axis, y_axis):
	axis.set_title(title, fontname=default_font)
	axis.set_xlabel(x_axis, fontname=legend_font)
	axis.set_ylabel(y_axis, fontname=legend_font)

def build_legend():
	plt.legend(loc=2, shadow = True, facecolor = background_figure,
			prop={'family' : legend_font, 'size' : legend_text_size})

def build_legends(axis_a, axis_b):
	a, al = axis_a.get_legend_handles_labels()
	b, bl = axis_b.get_legend_handles_labels()
	axis_b.legend(a + b, al + bl, loc=2, shadow = True, facecolor = background_figure,
				prop={'family' : legend_font, 'size' : legend_text_size})

def ticks_week_locator(weekInterval):
	plt.gca().xaxis.set_minor_locator(tk.AutoMinorLocator(7))
	plt.gca().xaxis.set_major_formatter(date_format)
	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval = weekInterval))
	plt.gca().xaxis.set_minor_formatter(tk.NullFormatter())
