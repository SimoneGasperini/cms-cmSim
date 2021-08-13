import pandas as pd
import pylab as plt
from datetime import date


def plot_storage_history(sites, start_date=date(2019, 1, 1), end_date=date(2020, 12, 31), freq='M'):
    """
    Draw a stacked area plot representing the time series of the amout of data stored
    in the given sites in the given time interval.

    Parameters
    ----------
    sites : List[Site]
        List of Site objects to be considered
    start_date : datetime.date, optional
        Timeline starting date, by default date(2019, 1, 1)
    end_date : datetime.date, optional
        Timeline ending date, by default date(2020, 12, 31)
    freq : str, optional
        Timeline frequency (month: 'M', week: 'W', etc), by default 'M'
    """
    timeline = pd.date_range(start=start_date, end=end_date, freq=freq)
    data = {s.name: s.get_storage_history(timeline) for s in sites}
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.stackplot(timeline, data.values(), labels=data.keys())
    ax.set_ylabel('stored data [B]', fontsize=14)
    ax.grid(linestyle='dotted')
    ax.legend(loc='best', fontsize=12)
    fig.autofmt_xdate()
    plt.show()
