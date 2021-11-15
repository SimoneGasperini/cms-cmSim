import pandas as pd
from datetime import date
from cmSim.tools import plotting


class Base:

    @staticmethod
    def _filter_by_tier(df, tier):
        return df[df['node_name'].str.startswith(tier)] if tier is not None else df

    @staticmethod
    def _filter_by_datatier(df, datatier):
        return df[df['tier'] == datatier] if datatier is not None else df

    @staticmethod
    def _get_storage_history(df, timeline):
        return [df[(df['min_time'] <= date) & (date <= df['max_time'])]['rep_size'].sum()
                for date in timeline]

    def plot_storage_history_by_datatier(self, ax, datatiers, title, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        df = self._filter_by_tier(self.data, tier)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = []
        for dtier in datatiers:
            dframe = df[df['tier'] == dtier]
            storage_history = self._get_storage_history(dframe, timeline)
            time_series.append(storage_history)
        # Other datatiers
        dframe = df[df['tier'] == 'Other']
        storage_history = self._get_storage_history(dframe, timeline)
        time_series.append(storage_history)
        more_labels = ['Other']
        labels = datatiers + more_labels
        if norm:
            time_series = plotting.norm_stacked_areas(time_series=time_series)
        time_series, sorted_labels = plotting.sort_stacked_areas(time_series=time_series,
                                                                 labels=datatiers, more_labels=more_labels)
        sorted_colors = plotting.get_colors(labels=sorted_labels,
                                            groups='datatiers')
        ax.stackplot(timeline, time_series,
                     labels=sorted_labels, colors=sorted_colors)
        plotting.set_stackplot_settings(ax, title=title, ylabel='Data fraction' if norm else 'Data amount [B]',
                                        legend_title='Data-tiers', legend_labels=labels)

    def plot_storage_history_by_pag(self, ax, pags, title, tier=None, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        df = self._filter_by_tier(self.data, tier)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = []
        for pag in pags:
            dframe = df[df['pwg'] == pag]
            storage_history = self._get_storage_history(dframe, timeline)
            time_series.append(storage_history)
        # Other PWG
        dframe = df[(df['pwg'] != 'None') & (~df['pwg'].isin(pags))]
        storage_history = self._get_storage_history(dframe, timeline)
        time_series.append(storage_history)
        # PWG not found
        dframe = df[df['pwg'] == 'None']
        storage_history = self._get_storage_history(dframe, timeline)
        time_series.append(storage_history)
        more_labels = ['Other PWG', 'Not found']
        labels = pags + more_labels
        if norm:
            time_series = plotting.norm_stacked_areas(time_series=time_series)
        time_series, sorted_labels = plotting.sort_stacked_areas(time_series=time_series,
                                                                 labels=pags, more_labels=more_labels)
        sorted_colors = plotting.get_colors(labels=sorted_labels,
                                            groups='pags')
        ax.stackplot(timeline, time_series,
                     labels=sorted_labels, colors=sorted_colors)
        plotting.set_stackplot_settings(ax, title=title, ylabel='Data fraction' if norm else 'Data amount [B]',
                                        legend_title='PAGs', legend_labels=labels)
