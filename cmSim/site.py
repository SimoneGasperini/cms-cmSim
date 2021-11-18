from cmSim._base import Base
from cmSim import utils


class Site(Base):
    """
    Class representing a node/site in the world.

    Parameters
    ----------
    name : str
        Site's name
    data : pandas.DataFrame, optional
        Data about the given site, by default None
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
        args.append(f'tier={self.tier}')
        args.append(f'country={self.country}')
        return f'{class_name}({", ".join(args)})'

    @classmethod
    def from_dataframe(cls, df, name):
        """
        Return the Site object created filtering data in the given dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Input dataframe
        name : str
            Site's name

        Returns
        -------
        site : Site
            Site object
        """
        df_site = df[df['node_name'] == name]
        site = cls(name=name, data=df_site)
        return site

    @property
    def tier(self):
        """
        Get the tier of belonging.

        Returns
        -------
        tier : str
            Site's tier
        """
        tier = utils.get_tier_from_site(self.name)
        return tier

    @property
    def country(self):
        """
        Get the country of belonging.

        Returns
        -------
        country : str
            Site's country
        """
        country = utils.get_country_from_site(self.name)
        return country
