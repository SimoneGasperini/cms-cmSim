import pandas as pd
from datetime import date
from cmSim.tools import plotting


class Base:

    @staticmethod
    def _filter_by_tier(df, tier):
        return df[df['node_name'].str.startswith(tier)] if tier is not None else df

    @staticmethod
    def _filter_by_datatiers(df, datatiers):
        return df[df['tier'].isin(datatiers)] if datatiers is not None else df

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
        more_labels = ['Other']
        labels = datatiers + more_labels
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [B]'
        time_series, sorted_labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=datatiers, more_labels=more_labels)
        sorted_colors = plotting.get_custom_colors(
            labels=sorted_labels, groups='datatiers')
        ax.stackplot(timeline, time_series,
                     labels=sorted_labels, colors=sorted_colors)
        plotting.set_stackplot_settings(
            ax, ylabel=ylabel, legend_title='Data-tiers', legend_labels=labels)

    def plot_storage_history_by_pag(self, ax, pags, datatiers=None, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data stored on disk (grouped by PAG)
        over the given time period (from 'date1' to 'date2' with intervals given by 'freq').
        The data are filtered considering only replicas stored in sites belonging to the specified 'tier'.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        pags : List[str]
            PAGs to be considered in the grouping
        datatiers : List[str], optional
            Datatiers to be considered (if None, all are taken), by default None
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
        df = self._filter_by_datatiers(self.data, datatiers)
        df = self._filter_by_tier(df, tier)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
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
        more_labels = ['Other PWG', 'Not found']
        labels = pags + more_labels
        if norm:
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [B]'
        time_series, sorted_labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=pags, more_labels=more_labels)
        sorted_colors = plotting.get_custom_colors(
            labels=sorted_labels, groups='pags')
        ax.stackplot(timeline, time_series,
                     labels=sorted_labels, colors=sorted_colors)
        plotting.set_stackplot_settings(
            ax, ylabel=ylabel, legend_title='PAGs', legend_labels=labels)
