import pandas as pd
from datetime import date
from cmSim._base import Base
from cmSim import utils


def get_datasets(df, pwg=None, datatier=None):
    """
    Return a list of datasets names applying the optional filters (by PWG and/or by datatier)
    to the given input dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe
    pwg : str, optional
        PWG to be considered (if None, all are taken), by default None
    datatier : str, optional
        Datatier to be considered (if None, all are taken), by default None

    Returns
    -------
    datasets : List[str]
        List of the selected datasets names
    """
    grouped_df = df.groupby('dataset_name').first()
    if pwg is not None:
        grouped_df = grouped_df[grouped_df['pwg'] == pwg]
    if datatier is not None:
        grouped_df = grouped_df[grouped_df['tier'] == datatier]
    datasets = list(grouped_df.index)
    return datasets


class DataContainer(Base):
    """
    Class representing a container for physics datasets.

    Parameters
    ----------
    datasets : List[str]
        List of datasets names
    data : pandas.DataFrame, optional
        Data about the given datasets, by default None
    """

    def __init__(self, datasets, data=None):
        self.datasets = datasets
        self.data = data

    @classmethod
    def from_dataframe(cls, datasets, df):
        """
        Return the DataContainer object created filtering data in the given dataframe.

        Parameters
        ----------
        datasets : List[str]
            List of datasets names
        df : pandas.DataFrame, optional
            Input dataframe

        Returns
        -------
        container : DataContainer
            DataContainer object
        """
        df_datasets = df[df['dataset_name'].isin(datasets)]
        container = cls(datasets=datasets, data=df_datasets)
        return container

    def plot_storage_history_in_sites(self, ax, tier=None, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by
        site) over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only the sites belonging to the specified 'tier'.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        tier : str, optional
            Tier to be considered (if None, all are taken), by default None
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        sites = list(df['node_name'].unique())
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        data = []
        for site in sites:
            dframe = df[df['node_name'] == site]
            storage_history = self._get_storage_history(dframe, timeline)
            data.append(storage_history)
        ax.stackplot(timeline, data, labels=sites)
        tiers = 'T1-T2' if tier is None else tier
        ax.set_title(f'Data storage by sites (tiers={tiers})', fontsize=20)
        self._plot_settings(ax=ax)

    def plot_storage_history_in_countries(self, ax, tier=None, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by
        country) over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only the sites belonging to the specified 'tier' in each country.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        tier : str, optional
            Tier to be considered (if None, all are taken), by default None
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        countries = list(df['node_name'].unique().apply(
            utils.get_country_from_site))
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        data = []
        for country in countries:
            code = utils.get_countryCode_from_countryName(country)
            dframe = df[df['node_name'].str.contains(f'_{code}_')]
            storage_history = self._get_storage_history(dframe, timeline)
            data.append(storage_history)
        ax.stackplot(timeline, data, labels=countries)
        tiers = 'T1-T2' if tier is None else tier
        ax.set_title(f'Data storage by countries (tiers={tiers})', fontsize=20)
        self._plot_settings(ax=ax)

    def plot_storage_history_in_datalakes(self, ax, tier=None, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by
        datalake) over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only the sites belonging to the specified 'tier' in each datalake.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        tier : str, optional
            Tier to be considered (if None, all are taken), by default None
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        datalakes = utils.get_datalakes()
        df['datalake'] = df['node_name'].apply(utils.get_datalake_from_site)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        data = []
        for datalake in datalakes:
            dframe = df[df['datalake'] == datalake]
            storage_history = self._get_storage_history(dframe, timeline)
            data.append(storage_history)
        ax.stackplot(timeline, data, labels=datalakes)
        tiers = 'T1-T2' if tier is None else tier
        ax.set_title(f'Data storage by datalakes (tiers={tiers})', fontsize=20)
        self._plot_settings(ax=ax)

    def plot_storage_history_by_pag(self):
        raise NotImplementedError
