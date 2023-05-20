"""
The code in this file is for each of the visualizations in the Streamlit app.

It uses the dataframe that is created in mta.py

I mostly worked in iPython(interactive), and each of these code blurbs outputs a json file.
"""

#daily counts - rolling average
daily_traffic_sum = merged.resample('D')['net_traffic'].sum()
rolling_days = daily_traffic_sum.rolling(7, min_periods=1)
rolling_average_days = rolling_days.mean()
rolling_average_days = rolling_average_days.reset_index()
rolling_average_days['category'] = 'day'

#weekly counts - rolling average
weekly_traffic_sum = merged.resample('W')['net_traffic'].sum()
rolling_weeks = weekly_traffic_sum.rolling(30, min_periods=1)
rolling_average_weeks = rolling_weeks.mean()
rolling_average_weeks = rolling_average_weeks.reset_index()
rolling_average_weeks['category'] = 'week'

rolling_avg_days_weeks = pd.concat([rolling_average_days, rolling_average_weeks])
rolling_avg_days_weeks.to_json(orient="records", path_or_buf="rolling_avg_days_weeks.json")


#box plot - traffic by each day of the week
daily_sums = merged.groupby(['weekday', pd.Grouper(freq='D')])['net_traffic'].sum()
daily_sums = daily_sums.reset_index()
daily_stats = daily_sums.groupby(['weekday'])['net_traffic'].describe()
daily_stats['median'] = daily_sums.groupby(['weekday'])['net_traffic'].median()
daily_stats = daily_stats.reset_index()
daily_stats.to_json(orient="records", path_or_buf="weekday_box_plot.json")


#weekly stacked area chart - weekend vs non-weekend traffic
week_day_end_sums = merged.groupby(['is_weekend', pd.Grouper(freq='D')])['net_traffic'].sum()
week_day_end_sums = week_day_end_sums.rolling(7,min_periods=1)
week_day_end_mean = week_day_end_sums.mean()
week_day_end_mean = week_day_end_mean.reset_index(name="mean_traffic")
week_day_end_mean = week_day_end_mean.set_index('observed_at')
week_day_end_mean_weekly = week_day_end_mean.groupby(['is_weekend', pd.Grouper(freq='W')])['mean_traffic'].sum()
week_day_end_mean_weekly = week_day_end_mean_weekly.reset_index()
week_day_end_mean_weekly['pct_change'] = week_day_end_mean_weekly.groupby('is_weekend')['mean_traffic'].pct_change()
week_day_end_mean_weekly['pct_change'] = week_day_end_mean_weekly['pct_change'].fillna(0)
week_day_end_mean_weekly.to_json(orient="records", path_or_buf="weekly_traffic_weekend_vs_day.json")


# diverging bar chart: entries and exits
grouped = merged.groupby([pd.Grouper(freq='D'), 'hour_bin', 'is_weekend']).agg({'net_entries': 'sum', 'net_exits': 'sum'})
grouped = grouped.reset_index()
entries = grouped[['observed_at', 'hour_bin', 'is_weekend', 'net_entries']]
entries['type'] = 'entry'
entries = entries.rename(columns={"net_entries": "count"})
exits = grouped[['observed_at', 'hour_bin', 'is_weekend', 'net_exits']]
exits['type'] = 'exit'
exits = exits.rename(columns={"net_exits": "count"})
entry_exits = pd.concat([entries,exits])
entry_exits = entry_exits.set_index('observed_at')
entry_exit_rows = entry_exits.groupby(['hour_bin', 'is_weekend', 'type'])['count'].sum()
entry_exit_rows = entry_exit_rows.reset_index()
entry_exit_rows['count'] = entry_exit_rows['count'].astype('int')
entry_exit_rows.to_json(orient="records", path_or_buf='entry_exit_hours.json')


#weekly ratio of entries to exits
weekly_ratio = merged.groupby([pd.Grouper(freq='W')]).apply(lambda r: r['net_entries'].sum()/r['net_exits'].sum())
weekly_ratio = weekly_ratio.reset_index(name="ratio")
weekly_ratio.observed_at = weekly_ratio.observed_at.dt.strftime('%Y-%m-%d')
weekly_ratio['diff'] = weekly_ratio['ratio'] - 1
weekly_ratio.to_json(orient="records", path_or_buf="weekly_entry_exit_ratios.json")


#bubble chart - net traffic by turnstile and line count
bubble_chart_data = merged.groupby('STATION').agg({'net_traffic': 'sum', 'unit_id': 'nunique','LINENAME': 'first'})
bubble_chart_data['num_lines'] = bubble_chart_data['LINENAME'].str.len()
bubble_chart_data.net_traffic = bubble_chart_data.net_traffic.astype('int')
bubble_chart_data = bubble_chart_data.reset_index()
bubble_chart_data.to_json(orient="records",path_or_buf="bubble_chart_data.json")


#change entries or exits column depending
def weekday_time_bin_heatmap(frame, output_file_name):
	grouped = frame.groupby(['weekday', 'hour_bin'])['net_exits'].sum().unstack().fillna(0).stack().reset_index(name='count')
	grouped.to_json(orient="records",path_or_buf=output_file_name)
	return grouped

weekday_time_bin_heatmap(merged,"days_hours.json")
weekday_time_bin_heatmap(merged,"days_hours_exits.json")



#station traffic with number of turnstiles
traffic_station_turnstiles = merged.groupby('STATION').agg({'net_traffic':'sum', 'unit_id': 'nunique', 'LINENAME': 'first'})
#highest traffic turnstiles/stations
top_ten_overall_stations = traffic_station_turnstiles.sort_values(by="net_traffic", ascending=False).head(10)
top_ten_overall_stations = top_ten_overall_stations.reset_index()
top_ten_overall_stations['category'] = 'highest'
top_ten_lowest_traffic = traffic_station_turnstiles.sort_values(by="net_traffic").head(10)
top_ten_lowest_traffic = top_ten_lowest_traffic.reset_index()
top_ten_lowest_traffic['net_traffic'] = top_ten_lowest_traffic['net_traffic'].astype('int')
top_ten_lowest_traffic['category'] = 'lowest'
top_and_bottom_ten_traffic = pd.concat([top_ten_overall_stations, top_ten_lowest_traffic])
top_and_bottom_ten_traffic.to_json(orient="records", path_or_buf="top_bottom_ten_traffic.json")


#top traffic station - Penn Station
penn = merged[merged['STATION'] == '34 ST-PENN STA']
penn_daily = penn.groupby([pd.Grouper(freq="D")]).agg({'net_traffic': 'sum', 'weekday': 'first'})
penn_daily_time = penn_daily.set_index('observed_at')
penn_daily_time['month'] = penn_daily_time.index.month_name()
penn_monthly_traffic = penn_daily_time.groupby(['month']).agg({'net_traffic': 'describe', 'weekday': 'first'})
penn_stats = penn_monthly_traffic.groupby([pd.Grouper(freq='M')])['net_traffic'].describe()
penn_stats['median'] = penn_daily_time.groupby([pd.Grouper(freq='M')])['net_traffic'].median()
penn_stats['net_traffic'] = penn_daily_time.groupby([pd.Grouper(freq='M')])['net_traffic'].sum()
penn_stats = penn_stats.reset_index()
penn_stats.observed_at = penn_stats.observed_at.dt.month_name()
penn_stats['plot'] = 'month'
penn_daily = penn_daily.reset_index()
penn_weekday_stats = penn_daily.groupby(['weekday'])['net_traffic'].describe()
penn_weekday_stats['median'] = penn_daily.groupby(['weekday'])['net_traffic'].median()
penn_weekday_stats['net_traffic'] = penn_daily.groupby(['weekday'])['net_traffic'].sum()
penn_weekday_stats['plot'] = 'week'
penn_weekday_stats = penn_weekday_stats.reset_index()
penn_station_box_plots = pd.concat([penn_stats,penn_weekday_stats])
penn_station_box_plots.to_json(orient="records", path_or_buf="penn_box_plots.json")









