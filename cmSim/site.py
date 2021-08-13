def get_sites(df, tier=None, country=None):
    """
    Return a list of Site objects created from the given dataframe and applying the
    optional filters by tier and by country.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe from which to extract data about the sites
    tier : str, optional
        Tier of belonging (e.g. 'T2'), by default None
    country : str, optional
        Country of belonging (e.g. 'IT'), by default None

    Returns
    -------
    List[Site]
        List containing the selected Site objects
    """
    tier = tier + '_' if tier is not None else ''
    country = '_' + country + '_' if country is not None else ''
    df = df[(df['node_name'].str.contains(tier)) &
            (df['node_name'].str.contains(country))]
    sites = [Site.from_dataframe(df=df[df['node_name'] == name])
             for name in df['node_name'].unique()]
    return sites


class Site:
    """
    Class representing a computing centre/node/site in the world.

    Parameters
    ----------
    name : str
        Name
    disk : float, optional
        Total disk storage available, by default None
    tape : float, optional
        Total tape storage available, by default None
    cpu : float, optional
        Total CPU power available, by default None
    df : pandas.DataFrame, optional
        Dataframe containing data about the site, by default None
    """

    def __init__(self, name, disk=None, tape=None, cpu=None, df=None):
        self.name = name
        self.disk = disk
        self.tape = tape
        self.cpu = cpu
        self.df = df

    def __repr__(self):
        class_name = self.__class__.__qualname__
        params = list(self.__init__.__code__.co_varnames)
        params.remove('self')
        params.remove('df')
        args = [f'{key}={getattr(self, key)}' for key in params]
        args.append(f'tier={self.tier}')
        args.append(f'country={self.country}')
        return f'{class_name}({", ".join(args)})'

    @classmethod
    def from_dataframe(cls, df):
        """
        Return the Site object created from data in the given dataframe.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing data about the site

        Returns
        -------
        Site
            Site object created
        """
        name = df['node_name'].iloc[0]
        return cls(name=name, df=df)

    @property
    def tier(self):
        """
        Get the Site's tier of belonging.

        Returns
        -------
        str
            Tier of belonging
        """
        return self.name.split('_')[0]

    @property
    def country(self):
        """
        Get the Site's country of belonging.

        Returns
        -------
        str
            Country of belonging
        """
        return self.name.split('_')[1]

    def get_storage_history(self, timeline):
        """
        Return a list of stored data amounts corresponding to the given timeline.

        Parameters
        ----------
        timeline : pandas.DatetimeIndex
            Timeline object by Pandas

        Returns
        -------
        List[float]
            List of stored data amounts
        """
        size = [self.df[(date >= self.df['min_time']) & (
            date <= self.df['max_time'])]['rep_size'].sum() for date in timeline]
        return size
