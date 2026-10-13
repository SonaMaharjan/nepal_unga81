# import os
#print(os.getcwd())

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

# Go from main to UNGA, then into figures
output_dir = Path("../figures")

# Create the folder if it doesn't already exist
output_dir.mkdir(parents=True, exist_ok=True)

meetings = pd.read_csv("../data/meetings.csv")
events = pd.read_csv("../data/events.csv")

# converting date type

meetings["Date"] = meetings["Date"].replace("25", "25 Sep")
meetings["Date"] = meetings["Date"].str.strip()
# print(meetings["Date"].unique())
meetings["Date"] = pd.to_datetime(meetings["Date"] + "2026")
# print(meetings["Date"].dtype)


print(events["Date"].unique())
events["Date"]=pd.to_datetime(events["Date"]+"2026")
print(events["Date"].dtype)

####
# How many meetings took place on each day?
print("Number of meetings per day",meetings["Date"].value_counts())
print("Number of events per day",events["Date"].value_counts())

# What types of meetings did Nepal have, and how many of each type were there?
print("Types of meetings",meetings["Meeting_type"].value_counts())
print("Types of events",events["Event_type"].value_counts())

# Which regions did Nepal engage with most frequently through meetings?
print("Regions enaged in meetings",meetings["Region"].value_counts())
print("Continents enaged in meetings",meetings["Continent"].value_counts())

# How did meeting type vary by date?
print("Meeting type by date \n", pd.crosstab(meetings["Date"], meetings["Meeting_type"]))


####
# What issues appeared most frequently in Nepal's documented bilateral meetings, and how did those issues vary across counterparts/regions?

new_meetings_bilateral = (meetings[meetings["Meeting_type"] == "Bilateral"]).copy()
new_meetings = meetings.copy()


new_meetings["Topics"] = new_meetings["Topics"].str.split(", ")
# print(new_meetings.shape)

new_meetings = new_meetings.explode("Topics")
print("\nTotal topic frequency for bilateral\n", new_meetings["Topics"].value_counts())

new_meetings_count = (
    new_meetings.groupby(["Region", "Topics"])
       .size()
       .reset_index(name="Count")
)
print("\nTotal meetings count Region x Topics\n", new_meetings_count.sort_values(by="Count", ascending=False))
# print(new_count)

####
# Which issues did Nepal emphasise in multilateral forums?
# print(events["Topics"].unique())
new_events = events.copy()

new_events["Topics"]=new_events["Topics"].str.split("; ")
new_events = new_events.explode("Topics")

print("\nTopics in Events\n",new_events["Topics"].value_counts())

new_events_count = (
	new_events.groupby(["Event_type", "Topics"])
	.size()
	.reset_index(name="Count")
)
print("\nEvent Type x Topics \n", new_events_count.sort_values(by="Count", ascending=False))
print("\nTypes of roles in events \n", events["Role"].value_counts(dropna=False))

# Which topics occur in both datasets?
meetings_set = set(new_meetings["Topics"])
events_set = set(new_events["Topics"])

meetings_events = meetings_set.intersection(events_set)

print("The shared topics are:\n",meetings_events)

shared_meetings = new_meetings[new_meetings["Topics"].isin(meetings_events)]
shared_events = new_events[new_events["Topics"].isin(meetings_events)]

# print("Frequency of shared meetings\n", shared_meetings["Topics"].value_counts(), '  ', shared_events["Topics"].value_counts())
# bilateral_total = meetings["Meeting_type"].sum()
# multilateral_total = events["Event_type"].sum()

meetings_counts = (shared_meetings["Topics"].value_counts()/len(meetings)*100).round(1)
events_counts = (shared_events["Topics"].value_counts()/len(events)*100).round(1)

meetings_counts.name = "Meetings"
events_counts.name = "Events"

shared_table = pd.concat(
    [meetings_counts, events_counts],
    axis = 1
)

print(shared_table)

print(meetings_set.difference(events_set))
print(events_set.difference(meetings_set))

# 1. Shared diplomatic topics: Meetings vs Events

sns.set_theme(style="whitegrid")

shared_long = (shared_table.reset_index().melt(id_vars="Topics", var_name="Engagement Type", value_name="Percentage"))

fig, ax = plt.subplots(figsize=(11, 6))

sns.barplot(
    data=shared_long,
    x="Percentage",
    y="Topics",
    hue="Engagement Type",
    ax=ax
)

for i in ax.containers:
    ax.bar_label(i, fmt="%.1f%%", padding=3)

ax.set_title(
    "Shared Diplomatic Topics: Bilateral Meetings vs Multilateral Events",
    fontsize=14,
    fontweight="bold",
    pad=20
)
ax.set_xlabel("Percentage of documented engagements")
ax.set_ylabel("")
ax.legend(title="Engagement Type")

plt.tight_layout()
plt.savefig(output_dir / "topics_comparison.svg",
            bbox_inches="tight")

plt.show()


# 2. Diplomatic activity over time

meeting_daily = meetings.groupby("Date").size().rename("Meetings")
event_daily = events.groupby("Date").size().rename("Events")

daily_activity = pd.concat([meeting_daily, event_daily],axis=1).fillna(0).astype(int).sort_index()

daily_long = daily_activity.reset_index().melt(id_vars="Date", var_name="Engagement Type", value_name="Count")

fig, ax = plt.subplots(figsize=(11, 5))

sns.lineplot(
    data=daily_long,
    x="Date",
    y="Count",
    hue="Engagement Type",
    marker="o",
    linewidth=2.5,
    estimator=None,
    ax=ax
)

ax.set_title(
    "Nepal's Documented Diplomatic Activity at UNGA 2026",
    fontsize=14,
    fontweight="bold"
)
ax.set_xlabel("Date")
ax.set_ylabel("Number of engagements")
ax.set_ylim(bottom=0)
ax.set_xticks(daily_activity.index)
ax.tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig(output_dir / "daily_activity.svg",
            bbox_inches="tight")
plt.show()

# 3. Geographic distribution of meetings

continent_counts = (meetings["Continent"].value_counts().reset_index())

continent_counts.columns = ["Continent", "Count"]

fig, ax = plt.subplots(figsize=(10, 5))

sns.barplot(
    data=continent_counts,
    x="Count",
    y="Continent",
    color="steelblue",
    ax=ax
)

for container in ax.containers:
    ax.bar_label(container, padding=3)

ax.set_title(
    "Geographic Distribution of Nepal's UNGA Meetings",
    fontsize=14,
    fontweight="bold"
)
ax.set_xlabel("Number of meetings")
ax.set_ylabel("")
ax.set_xlim(0, continent_counts["Count"].max() * 1.2)

plt.tight_layout()

plt.savefig(
    output_dir / "geographic_distribution.svg",
    format="svg",
    bbox_inches="tight",
    transparent=True
)
plt.show()

# 4. Most frequently documented topics

meeting_topics = (
    new_meetings["Topics"]
    .dropna()
    .value_counts()
    .rename("Meetings")
)

event_topics = (
    new_events["Topics"]
    .dropna()
    .value_counts()
    .rename("Events")
)

topic_counts = pd.concat(
    [meeting_topics, event_topics],
    axis=1
).fillna(0)

topic_counts = topic_counts.drop(
    index="Bilateral relations",
    errors="ignore"
)

topic_counts["Total"] = (
    topic_counts["Meetings"] + topic_counts["Events"]
)

top_topics = topic_counts.nlargest(10, "Total").drop(
    columns="Total"
)

top_long = (
    top_topics
    .reset_index()
    .rename(columns={"index": "Topics"})
    .melt(
        id_vars="Topics",
        var_name="Engagement Type",
        value_name="Count"
    )
)

fig, ax = plt.subplots(figsize=(11, 7))

sns.barplot(
    data=top_long,
    x="Count",
    y="Topics",
    hue="Engagement Type",
    ax=ax
)

for container in ax.containers:
    ax.bar_label(container, fmt="%.0f", padding=3)

ax.set_title(
    "Most Frequently Documented Topics at UNGA 2026",
    fontsize=14,
    fontweight="bold"
)
ax.set_xlabel("Number of engagements mentioning topic")
ax.set_ylabel("")
ax.set_xlim(0, top_long["Count"].max() * 1.2)

plt.tight_layout()

plt.savefig(output_dir / "topics_discussed.svg",
            bbox_inches="tight")
plt.show()

# 5. Interactive world map of Nepal's diplomatic counterparts

# Check the available columns first
print(meetings.columns.tolist())

country_counts = (
    meetings["Country"]
    .dropna()
    .value_counts()
    .reset_index()
)

country_counts.columns = ["Country", "Meetings"]

fig = px.choropleth(
    country_counts,
    locations="Country",
    locationmode="country names",
    color="Meetings",
    hover_name="Country",
    color_continuous_scale="Viridis",
    title="Nepal's Documented Diplomatic Engagements at UNGA 2026"
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    ),
    margin=dict(l=0, r=0, t=60, b=0)
)

fig.show()

