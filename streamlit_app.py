import streamlit as st
import pandas as pd

st.title('MTA Turnstile Data')
st.write('01/01/2020 to 06/30/2020')

from pathlib import Path


path = Path(__file__).parent / 'data/'

rolling_averages = pd.read_json(
    path / 'rolling_avg_days_weeks.json')
rolling_weekly_means_chart = pd.read_json(
    path / 'rolling_week_means.json')
day_of_week_box_plot = pd.read_json(
    path / 'weekday_box_plot.json')
weekday_weekend_traffic_stacked_area = pd.read_json(
    path / 'weekly_traffic_weekend_vs_day.json')
entry_exit_hours = pd.read_json(
    path / 'entry_exit_hours.json')
entry_exit_ratios = pd.read_json(
    path / 'weekly_entry_exit_ratios.json')
bubble_chart_data = pd.read_json(
    path / 'bubble_chart_data.json')
subway_entry_heatmap = pd.read_json(
    path / 'days_hours.json', dtype="int")
subway_exit_heatmap = pd.read_json(
    path / 'days_hours_exits.json')
top_bottom_ten_station_traffic = pd.read_json(
    path / 'top_bottom_ten_traffic.json')
penn_box_plots = pd.read_json(
    path / 'penn_box_plots.json')


st.vega_lite_chart(rolling_averages,
                   {
                       "title": {"text": "Average Turnstile Traffic", "subtitle": "Rolling averages of turnstile entries + exits.", "color": "#000", "anchor": "middle"},

                       "spacing": 20,
                       "hconcat": [
                           {
                               "transform": [{
                                   "filter": {"field": "category", "equal": "day"}
                               }],
                               "width": 300,
                               "title": {"text": "Daily", "anchor": "middle"},

                               "mark": {"type": "line", "color": "#28666e"},
                               "encoding": {
                                   "x": {
                                       "field": "observed_at",
                                       "type": "temporal",
                                       "title": None
                                   },
                                   "y": {
                                       "field": "net_traffic",
                                       "aggregate": "sum",
                                       "axis": {"format": "s"},
                                       "title": "Traffic"
                                   }
                               },

                           },
                           {
                               "transform": [{
                                   "filter": {"field": "category", "equal": "week"}
                               }],
                               "width": 300,
                               "title": {"text": "Weekly", "anchor": "middle"},
                               "mark": {"type": "line", "color": "#28666e"},
                               "tooltip": [
                                   {"field": "observed_at",
                                       "type": "text", "title": "Date"},
                                   {"field": "net_traffic",
                                       "type": "quantitative", "title": "Traffic"},
                               ],
                               "encoding": {
                                   "x": {
                                       "field": "observed_at",
                                       "type": "temporal",
                                       "title": None
                                   },
                                   "y": {
                                       "field": "net_traffic",
                                       "aggregate": "sum",
                                       "axis": {"format": "s"},
                                       "title": None
                                   }

                               }
                           }
                       ]
                   }
                   )

st.vega_lite_chart(rolling_weekly_means_chart,
                   {
                       "title": {"text": "Rolling Weekly Average", "subtitle": "Turnstile entries + exits by time bucket.", "anchor": "middle"},
                       "width": 500,
                       "height": 200,
                       "mark": "line",
                       "encoding": {
                           "x": {"field": "observed_at", "type": "temporal", "title": "Month"},
                           "y": {"field": "net_traffic", "type": "quantitative", "title": "Traffic"},
                           "color": {"title": None, "field": "hour_bin", "type": "ordinal", "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"], "scale": {"range": ["#440154", "#31688e", "#35b779", "#fde725"]}}
                       }
                   }
                   )

st.vega_lite_chart(day_of_week_box_plot,
                   {
                       "title": {"text": "Descriptive Statistics", "subtitle": "Traffic statistics by day of week.", "anchor": "middle"},

                       "encoding": {"y": {
                           "field": "weekday",
                           "type": "nominal",
                           "title": None,
                           "sort": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                       },
                           "tooltip": [
                           {"field": "weekday", "type": "text", "title": "Day"},
                           {"field": "min", "type": "quantitative", "title": "Min"},
                           {"field": "25%", "type": "quantitative", "title": "25%"},
                           {"field": "75%", "type": "quantitative", "title": "75%"},
                           {"field": "max", "type": "quantitative", "title": "Max"},
                           {"field": "median", "type": "quantitative",
                               "title": "Median"},
                           {"field": "mean", "type": "quantitative", "title": "Mean"},
                           {"field": "std", "type": "quantitative",
                               "title": "Standard Deviation"}



                       ]},

                       "layer": [

                           {
                               "mark": {"type": "rule", "color": "#003d5b"},
                               "encoding": {
                                   "x": {"field": "min", "type": "quantitative", "scale": {"zero": False}, "title": None},
                                   "x2": {"field": "max"}
                               }
                           },
                           {
                               "mark": {"type": "bar", "size": 14},

                               "encoding": {
                                   "x": {"field": "25%", "type": "quantitative"},
                                   "x2": {"field": "75%"},
                                   "color": {"field": "weekday", "type": "nominal", "legend": None, "scale": {"range": ["#440154", "#443983", "#31688e", "#21918c", "#35b779", "#90d743", "#fde725"]}}
                               }
                           },
                           {
                               "mark": {"type": "tick", "color": "white", "size": 14},
                               "encoding": {
                                   "x": {"field": "median", "type": "quantitative"}
                               }

                           }
                       ]
                   })

st.vega_lite_chart(weekday_weekend_traffic_stacked_area,
                   {
                       "title": {"text": "Weekend vs Weekday Traffic", "subtitle": "Entries + Exits on weekdays vs weekend days.", "anchor": "middle"},
                       "width": 500, "height": 200,
                       "mark": "area",
                       "encoding": {
                           "x": {
                               "title": None,
                               "timeUnit": "yearmonth",
                               "field": "observed_at",
                               "axis": {"format": "%Y-%m"}
                           },
                           "y": {
                               "aggregate": "sum",
                               "field": "mean_traffic",
                               "title": "Average Traffic",
                           },
                           "color": {
                               "field": "is_weekend",
                               "title": "Is Weekend",
                               "scale": {"range": ["#52b69a", "#d9ed92"]}
                           }
                       }
                   }
                   )

st.vega_lite_chart(entry_exit_hours,
                   {
                       "title": {"text": "Turnstile Entries and Exits", "subtitle": "Weekend vs Weekday by Time Bucket", "anchor": "middle"},
                       "spacing": 0,
                       "hconcat": [{
                           "transform": [{
                               "filter": {"field": "type", "equal": "entry"}
                           }],
                           "title": {"text": "Entries", "anchor": "middle"},
                           "mark": "bar",
                           "encoding": {
                               "y": {
                                   "field": "hour_bin", "axis": None, "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"]
                               },
                               "x": {
                                   "aggregate": "sum",
                                   "field": "count",
                                   "scale": {"domain": [0, 100000000]},
                                   "title": "Total Traffic",
                                   "axis": {"format": "s"},
                                   "sort": "descending"
                               },
                               "color": {
                                   "field": "is_weekend",
                                   "scale": {"range": ["#52b69a", "#d9ed92"]},
                                   "legend": None
                               }
                           }
                       }, {
                           "width": 20,
                           "view": {"stroke": None},
                           "mark": {
                               "type": "text",
                               "align": "center"
                           },
                           "encoding": {
                               "y": {"field": "hour_bin", "type": "ordinal", "axis": None, "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"]},
                               "text": {"field": "hour_bin", "type": "text"}
                           }
                       }, {
                           "transform": [{
                               "filter": {"field": "type", "equal": "exit"}
                           }],
                           "title": {"text": "Exits", "anchor": "middle"},
                           "mark": "bar",
                           "encoding": {
                               "y": {
                                   "field": "hour_bin", "title": None,
                                   "axis": None, "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"]
                               },
                               "x": {
                                   "aggregate": "sum",
                                   "field": "count",
                                   "title": "Total Traffic",
                                   "scale": {"domain": [0, 100000000]},
                                   "axis": {"format": "s"}
                               },
                               "color": {
                                   "field": "is_weekend",
                                   "legend": None
                               }
                           }
                       }],
                       "config": {
                           "view": {"stroke": None},
                           "axis": {"grid": False}
                       }
                   }


                   )

st.vega_lite_chart(entry_exit_ratios,
                   {
                       "mark": {"type": "bar", "color": "#28666e"},

                       "title": {"text": "Turnstile Entry to Exit Ratio", "anchor": "middle"},

                       "encoding": {
                           "tooltip": [
                               {"field": "observed_at",
                                   "type": "text", "title": "Month"},
                               {"field": "ratio", "type": "quantitative",
                                   "title": "Ratio"},
                               {"field": "diff", "type": "quantitative",
                                   "title": "Diff"},

                           ],
                           "x": {
                               "field": "observed_at", "type": "temporal",
                               "title": None,
                               "axis": {
                                   "domain": False,
                                   "ticks": False,
                                   "labelAngle": 0,
                                   "labelPadding": 2
                               }
                           },
                           "y": {
                               "title": {"text": "Entry-to-Exit Ratio", "anchor": "middle"},
                               "field": "diff", "type": "quantitative",
                               "axis": {
                                   "gridColor": {
                                       "condition": {"test": "datum.diff === 1", "value": "black"},
                                       "value": "#ddd"
                                   }
                               }
                           }
                       }
                   }
                   )

st.vega_lite_chart(bubble_chart_data,
                   {
                       "title": {"text": "Traffic compared to Turnstile and Line Count", "anchor": "middle"},
                       "width": 500, "height": 400,

                       "params": [{
                           "name": "view",
                           "select": "interval",
                           "bind": "scales"
                       }],
                       "mark": "circle",


                       "encoding": {
                           "y": {
                               "field": "net_traffic",
                               "type": "quantitative",
                               "scale": {"zero": False},
                               "title": "Traffic",
                               "axis": {"minExtent": 30}
                           },
                           "x": {
                               "field": "unit_id",
                               "title": "Turnstile Count",
                           },
                           "size": {"field": "num_lines", "type": "quantitative", "title": "Lines Count"},
                           "color": {"value": "#90be6d"},
                           "tooltip": [
                               {"field": "STATION", "type": "text",
                                   "title": "Station"},
                               {"field": "LINENAME", "type": "text",
                                   "title": "Line Names"},
                               {"field": "num_lines", "type": "quantitative",
                                   "title": "Lines Count"},
                               {"field": "unit_id", "type": "quantitative",
                                   "title": "Turnstile Count"},
                               {"field": "net_traffic", "type": "quantitative",
                                   "title": "Total Traffic"}

                           ],
                       }
                   }
                   )


st.vega_lite_chart(subway_entry_heatmap,
                   {
                       "title": {"text": "Turnstile Entries", "subtitle": "By Day of Week and Time Bucket.", "anchor": "middle"},
                       "mark": "rect",
                       "width": 500,
                       "height": 300,
                       "encoding": {
                           "tooltip": [
                               {"field": "weekday", "type": "text", "title": "Day"},
                               {"field": "hour_bin", "type": "text", "title": "Time"},
                               {"field": "count", "type": "quantitative",
                                   "title": "Traffic"},
                           ],
                           "x": {
                               "title": None,
                               "field": "weekday",
                               "type": "ordinal",
                               "sort": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                           },
                           "y": {
                               "title": None,
                               "field": "hour_bin",
                               "type": "ordinal",
                               "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"]
                           },
                           "color": {
                               "title": "Traffic",
                               "field": "count",
                               "type": "quantitative",
                               "scale": {"domain": [3500000, 17000000], "range": ["#c7f9cc", "#264653"]}
                           }
                       },
                       "config": {

                       }
                   }
                   )

st.vega_lite_chart(subway_exit_heatmap,
                   {
                       "title": {"text": "Turnstile Exits", "subtitle": "By Day of Week and Time Bucket.", "anchor": "middle"},
                       "mark": "rect",
                       "width": 500,
                       "height": 300,
                       "encoding": {
                           "tooltip": [
                               {"field": "weekday", "type": "text", "title": "Day"},
                               {"field": "hour_bin", "type": "text", "title": "Time"},
                               {"field": "count", "type": "quantitative",
                                   "title": "Traffic"},
                           ],
                           "x": {
                               "title": None,
                               "field": "weekday",
                               "type": "ordinal",
                               "sort": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
                           },
                           "y": {
                               "title": None,
                               "field": "hour_bin",
                               "type": "ordinal",
                               "sort": ["12am-6am", "6am-12pm", "12pm-6pm", "6pm-12am"]
                           },
                           "color": {
                               "title": "Traffic",
                               "field": "count",
                               "type": "quantitative",
                               "scale": {"domain": [3500000, 17000000], "range": ["#c7f9cc", "#264653"]}
                           }
                       },
                       "config": {

                       }
                   }
                   )


st.vega_lite_chart(top_bottom_ten_station_traffic,
                   {
                       "title": {"text": "Top and Bottom 10 Stations", "subtitle": "Ranked by total turnstile traffic.", "anchor": "middle"},
                       "transform": [
                           {
                               "window": [{
                                   "op": "rank",
                                   "as": "rank"
                               }],
                               "sort": [{"field": "net_traffic", "order": "descending"}]
                           }
                       ],
                       "mark": "bar",

                       "encoding": {
                           "x": {
                               "title": "Traffic",
                               "field": "net_traffic",
                               "type": "quantitative"
                           },
                           "y": {
                               "title": "Station",
                               "field": "STATION",
                               "type": "ordinal",
                               "sort": {"field": "net_traffic", "op": "average", "order": "descending"}
                           },
                           "tooltip": [
                               {"field": "STATION", "type": "text",
                                   "title": "Station"},
                               {"field": "LINENAME", "type": "text",
                                   "title": "Subway Lines"},
                               {"field": "unit_id", "type": "quantitative",
                                   "title": "Turnstile Count"},
                               {"field": "net_traffic", "type": "quantitative",
                                   "title": "Total Traffic"}

                           ],
                           "color": {
                               "field": "category",
                               "scale": {"range": ["#31688e", "#35b779"]},
                               "legend": None
                           }
                       }
                   })

st.vega_lite_chart(penn_box_plots, {
    "title": {"text": "Penn Station - 34th Street", "subtitle": "Station with the highest traffic.", "anchor": "middle"},
    "description": "Penn Station is the subway station with the highest overall traffic",
    "hconcat": [{
        "title": {"text": "Traffic by Day Of Week", "anchor": "middle"},
        "width": 300,
        "transform": [{
            "filter": {"field": "plot", "equal": "week"}
        }],

        "encoding": {"y": {
            "field": "weekday",
            "type": "nominal",
            "title": None,
            "sort": ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        },
            "tooltip": [
            {"field": "weekday", "type": "text", "title": "Day"},
            {"field": "min", "type": "quantitative", "title": "Min"},
            {"field": "25%", "type": "quantitative", "title": "25%"},
            {"field": "75%", "type": "quantitative", "title": "75%"},
            {"field": "max", "type": "quantitative", "title": "Max"},
            {"field": "median", "type": "quantitative", "title": "Median"},
            {"field": "mean", "type": "quantitative", "title": "Mean"},
            {"field": "std", "type": "quantitative",
             "title": "Standard Deviation"}
        ],
        },

        "layer": [
            {
                "mark": {"type": "rule", "color": "#003d5b"},
                "encoding": {
                    "x": {"field": "min", "type": "quantitative", "scale": {"zero": False}, "title": None},
                    "x2": {"field": "max"}
                }
            },
            {
                "mark": {"type": "bar", "size": 14},

                "encoding": {
                    "x": {"field": "25%", "type": "quantitative"},
                    "x2": {"field": "75%"},
                    "color": {"field": "weekday", "type": "nominal", "legend": None, "scale": {"range": ["#440154", "#443983", "#31688e", "#21918c", "#35b779", "#90d743", "#fde725"]}}
                }
            },
            {
                "mark": {"type": "tick", "color": "white", "size": 14},
                "encoding": {
                    "x": {"field": "median", "type": "quantitative"}
                }

            }
        ]
    }, {


        "transform": [{
            "filter": {"field": "plot", "equal": "month"}
        }],
        "title": {"text": "Traffic by Month", "anchor": "middle"},
        "width": 300,

        "encoding": {"y": {
            "field": "observed_at",
            "type": "nominal",
            "title": None,
            "sort": ["January", "February", "March", "April", "May", "June"]
        },
            "tooltip": [
            {"field": "observed_at", "type": "text", "title": "Month"},
            {"field": "min", "type": "quantitative", "title": "Min"},
            {"field": "25%", "type": "quantitative", "title": "25%"},
            {"field": "75%", "type": "quantitative", "title": "75%"},
            {"field": "max", "type": "quantitative", "title": "Max"},
            {"field": "median", "type": "quantitative", "title": "Median"},
            {"field": "mean", "type": "quantitative", "title": "Mean"},
            {"field": "std", "type": "quantitative",
             "title": "Standard Deviation"}
        ],
        },

        "layer": [
            {
                "mark": {"type": "rule"},
                "encoding": {
                    "x": {"field": "min", "type": "quantitative", "scale": {"zero": False}, "title": None},
                    "x2": {"field": "max"}
                }
            },
            {
                "mark": {"type": "bar", "size": 14},

                "encoding": {
                    "x": {"field": "25%", "type": "quantitative"},
                    "x2": {"field": "75%"},
                    "color": {"field": "observed_at", "type": "nominal", "legend": None}
                }
            },
            {
                "mark": {"type": "tick", "color": "white", "size": 14},
                "encoding": {
                    "x": {"field": "median", "type": "quantitative"}
                }

            }
        ]




    }
    ]

})
