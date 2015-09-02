import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data file and ask for file formate, title, and labels
file_name_in = sys.argv[1]
file_format_out = 'pdf'
#file_format_out = raw_input('Figure output format: ').lower()
title = raw_input('Figure title: ')
ylab = raw_input('Y-axis label: ')
xlab = raw_input('X-axis label: ')

# read data into dataframe, set 'name' column to string in case they are numerical
data = pd.read_csv(file_name_in, dtype = {'name':object})

# get column headers for grouping/labeling later
headers = data.columns
#labels = headers[1][::3]

# create mean/stdev dataframes, grouping by sample names which are identical within triplicates
# but unique outside triplicates, do not sort the dataframes when creating them, calculat the mean/stdev
# create new column in each dataframe to hold the name of the triplicate
mean = data.groupby(headers[1], sort = False).mean()
mean[headers[1]] = mean.index
stdev = data.groupby(headers[1], sort = False).std()
stdev[headers[1]] = stdev.index

# get number of samples used for bar spacing, set bar width, adjust figure size to number of samples 
sample_num = np.arange(len(mean.index))
bar_width = 0.35
fig_width = (len(sample_num) / 2) + 4

# because all things must be Arial
plt.rcParams['font.sans-serif'] = 'Arial'

# begin to make a figure of appropriate sizes, add first set of bars, set labels and attributes
fig, ax = plt.subplots(figsize = (fig_width, 6))
rects1 = ax.bar(sample_num, mean[headers[2]], bar_width, yerr = stdev[headers[2]], color = 'red',
	label = headers[2], linewidth = 1.5,
	error_kw = dict(elinewidth = 1.5, capthick = 1.5, ecolor = 'black', capsize = 4))

# if there is a second dataset make bars for it
# set attributes for X-tick labels and adjust label placement if there is 1 dataset vs 2
if len(data.columns) == 4:
	rects2 = ax.bar(sample_num + bar_width, mean[headers[3]], bar_width, yerr = stdev[headers[3]],
		color = 'grey', label = headers[3], linewidth = 1.5,
		error_kw = dict(elinewidth = 1.5, capthick = 1.5, ecolor = 'black', capsize = 4))
	plt.xticks(sample_num + (bar_width), mean[headers[1]], fontsize = 16, rotation = 45)
else:
	plt.xticks(sample_num + (bar_width / 2), mean[headers[1]], fontsize = 16, rotation = 45)

# increase fontsize and linewidth for title, axis labels, and ticks
# define tick placement, force axis minimums to set values while maximums will autoscale to data
plt.suptitle(title, fontsize = 20)
plt.ylabel(ylab, fontsize = 20)
plt.xlabel(xlab, fontsize = 20)
plt.yticks(fontsize = 16)
plt.tick_params(axis = 'y', length = 5, width = 1.5, right = False)
plt.tick_params(axis = 'x', length = 0)
plt.gca().set_ylim(bottom = 0)
plt.gca().set_xlim(left = -0.5)

#uncomment the line below to set an arbitrary y-axis maximum
#plt.gca().set_ylim(top = 2000)

# increase linewidth for axes surrounding the figure
for axis in ['top','bottom','left','right']:
  ax.spines[axis].set_linewidth(1.5)

# create legend, automatic location, no box, change rectangles to squares and adjust spacing
leg = ax.legend(loc = 0, frameon = False, handlelength = 0.70,
	handletextpad = 0.5, labelspacing = 0.25, fontsize = 30)

# readjust legend font size independent of square size, readjust spacing
for txt in leg.get_texts():
		txt.set_fontsize(20)
		txt.set_va('bottom')

# save figure in desired format with name from input data, tightly crop the figure
plt.savefig((file_name_in[0:-3] + file_format_out), bbox_inches = 'tight')
