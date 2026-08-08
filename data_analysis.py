#data_analysis.py: takes csv with data, cleans data and outputs matrices
import numpy as np
import pandas as pd

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

grouped_stats["Mean_Time"] = grouped_stats["Mean_Time"].round(2)
grouped_stats["Median_Time"] = grouped_stats["Median_Time"].round(2)
grouped_stats["Std_Dev"] = grouped_stats["Std_Dev"].round(2)
grouped_stats["Forfeit_Rate"] = grouped_stats["Forfeit_Rate"].round(1)

forfeit_matrix = pd.pivot_table(
    grouped_stats, values="Forfeit_Rate", index="overworld_seed", columns="elo_tier"
)

median_time_matrix = pd.pivot_table(
    grouped_stats, values="Median_Time", index="overworld_seed", columns="elo_tier"
)

print(" 1. FULL BREAKDOWN BY ELO TIER AND OVERWORLD SEED ")
print(grouped_stats.to_string(index=False))

print(" 2. FORFEIT RATE MATRIX (%) BY RANK ")
print(forfeit_matrix.to_string())

print(" 3. MEDIAN WINNING TIME MATRIX (MINUTES) BY RANK ")
print(median_time_matrix.to_string())
