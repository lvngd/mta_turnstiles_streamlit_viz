import pandas as pd

pd.set_option('display.float_format', lambda x: '%.3f' % x)

OUTLIER_PERCENTILE = 0.96

"""

The MTA turnstile data urls listed below used to be at this url http://web.mta.info/developers/turnstile.html

But they updated things on ~May 17, 2023 and these are the archives.

This script fetches the data from each of the urls and then concatenates them 
together into one large Pandas dataframe. 

I worked in iPython, and mostly ran this script in interactive mode, 
and then ran the code snippets in 
mta_charts.py for each visualization.
"""
data_urls = ["http://web.mta.info/developers/data/nyct/turnstile/turnstile_200704.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_191228.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200627.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200620.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200613.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200606.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200530.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200523.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200516.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200509.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200502.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200425.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200418.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200411.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200404.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200328.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200321.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200314.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200307.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200229.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200222.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200215.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200208.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200201.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200125.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200118.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200111.txt",
"http://web.mta.info/developers/data/nyct/turnstile/turnstile_200104.txt"]


#remove outliers - anything above 96 percentile for net traffic
def remove_outliers(frame, column_name):
	frame = frame[frame[column_name] < frame[column_name].quantile(OUTLIER_PERCENTILE)]
	return frame


def get_hour_bin(row):
	hour = row['hour']
	if hour <= 6:
		return "12am-6am"
	elif hour > 6 and hour <= 12:
		return "6am-12pm"
	elif hour > 12 and hour <= 18:
		return "12pm-6pm"
	elif hour > 18:
		return "6pm-12am"


def prepare_data(frame):
	frame.columns = frame.columns.str.strip()
	frame['observed_at'] = frame['DATE'] + ':' + frame['TIME']
	frame['observed_at'] = pd.to_datetime(frame['observed_at'], format="%m/%d/%Y:%H:%M:%S")
	#UNIQUE
	frame['id'] = frame['UNIT'] + frame['C/A'] + frame['SCP'] + frame['DATE'] + frame['TIME']
	frame['unit_id'] = frame['UNIT'] + frame['C/A'] + frame['SCP']
	frame = frame.drop(columns=['DIVISION', 'DESC', 'UNIT', 'C/A', 'SCP', 'DATE', 'TIME'])
	#add in hour and weekday for heatmap
	frame['hour'] = frame['observed_at'].dt.hour
	frame['weekday'] = frame['observed_at'].dt.day_name()
	#bin the hours into 4 quadrants
	frame['hour_bin'] = frame.apply(get_hour_bin, axis=1)
	#datetime index
	frame = frame.set_index('observed_at')
	return frame



frames = []
for url in data_urls:
	frame = pd.read_csv(url)
	edited_frame = prepare_data(frame)
	frames.append(edited_frame)


#concatenate frame from each data url
merged = pd.concat(frames)

#sort by timestamp index
merged = merged.sort_index()

"""
get net values for entry, exit and total traffic for each check by taking the absolute value
of the difference between the value and the previous value, because it increases like
an odometer
"""

def get_net_entry_exits(frame):
	#absolute values because some turnstiles count down instead of up
	frame.drop_duplicates(subset=["id"],inplace=True)
	frame['net_entries'] = frame.groupby('unit_id')['ENTRIES'].diff()
	frame['net_entries'] = frame['net_entries'].abs()
	frame['net_exits'] = frame.groupby('unit_id')['EXITS'].diff()
	frame['net_exits'] = frame['net_exits'].abs()
	frame['net_traffic'] = frame['net_entries'] + frame['net_exits']
	return frame

merged = get_net_entry_exits(merged)


#the only NAs at this point are the first rows for each turnstile unit from using diff()
merged['net_entries'].fillna(0, inplace=True)
merged['net_exits'].fillna(0, inplace=True)

#removing outliers
merged = remove_outliers(merged,'net_traffic')

"""
slice off excess rows before 1/1/2020 and after 6/30/2020
since the data starts before 1/1/2020, 
the fillna = 0s(the first .diff() value) will be chopped off anyway
"""
merged = merged['2020-01-01':'2020-06-30']
merged['month'] = merged.index.month


'''
merged is the dataframe that I am using with the code in mta_charts.py
'''




