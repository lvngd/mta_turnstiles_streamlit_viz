# MTA Turnstile Data Visualization
01/01/2020 to 06/30/2020

Visualized using Streamlit + vega-lite.


## How to run

In a virtual environment, install requirements.

```
pip install -r requirements.txt
```

Then run with this command:

```
streamlit run streamlit_app.py
```

You should be able to view at **http://localhost:8501/**.

## MTA turnstile data

The MTA turnstile data used to be found at [http://web.mta.info/developers/turnstile.html](http://web.mta.info/developers/turnstile.html), and has been archived. 

The url now redirects, but I am using the archived data that used to be hosted there.


### Rolling Averages - Daily and Weekly traffic

First I looked at the average turnstile traffic, from January to June, 2020. 

The MTA data has counts of turnstile entries and exits, and in these visualizations, **traffic** mostly means **combined** entries and exits. 

Of course this is the time period that surrounds the start of the COVID-19 pandemic, and you can see a huge drop in traffic in March-April, 2020, which is when the city started to lock down.

I took a rolling average of the daily and weekly turnstile traffic, which you see in the first charts. 

### Rolling Weekly Average

The next chart is another rolling weekly average, but this time it divides the day into quadrants and looks at the traffic for each.

The turnstile data is collected roughly 4 times per day. 

It is updated in a similar way to an odometer, where the numbers increment up to a certain point and then reset. Sometimes, for certain turnstiles, the numbers instead decrement, so this presented some challenges when wrangling the data. 

### Day of Week Breakdown

The next chart is a box plot that shows descriptive statistics broken down by the day of the week.

### Weekend vs Weekday traffic

This chart shows another rolling average of traffic, broken down by weekdays vs weekends. 

I thought that might be interesting to look at when taking the pandemic into account, with remote work in full force, whether or not traffic on weekdays decreased in a disproportionate way to weekend traffic.

### Turnstile entries and exits

Next, I thought it would be interesting to break down entries and exits. 

So this is a diverging bar chart with entries on one side and exits on the other. 

The bars are also broken down by weekend vs weekday traffic, and the scales are the same on each side.

### Turnstile entry to exit ratio

This chart shows overall turnstile entries to exits. 

I computed the ratios and then subtracted 1 to adjust them to show which way the ratio leans, so positive numbers indicate that the ratio favors entries, and negative indicates that the ratio favors exits. 

### Bubble chart

The bubble chart shows the correlation between traffic and turnstile count. 

The bubble size is a function of the number of subway lines in that station.

In the turnstile data, there are a few columns that, when concatenated together, can create a unique id that represents a single turnstile.

Another column has a string that represents the subway line names, so there might be "ABC", which means that the station has A, B and C trains. 

So I took the length of this string to get the number of lines.

### Heatmaps - turnstile entries and exits

The following two visualizations are heatmaps and they show turnstile entries and exits, respectively, by time bucket and day of the week. 

I kept the scales the same for both of the heatmaps, so they can be compared.

### Top 10 and Bottom 10 Stations by traffic

Next is a bar chart that has both the top 10 and bottom 10 subway stations by total traffic. 

### Penn Station

34th Street Penn Station is the station with the most traffic overall, and so the final two visualizations are box plots breaking down its traffic.

The first one shows the traffic broken down over each week day.

The second shows the traffic for each month, and March is particularly interesting here because it was a little after mid March when everything really started to shut down in the city.


## Sources

I used a few sources to learn about this data - particularly about the columns that can be concatenated to form a unique id for each turnstile.


*  [https://medium.com/qri-io/taming-the-mtas-unruly-turnstile-data-c945f5f96ba0](https://medium.com/qri-io/taming-the-mtas-unruly-turnstile-data-c945f5f96ba0)
*  [https://towardsdatascience.com/mta-turstile-data-my-first-taste-of-a-data-science-project-493b03f1708a](https://towardsdatascience.com/mta-turstile-data-my-first-taste-of-a-data-science-project-493b03f1708a)
*  [https://toddwschneider.com/dashboards/nyc-subway-turnstiles-exits/](https://toddwschneider.com/dashboards/nyc-subway-turnstiles-exits/)






