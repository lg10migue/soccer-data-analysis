import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets.
players_df = pd.read_csv("data/players_20_21.csv")
match_results_df = pd.read_csv("data/results_20_21.csv")

# Question 1: What are the top scorers and assisters in the Premier League 20/21?

# Get the top 10 goal scorers by sorting the data frame by the Goals column.
top_scorers = (
    players_df[["Name", "Club", "Goals"]]
    .sort_values(by="Goals", ascending=False)
    .head(10)
)

# Get the top 10 assisters, similar to the top scorers, but using the Assists column instead of Goals.
top_assisters = (
    players_df[["Name", "Club", "Assists"]]
    .sort_values(by="Assists", ascending=False)
    .head(10)
)

# Prepare the charts.
sns.set_theme(style="whitegrid")

# Create the top scorers visualization.
plt.figure(figsize=(10, 6))
sns.barplot(data=top_scorers, x="Goals", y="Name", palette="viridis", hue="Club")
plt.title("Top 10 Goal Scorers in Premier League 20/21")
plt.xlabel("Goals")
plt.ylabel("Player Name")
plt.show()

# Create the top assisters visualization.
plt.figure(figsize=(10, 6))
sns.barplot(data=top_assisters, x="Assists", y="Name", palette="viridis", hue="Club")
plt.title("Top 10 Assisters in Premier League 20/21")
plt.xlabel("Assists")
plt.ylabel("Player Name")
plt.show()

# Question 2: What is the location impact on the match results?

# Determine the outcome of the match based on the goals scored by the home and away teams.
match_results_df["Outcome"] = match_results_df.apply(
    lambda row: (
        "Home Win"
        if row["Full Time Home Goals"] > row["Full Time Away Goals"]
        else (
            "Away Win"
            if row["Full Time Away Goals"] > row["Full Time Home Goals"]
            else "Draw"
        )
    ),
    axis=1,
)

# Calculate the total number of each outcome for home and away teams.
outcome_counts = match_results_df["Outcome"].value_counts()

# Calculate the win rates.
total_matches = outcome_counts.sum()
home_win_rate = outcome_counts["Home Win"] / total_matches * 100
away_win_rate = outcome_counts["Away Win"] / total_matches * 100

# Prepare the data for the visualization.
labels = ["Home Win", "Away Win", "Draw"]
sizes = [outcome_counts["Home Win"], outcome_counts["Away Win"], outcome_counts["Draw"]]
colors = ["lightcoral", "lightskyblue", "lightgreen"]
explode = (0.1, 0, 0)

# Create the Home vs. Away visualization.
plt.figure(figsize=(7, 7))
plt.pie(
    sizes,
    explode=explode,
    labels=labels,
    colors=colors,
    autopct="%1.1f%%",
    shadow=True,
    startangle=140,
)
plt.axis("equal")
plt.title("Home vs. Away Win Rate - Premier League 20/21")
plt.show()

# Question 3: What is the relationship between goals scored and assists provided by players?

# Aggregate goals and assists for each player.
players_stats = (
    players_df.groupby("Name").agg({"Goals": "sum", "Assists": "sum"}).reset_index()
)

# Create the Goals vs. Assists visualization.
plt.figure(figsize=(10, 6))
plt.scatter(players_df["Goals"], players_df["Assists"], alpha=0.5)
plt.title("Goals vs. Assists for Players - Premier League 20/21")
plt.xlabel("Total Goals")
plt.ylabel("Total Assists")
plt.grid(True)

# Highlight the top performers.
top_5_scorers = players_stats.sort_values(by="Goals", ascending=False).head(5)
top_5_assisters = players_stats.sort_values(by="Assists", ascending=False).head(5)

# Loop through the top 5 scorers and assisters to label them on the chart.
for i, row in top_5_scorers.iterrows():
    plt.text(
        row["Goals"], row["Assists"], row["Name"], fontsize=9, color="blue", ha="right"
    )

for i, row in top_5_assisters.iterrows():
    plt.text(
        row["Goals"], row["Assists"], row["Name"], fontsize=9, color="red", ha="left"
    )

plt.show()
