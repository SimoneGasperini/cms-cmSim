import numpy as np
import pandas as pd
from datetime import date
from cmSim._base import Base
from cmSim import utils
from cmSim.tools import plotting


def get_datasets(df, pwgs=None, datatiers=None):
    """
    Return a list of datasets names applying the optional filters (by PWG and/or by datatier)
    to the given input dataframe.

    Parameters
    ----------
    df : pandas.DataFrame
        Input dataframe
    pwgs : List[str], optional
        PWGs to be considered (if None, all are taken), by default None
    datatiers : List[str], optional
        Datatiers to be considered (if None, all are taken), by default None

    Returns
    -------
    datasets : List[str]
        List of the selected datasets names
    """
    grouped_df = df.groupby('dataset_name').first()
    if pwgs is not None:
        grouped_df = grouped_df[grouped_df['pwg'].isin(pwgs)]
    if datatiers is not None:
        grouped_df = grouped_df[grouped_df['tier'].isin(datatiers)]
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
    def from_dataframe(cls, df, datasets=None):
        """
        Return the DataContainer object created filtering data in the given dataframe.

        Parameters
        ----------
        df : pandas.DataFrame, optional
            Input dataframe
        datasets : List[str], optional
            List of datasets names (if None, all are taken), by default None

        Returns
        -------
        container : DataContainer
            DataContainer object
        """
        if datasets is not None:
            df = df[df['dataset_name'].isin(datasets)]
        container = cls(datasets=datasets, data=df)
        return container

    def plot_storage_history_in_sites(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
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
        norm : bool, optional
            If True, apply normalization, by default False
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        sites = sorted(list(df['node_name'].unique()))
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = [self._get_storage_history(df[df['node_name'] == site], timeline)
                       for site in sites]
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [B]'
        time_series, sorted_labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=sites)
        time_series, merged_sorted_labels = plotting.merge_stacked_areas(
            time_series=time_series, labels=sorted_labels)
        colors = plotting.get_default_colors(labels=merged_sorted_labels)
        ax.stackplot(timeline, time_series,
                     labels=merged_sorted_labels, colors=colors)
        labels = [site for site in sites
                  if site in merged_sorted_labels] + ['Other']
        plotting.set_stackplot_settings(
            ax, ylabel=ylabel, legend_title='Sites', legend_labels=labels)

    def plot_storage_history_in_countries(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
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
        norm : bool, optional
            If True, apply normalization, by default False
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        countries = utils.get_countries()
        country_mask = np.array([utils.get_country_from_site(site)
                                 for site in df['node_name']])
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = [self._get_storage_history(df[country_mask == country], timeline)
                       for country in countries]
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [B]'
        time_series, sorted_labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=countries)
        time_series, merged_sorted_labels = plotting.merge_stacked_areas(
            time_series=time_series, labels=sorted_labels)
        colors = plotting.get_default_colors(labels=merged_sorted_labels)
        ax.stackplot(timeline, time_series,
                     labels=merged_sorted_labels, colors=colors)
        labels = [country for country in countries
                  if country in merged_sorted_labels] + ['Other']
        plotting.set_stackplot_settings(
            ax, ylabel=ylabel, legend_title='Countries', legend_labels=labels)

    def plot_storage_history_in_datalakes(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
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
        norm : bool, optional
            If True, apply normalization, by default False
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        df = self._filter_by_tier(self.data, tier)
        datalakes = utils.get_datalakes()
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        datalake_mask = np.array([utils.get_datalake_from_site(site)
                                  for site in df['node_name']])
        time_series = [self._get_storage_history(df[datalake_mask == datalake], timeline)
                       for datalake in datalakes]
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [B]'
        time_series, sorted_labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=datalakes)
        sorted_colors = plotting.get_custom_colors(
            labels=sorted_labels, groups='datalakes')
        ax.stackplot(timeline, time_series,
                     labels=sorted_labels, colors=sorted_colors)
        plotting.set_stackplot_settings(
            ax, ylabel=ylabel, legend_title='Datalakes', legend_labels=datalakes)
