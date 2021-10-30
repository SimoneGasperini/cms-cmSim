import pandas as pd
from datetime import date
from cmSim._base import Base
from cmSim import utils


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
    def from_dataframe(cls, name, df):
        """
        Return the Country object created filtering data in the given dataframe.

        Parameters
        ----------
        name : str
            Country's name
        df : pandas.DataFrame
            Input dataframe

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

    def plot_storage_history_by_site(self, ax, datatier=None, date1=date(2019, 1, 1), date2=date(2020, 12, 31), freq='W'):
        """
        Draw a stacked area plot representing the time series of data amout stored on disk in the
        country (grouped by site) over the given time period (from 'date1' to 'date2' with intervals
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
        sites = self.t1_sites + self.t2_sites
        df = self._filter_by_datatier(self.data, datatier)
        timeline = [dt.date() for dt in pd.date_range(date1, date2, freq=freq)]
        data = []
        for site in sites:
            dframe = df[df['node_name'] == site]
            storage_history = self._get_storage_history(dframe, timeline)
            data.append(storage_history)
        ax.stackplot(timeline, data, labels=sites)
        ax.set_title(self.__repr__(), fontsize=20)
        self._plot_settings(ax=ax)
