import pandas as pd
import os

BASE_DIR = r"C:\Users\DELL\PycharmProjects\Project_1"
data_dir = os.path.join(BASE_DIR, "data")
output_dir = os.path.join(BASE_DIR, "output")

os.makedirs(output_dir, exist_ok=True)

file_path = os.path.join(data_dir, "dex-temp-db.score_v4.csv")

df = pd.read_csv(file_path)

print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())

score_columns = [col for col in df.columns if "score" in col.lower() or "lp_category_breakdown" in col.lower()]
print("\nScore Columns:", score_columns)

if "total_deposit_usd" in df.columns:
    deposit_vs_score = df["aggregated_lp_score"].corr(df["total_deposit_usd"])
else:
    deposit_vs_score = None

print("\nCorrelation between deposits and scores:", deposit_vs_score)

anomalies = []

if "aggregated_lp_score" in df.columns:
    bad_scores = df[(df["aggregated_lp_score"] < 0) | (df["aggregated_lp_score"] > 1)]
    if not bad_scores.empty:
        anomalies.append(("Invalid score range", bad_scores))

missing_scores = df[score_columns].isnull().sum()
print("\nMissing values in score columns:\n", missing_scores)

if {"aggregated_lp_score", "lp_category_breakdown_score"}.issubset(df.columns):
    mismatch = df[abs(df["aggregated_lp_score"] - df["lp_category_breakdown_score"]) > 0.2]
    if not mismatch.empty:
        anomalies.append(("Mismatch between aggregated & breakdown scores", mismatch))

if anomalies:
    anomaly_report = pd.concat([a[1] for a in anomalies])
    anomaly_report_path = os.path.join(output_dir, "anomalies_report.csv")
    anomaly_report.to_csv(anomaly_report_path, index=False)
    print(f"\n Anomaly report saved to: {anomaly_report_path}")
else:
    print("\n No major anomalies detected.")
