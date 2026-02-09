import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def graph_issued_asns(data: pd.DataFrame):
    daily_counts = (
        data.groupby('day')
        .size()
        .rename('asns_issued')
        .sort_index()
    )

    if not daily_counts.empty:
        full_range = pd.date_range(daily_counts.index.min(), daily_counts.index.max(), freq='D',
                                   tz=daily_counts.index.tz)
        daily_counts = daily_counts.reindex(full_range, fill_value=0)
    else:
        daily_counts = pd.Series([], dtype='int64', name='asns_issued')

    # Fill missing days with 0 to get a continuous series (helps with plotting/rolling windows)
    full_range = pd.date_range(daily_counts.index.min(), daily_counts.index.max(), freq='D')
    daily_counts = daily_counts.reindex(full_range, fill_value=0)
    daily_counts.index.name = 'date'

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 6), dpi=140)


    # --- 4) Find and store the peak day ---
    peak_day = daily_counts.idxmax()
    peak_val = int(daily_counts.loc[peak_day])

    # Daily series (light line) + rolling average (bold line)
    ax.plot(daily_counts.index, daily_counts.values, color='steelblue', alpha=0.45, linewidth=1.0,
            label='Daily ASNs issued')

    ax.axvline(peak_day, color='goldenrod', linestyle='--', linewidth=2, alpha=0.9)
    ax.scatter([peak_day], [peak_val], color='gold', edgecolor='black', zorder=5)
    ax.annotate(
        f'Peak: {peak_val} ASNs on {peak_day:%Y-%m-%d}',
        xy=(peak_day, peak_val),
        xytext=(10, 18),
        textcoords='offset points',
        ha='left', va='bottom',
        bbox=dict(boxstyle='round,pad=0.3', fc='lemonchiffon', ec='goldenrod', alpha=0.9),
        arrowprops=dict(arrowstyle='->', color='goldenrod')
    )

    locator = mdates.AutoDateLocator(minticks=6, maxticks=12)  # keeps tick count sane
    formatter = mdates.ConciseDateFormatter(locator)  # compact "2008", "2012", "Jan 2015", etc.
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # Labels, legend, limits
    ax.set_title('ARIN ASN Issuance Over Time (Daily)', pad=14)
    ax.set_ylabel('ASNs issued per day')
    ax.set_xlabel('Date')
    ax.set_ylim(bottom=0)
    ax.legend(loc='upper left', ncols=2)
    ax.grid(True, axis='y', linestyle='--', alpha=0.35)

    fig.tight_layout()
    # Optional: fig.savefig('arin_asn_issuance_daily.png', bbox_inches='tight')
    plt.show()


def main():
    # data = pd.read_csv("summary.csv").sort_values(by=['date'], ascending=True)
    data = pd.read_csv("summary.csv")

    asn_add = data.loc[(data['resourceType'].str.upper() == 'ASN') & (data['action'].str.upper() == 'ADD'), ['dt']].dropna().copy()
    asn_add['day'] = asn_add['dt'].dt.floor('D')

    print(data.head(1))

    graph_issued_asns(asn_add)


if __name__ == "__main__":
    main()