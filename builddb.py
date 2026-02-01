import json
import os, gzip

archives = []

for thing in os.listdir('.'):
    if thing.endswith('.txt.gz'):
        archives.append(thing)

print(f"Found {archives}")

summaries = {}

for thing in archives:
    yearmonth = thing.split('.')[0]
    year = yearmonth.split('-')[0]
    month = yearmonth.split('-')[1]
    summary = {
        'year': year,
        'month': month,
        'reports': []
    }
    with gzip.open(thing, 'rt') as f:
        reportStrs = f.read().split("-------------- next part --------------")
        for reportStr in reportStrs:
            report = {
                'date': "",
                'ASN_add': [],
                'ASN_rm': [],
                'IPRange_add': [],
                'IPRange_rm': [],
            }
            for line in reportStr.split("\n"):
                if line.startswith("Date:"):
                    report['date'] = line[5:].strip()
                elif line.startswith("Remove "):
                    resource = line.split(" ")[1]
                    if resource.startswith("AS"):
                        report['ASN_rm'].append(resource)
                    else:
                        report['IPRange_rm'].append(resource)
                elif line.startswith("Add "):
                    resource = line.split(" ")[1]
                    if resource.startswith("AS"):
                        report['ASN_add'].append(resource)
                    else:
                        report['IPRange_add'].append(resource)
            print(f"Completed report for {report['date']}")
            if len(report['date']) > 0:
                print(f"Completed report for {report['date']}")
                summary['reports'].append(report)

    summaries[yearmonth] = summary

with open("summary.json", "w") as f:
    json.dump(summaries, f, indent=2)