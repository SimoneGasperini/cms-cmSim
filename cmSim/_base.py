import pandas as pd
from datetime import date
from cmSim import utils


class Base:

    @staticmethod
    def _filter_by_tier(df, tier):
        if tier is not None:
            return df[df['node_name'].str.contains(f'{tier}_')]
        else:
            return df

    @staticmethod
    def _filter_by_datatier(df, datatier):
        if datatier is not None:
            return df[df['tier'] == datatier]
        else:
            return df

    @staticmethod
    def _get_storage_history(df, timeline):
        storage_history = [df[(df['min_time'] <= date) & (date <= df['max_time'])]['rep_size'].sum()
                           for date in timeline]
        return storage_history

    @staticmethod
    def _plot_settings(ax):
        ax.set_xlabel('time', fontsize=16)
        ax.set_ylabel('data stored on disk [B]', fontsize=16)
        ax.tick_params(axis='both', labelsize=14)
        ax.legend(loc='best', fontsize=14)
        ax.grid(linestyle='dotted')

    def plot_storage_history_by_pag(self, ax, datatier=None, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data amout stored on disk in the
        site/country (grouped by PAG) over the given time period (from 'date1' to 'date2' with intervals
        given by 'freq'). The data are filtered considering only the specified 'datatier'.

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        datatier : str, optional
            Datatier to be considered (if None, all are taken), by default None
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        pags = utils.get_pwgs(group='pags')
        df = self._filter_by_datatier(self.data, datatier)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        data = []
        for pag in pags:
            dframe = df[df['pwg'] == pag]
            storage_history = self._get_storage_history(dframe, timeline)
            data.append(storage_history)
        # Other PWG (POGs or DPGs)
        dframe = df[(df['pwg'] != 'None') & (~df['pwg'].isin(pags))]
        storage_history = self._get_storage_history(dframe, timeline)
        data.append(storage_history)
        # PWG not found (None)
        dframe = df[df['pwg'] == 'None']
        storage_history = self._get_storage_history(dframe, timeline)
        data.append(storage_history)
        labels = pags + ['Other PWG', 'Not found']
        label_to_color = utils.get_pag_to_color(others={'Other PWG': 'gray',
                                                        'Not found': 'black'})
        colors = [label_to_color[label] for label in labels]
        ax.stackplot(timeline, data, labels=labels, colors=colors)
        ax.set_title(self.__repr__(), fontsize=20)
        self._plot_settings(ax=ax)
