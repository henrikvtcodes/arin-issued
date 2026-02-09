import pandas as pd


def remove_as_prefix(asn: str) -> int:
    return asn.replace("")

def main():
    data = pd.read_csv("summary.csv")

    # Get all ASN allocations, convert ASN resource to int and sort
    asns = data[data['resourceType'] == 'ASN']
    asns['resource'] = pd.to_numeric(asns['resource'].apply(lambda x: int(x.replace("AS", ""))))
    asns.sort_values('resource', inplace=True)

    # split out allocations/de-allocations
    asns_allocated: pd.DataFrame = asns[asns['action'] == 'Add']
    asns_removed: pd.DataFrame = asns[asns['action'] == 'Remove']

    # Filter out asns in the free pool that were re-allocated
    asns_available = asns_removed[asns_removed['resource'].isin(asns_allocated['resource'])]
    asns_available.sort_values('resource', inplace=True)

    # Remove unused columns
    asns_available['resourceType'] = None
    asns_available['dt'] = None
    asns_available['action'] = None

    asns_available.to_csv('available.csv', index=False)

if __name__ == "__main__":
    main()