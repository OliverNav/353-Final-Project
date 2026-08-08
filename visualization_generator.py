import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

#what I could do:
#heatmaps for matrices, linear line to see time increase, box plots to see variance/outliers, histogram?, linechart instead of linear line
#any other ideas I think of: 

OUTPUT_DIR = "results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv("mcsr_matches_dataset.csv")

#not sure if I want to worry about coal 1, coal 2 ... 
#might make bucket sizes too small and not necessary
rank_value = [0, 600, 900, 1200, 1500, 1800, 3000]
rank_name = ["Coal", "Iron", "Gold", "Emerald", "Diamond", "Netherite"]
df["elo_tier"] = pd.cut(df["avg_elo"], bins=rank_value, labels=rank_name, right=False)

df["winning_time_min"] = np.where(df["is_forfeited"] == False, df["winning_time_sec"] / 60.0, np.nan)

#forfeit_rate is tricky, look into more
grouped_stats = (
    df.groupby(["elo_tier", "overworld_seed"], observed=False)
    .agg(
        Sample_Size=("match_id", "count"),
        Completed_Count=("winning_time_min", "count"),
        Mean_Time=("winning_time_min", "mean"),
        Median_Time=("winning_time_min", "median"),
        Std_Dev=("winning_time_min", "std"),
        Forfeit_Rate=("is_forfeited", lambda x: (x.mean() * 100)),
    )
    .reset_index()
)

grouped_stats = grouped_stats[grouped_stats["Sample_Size"] > 0].copy()
grouped_stats["Median_Time"] = grouped_stats["Median_Time"].round(2)
grouped_stats["Forfeit_Rate"] = grouped_stats["Forfeit_Rate"].round(1)

sns.set_theme(style="whitegrid", font="sans-serif")
palette = sns.color_palette("tab10")


#vis1 finish time heatmap 

time_matrix = pd.pivot_table(grouped_stats, values="Median_Time", index="overworld_seed", columns="elo_tier")

plt.figure(figsize=(9, 5))
sns.heatmap(
    time_matrix,
    annot=True,
    fmt=".1f",
    cmap="coolwarm",
    cbar_kws={"label": "Median Time (Minutes)"},
)
plt.title("Median Completion Time by Seed and Rank", fontweight="bold")
plt.xlabel("Elo Rank Tier")
plt.ylabel("Overworld Seed Structure")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "1_median_time_heatmap.png"), dpi=300)
plt.close()



# vis2 ff heatmap

forfeit_matrix = pd.pivot_table(
    grouped_stats, values="Forfeit_Rate", index="overworld_seed", columns="elo_tier"
)

plt.figure(figsize=(9, 5))
sns.heatmap(
    forfeit_matrix,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    cbar_kws={"label": "Forfeit Rate (%)"},
)
plt.title("Forfeit Rate by Seed and Rank", fontweight="bold")
plt.xlabel("Elo Rank Tier")
plt.ylabel("Overworld Seed Structure")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "2_forfeit_rate_heatmap.png"), dpi=300)
plt.close()


# vis3 elo slope line

plt.figure(figsize=(11, 6))

sns.lineplot(
    data=grouped_stats,
    x="elo_tier",
    y="Median_Time",
    hue="overworld_seed",
    marker="o",
    markersize=8,
    linewidth=2.5,
)

plt.title("Median Winning Time Progression Across Ranks", fontweight="bold")
plt.xlabel("Elo Rank Tier")
plt.ylabel("Median Winning Time (Minutes)")
plt.legend(title="Overworld Seed", loc="upper right", frameon=True)
plt.grid(True, linestyle="--")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "3_rank_progression_lines.png"), dpi=300)
plt.close()



# vis4 box plot of completions
completed_df = df[df["is_forfeited"] == False].copy()

plt.figure(figsize=(14, 6))

sns.boxplot(
    data=completed_df,
    x="elo_tier",
    y="winning_time_min",
    hue="overworld_seed",
    showmeans=True,
    meanprops={"marker": "o", "markerfacecolor": "white", "markeredgecolor": "black"}
)

plt.title("Winning Time Variance with Outliers Across Ranks", fontweight="bold")
plt.xlabel("Elo Rank Tier")
plt.ylabel("Winning Time (Minutes)")
plt.legend(title="Overworld Seed", loc="upper right")
plt.grid(axis="y", linestyle="--")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "4_time_distributions_boxplot.png"), dpi=300)
plt.close()