import pandas as pd
import numpy as np
import pylab as plt
from datetime import date
from cmSim import utils
from cmSim.tools import plotting


class Base:

    @staticmethod
    def _filter_by_tier(df, tier):
        return df[df['node_name'].str.startswith(tier)] if tier is not None else df

    @staticmethod
    def _get_storage_history(df, timeline):
        return [df[(df['min_time'] <= date) & (date <= df['max_time'])]['rep_size'].sum()
                for date in timeline]

    def plot_storage_history_by_datatier(self, ax, datatiers, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by
        datatier) over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only replicas stored in sites belonging to the specified 'tier'.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        datatiers : List[str]
            Datatiers to be considered in the grouping
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
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = [self._get_storage_history(df[df['tier'] == dtier], timeline)
                       for dtier in datatiers]
        # Other datatiers
        storage_history = self._get_storage_history(
            df[~df['tier'].isin(datatiers)], timeline)
        time_series.append(storage_history)
        time_series = np.array(time_series) / 1e15
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [PB]'
        time_series, labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=datatiers, more_labels=['Other'])
        colors = plotting.get_custom_colors(labels=labels, groups='datatiers')
        ax.stackplot(timeline, time_series, labels=labels, colors=colors)
        plotting.set_legend_settings(ax, title='Data tiers', labels=labels)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_ylabel(ylabel, fontsize=24)
        ax.grid(linestyle='dotted')

    def plot_storage_history_by_pag(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by PAG)
        over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only replicas stored in sites belonging to the specified 'tier'.

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
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        pags = list(set(df['pwg']) & set(utils.get_pags()))
        time_series = [self._get_storage_history(df[df['pwg'] == pag], timeline)
                       for pag in pags]
        # Other PWG
        storage_history = self._get_storage_history(
            df[(df['pwg'] != 'None') & (~df['pwg'].isin(pags))], timeline)
        time_series.append(storage_history)
        # PWG not found
        storage_history = self._get_storage_history(
            df[df['pwg'] == 'None'], timeline)
        time_series.append(storage_history)
        time_series = np.array(time_series) / 1e15
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [PB]'
        time_series, labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=pags, more_labels=['Other PWG', 'Not found'])
        colors = plotting.get_custom_colors(labels=labels, groups='pags')
        ax.stackplot(timeline, time_series, labels=labels, colors=colors)
        plotting.set_legend_settings(ax, title='PAGs', labels=labels)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_ylabel(ylabel, fontsize=24)
        ax.grid(linestyle='dotted')

    def plot_storage_history_by_year(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by campaign year)
        over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only replicas stored in sites belonging to the specified 'tier'.

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
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        years = list(df['year'].unique())
        if 'None' in years:
            years.remove('None')
        time_series = [self._get_storage_history(df[df['year'] == year], timeline)
                       for year in years]
        # Year not found
        storage_history = self._get_storage_history(
            df[df['year'] == 'None'], timeline)
        time_series.append(storage_history)
        time_series = np.array(time_series) / 1e15
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [PB]'
        time_series, labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=years, more_labels=['Not found'])
        colors = plotting.get_default_colors(labels=labels, cmap=plt.cm.Dark2)
        ax.stackplot(timeline, time_series, labels=labels, colors=colors)
        labels.sort()
        plotting.set_legend_settings(ax, title='Campaign year', labels=labels)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_ylabel(ylabel, fontsize=24)
        ax.grid(linestyle='dotted')

    def plot_storage_history_by_generator(self, ax, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by MC generator)
        over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only replicas stored in sites belonging to the specified 'tier'.

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
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        generators = list(df['generator'].unique())
        if 'None' in generators:
            generators.remove('None')
        time_series = [self._get_storage_history(df[df['generator'] == generator], timeline)
                       for generator in generators]
        # MC generator not found
        storage_history = self._get_storage_history(
            df[df['generator'] == 'None'], timeline)
        time_series.append(storage_history)
        time_series = np.array(time_series) / 1e15
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [PB]'
        time_series, labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=generators, more_labels=['Not found'])
        colors = plotting.get_default_colors(labels=labels, cmap=plt.cm.Set3)
        ax.stackplot(timeline, time_series, labels=labels, colors=colors)
        plotting.set_legend_settings(ax, title='MC generators', labels=labels)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_ylabel(ylabel, fontsize=24)
        ax.grid(linestyle='dotted')
