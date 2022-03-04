import pandas as pd
import numpy as np
import pylab as plt
from datetime import date
from cmSim._base import Base
from cmSim import utils
from cmSim.tools import plotting


class Country(Base):
    """
    Class representing a country in the world.

    Parameters
    ----------
    name : str
        Country's name
    data : pandas.DataFrame, optional
        Data about the given country, by default None
    """

    def __init__(self, name, data=None):
        self.name = name
        self.data = data

    def __repr__(self):
        class_name = self.__class__.__qualname__
        params = list(self.__init__.__code__.co_varnames)
        params.remove('self')
        params.remove('data')
        args = [f'{key}={getattr(self, key)}' for key in params]
        args.append(f'code={self.code}')
        args.append(f'#T1s={len(self.t1_sites)}')
        args.append(f'#T2s={len(self.t2_sites)}')
        return f'{class_name}({", ".join(args)})'

    @classmethod
    def from_dataframe(cls, df, name):
        """
        Return the Country object created filtering data in the given dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        name : str
            Country's name

        Returns
        -------
        country : Country
            Country object
        """
        code = utils.get_countryCode_from_countryName(name)
        df_country = df[df['node_name'].str.contains(f'_{code}_')]
        country = cls(name=name, data=df_country)
        return country

    @property
    def code(self):
        """
        Get the 2-letters code for the country.

        Returns
        -------
        code : str
            Country's 2-letters code
        """
        code = utils.get_countryCode_from_countryName(self.name)
        return code

    @property
    def t1_sites(self):
        """
        Get the list of Tier-1 sites in the country.

        Returns
        -------
        t1_sites : List[str]
            Country's Tier-1 sites
        """
        t1_sites = [site for site in set(self.data['node_name'])
                    if 'T1_' in site]
        return t1_sites

    @property
    def t2_sites(self):
        """
        Get the list of Tier-2 sites in the country.

        Returns
        -------
        t2_sites : List[str]
            Country's Tier-2 sites
        """
        t2_sites = [site for site in set(self.data['node_name'])
                    if 'T2_' in site]
        return t2_sites

    def plot_storage_history_by_site(self, ax, norm=False, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data amout stored on disk in the country
        (grouped by site) over the given time period (from 'date1' to 'date2' with intervals given by 'freq').

        Parameters
        ----------
        ax : matplotlib.axes
            Matplotlib axes on which to draw the plot
        norm : bool, optional
            If True, apply normalization, by default False
        date1 : datetime.date, optional
            Timeline starting date, by default date(2019, 1, 1)
        date2: datetime.date, optional
            Timeline ending date, by default date(2020, 12, 31)
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'W'
        """
        sites = self.t1_sites + self.t2_sites
        df = self.data
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        time_series = [self._get_storage_history(df[df['node_name'] == site], timeline)
                       for site in sites]
        time_series = np.array(time_series) / 1e15
        average_totsize = round(time_series.mean(axis=1).sum())
        if norm:
            ax.set_title(
                f'Average total size $\simeq$ {average_totsize} PB', fontsize=28)
            time_series = plotting.norm_stacked_areas(time_series)
            ylabel = 'Data fraction'
        else:
            ylabel = 'Data amount [PB]'
        time_series, labels = plotting.sort_stacked_areas(
            time_series=time_series, labels=sites)
        colors = plotting.get_default_colors(labels=labels, cmap=plt.cm.Set1)
        ax.stackplot(timeline, time_series, labels=labels, colors=colors)
        plotting.set_legend_settings(ax, title='Sites', labels=labels)
        ax.tick_params(axis='both', which='major', labelsize=18)
        ax.set_ylabel(ylabel, fontsize=24)
        ax.grid(linestyle='dotted')
