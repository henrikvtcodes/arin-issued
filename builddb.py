import pandas as pd
import os, gzip,json

archives = []

for thing in os.listdir('archives'):
    if thing.endswith('.txt.gz'):
        archives.append(thing)

print(f"Found {archives}")

summaryColumns = ['year','month','date','action','resourceType','resource']
summaries = pd.DataFrame(columns=summaryColumns)

def make_row(year, month, date, action, resourceType, resource):
    report = {
        'year':year,
        'month':month,
        'date':pd.to_datetime(date),
        'action':action,
        'resourceType':resourceType,
        'resource':resource
    }
    return report

for thing in archives:
    yearmonth = thing.split('.')[0]
    year = yearmonth.split('-')[0]
    month = yearmonth.split('-')[1]
    with gzip.open(thing, 'rt') as f:
        reportStrs = f.read().split("-------------- next part --------------")
        for reportStr in reportStrs:
            rows = []
            date = ""
            for line in reportStr.split("\n"):
                if line.startswith("Date:"):
                    date = line[5:].strip()[:-5].strip()
                # Handle ASNs/IPs taken back by ARIN
                elif line.startswith("Remove "):
                    resource = line.split(" ")[1]
                    if resource.startswith("AS"):
                        rows.append(make_row(year, month, date, "Remove", "ASN", resource))
                    else:
                        rows.append(make_row(year, month, date, "Remove", "IP", resource))
                # Handle ASNs/IPs issued by ARIN
                elif line.startswith("Add "):
                    resource = line.split(" ")[1]
                    if resource.startswith("AS"):
                        rows.append(make_row(year, month, date, "Add", "ASN", resource))
                    else:
                        rows.append(make_row(year, month, date, "Add", "IP", resource))
            print(f"Completed report for {date}")
            summaries = pd.concat([summaries, pd.DataFrame(rows)], ignore_index=True)

with open("summary.json", "w") as f:
    f.write(summaries.to_json(orient='records', indent=2))

summaries.to_csv('summary.csv', index=False)