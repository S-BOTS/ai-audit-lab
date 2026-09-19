import pandas as pd

journal = pd.read_csv("data/journal.csv")
journal["Posting_Date"] = pd.to_datetime(journal["Posting_Date"])
print(journal.head())
print("Total journal entries:", len(journal))
print("\n Journal Fields:" )
print(journal.columns)
print("\n Journal Data Types:")
print(journal.dtypes)
weekend_entries = journal[journal["Posting_Date"].dt.weekday >= 5]
print("\n Weekend Journal Entries:")
print(weekend_entries)
duplicate_entries = journal[journal.duplicated(subset=["Posting_Date","Account","Description","Amount","Prepared_By"], keep=False)]
print("\n Duplicate Journal Entries:")
print(duplicate_entries)
round_entries = journal[journal["Amount"] % 1000 == 0]
print("\n Round-DollarJournal Entries:")
print(round_entries)
high_value_entries = journal[journal["Amount"] >= 5000]
print("\n High-Value Journal Entries:")
print(high_value_entries)
# Calculate risk scores
journal["Risk_Score"] = 0 
journal["Risk_Reasons"] = ""
# ...your four risk tests...
journal.loc[journal["Posting_Date"].dt.weekday >= 5, "Risk_Score"] += 1
journal.loc[journal["Posting_Date"].dt.weekday >= 5, "Risk_Reasons"] += "Weekend Posting; "
journal.loc[journal["Amount"] % 1000 == 0, "Risk_Score"] += 1
journal.loc[journal["Amount"] % 1000 == 0, "Risk_Reasons"] += "Round Dollar; "
journal.loc[journal["Amount"] >= 5000, "Risk_Score"] += 1
journal.loc[journal["Amount"] >= 5000, "Risk_Reasons"] += "High Value; "
journal.loc[duplicate_entries.index, "Risk_Score"] += 1
journal.loc[duplicate_entries.index, "Risk_Reasons"] += "Potential Duplicate; "
# Assign risk levels
journal["Risk_Level"] = "Low"
journal.loc[journal["Risk_Score"] >= 1, "Risk_Level"] = "Medium"
journal.loc[journal["Risk_Score"] >= 3, "Risk_Level"] = "High"
risk_report = journal.sort_values(by="Risk_Score", ascending=False)
print("\nPrioritized Audit Risk Report:")
print(risk_report[["Journal_ID","Posting_Date","Amount","Prepared_By","Risk_Score","Risk_Level","Risk_Reasons"]])
risk_report.to_excel("output/audit_risk_report.xlsx", index=False)
print("\nAudit risk report exported successfully.")
