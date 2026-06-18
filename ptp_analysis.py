import pandas as pd

# 1. Sample data directly in code
data = {
    'customer_id': ['C001','C002','C003','C004','C005','C006','C007','C008','C009','C010'],
    'ptp_date': ['2026-04-15','2026-04-18','2026-04-14','2026-04-22','2026-04-12','2026-04-25','2026-04-26','2026-04-17','2026-04-21','2026-04-23'],
    'receipt_date': ['2026-04-15','2026-04-20','2026-04-13',None,'2026-04-12','2026-04-24','2026-04-28','2026-04-17',None,'2026-04-23'],
    'ptp_amount': [20000,30000,15000,25000,10000,40000,20000,18000,22000,12000],
    'receipt_amount': [20000,30000,15000,0,10000,40000,20000,18000,0,12000]
}

df = pd.DataFrame(data)

# 2. Convert dates
df['ptp_date'] = pd.to_datetime(df['ptp_date'])
df['receipt_date'] = pd.to_datetime(df['receipt_date'], errors='coerce')

# 3. Check if PTP was kept: paid on/before PTP date AND full amount
df['ptp_kept'] = (df['receipt_date'].notna()) & \
                 (df['receipt_date'] <= df['ptp_date']) & \
                 (df['receipt_amount'] >= df['ptp_amount'])

# 4. Calculate Score
total_ptps = len(df)
ptps_kept = df['ptp_kept'].sum()
ptp_score = round(ptps_kept * 100 / total_ptps, 2)

print(f"Total PTPs: {total_ptps}")
print(f"PTPs Kept: {ptps_kept}")
print(f"PTP Reliability Score: {ptp_score}%")

# Show summary of who kept vs broke PTP
summary = df[['customer_id','ptp_date','receipt_date','ptp_amount','receipt_amount','ptp_kept']]
print(summary)

# Optional: split into two groups
kept_ptps = summary[summary['ptp_kept']]
broken_ptps = summary[~summary['ptp_kept']]

print("\nCustomers who kept PTPs:")
print(kept_ptps)

print("\nCustomers who broke PTPs:")
print(broken_ptps)

# Categorize outcomes
def categorize(row):
    if row['ptp_kept']:
        return "Kept"
    elif pd.isna(row['receipt_date']):
        return "No Payment"
    elif row['receipt_date'] > row['ptp_date'] and row['receipt_amount'] >= row['ptp_amount']:
        return "Late but Full"
    elif row['receipt_amount'] < row['ptp_amount'] and row['receipt_date'] <= row['ptp_date']:
        return "On Time but Partial"
    else:
        return "Late and/or Partial"

df['ptp_status'] = df.apply(categorize, axis=1)

print(df[['customer_id','ptp_date','receipt_date','ptp_amount','receipt_amount','ptp_status']])

import matplotlib.pyplot as plt

# Count each status
status_counts = df['ptp_status'].value_counts()

# --- Bar Chart ---
plt.figure(figsize=(8,5))
status_counts.plot(kind='bar', color=['green','red','orange','blue','purple'])
plt.title("Breakdown of PTP Statuses")
plt.xlabel("PTP Status")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Pie Chart ---
plt.figure(figsize=(6,6))
status_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green','red','orange','blue','purple'])
plt.title("PTP Status Distribution")
plt.ylabel("")  # Hide y-label
plt.show()


plt.figure(figsize=(8,5))
ax = status_counts.plot(kind='bar', color=['green','red','orange','blue','purple'])
plt.title("Breakdown of PTP Statuses")
plt.xlabel("PTP Status")
plt.ylabel("Number of Customers")
plt.xticks(rotation=45)

# Add labels on top of bars
for i, v in enumerate(status_counts):
    ax.text(i, v + 0.1, str(v), ha='center')

plt.tight_layout()
plt.show()
