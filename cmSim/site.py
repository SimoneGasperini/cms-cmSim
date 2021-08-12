def get_sites(df, tier=None, country=None):
    tier = tier + '_' if tier is not None else ''
    country = '_' + country + '_' if country is not None else ''
    df = df[(df['node_name'].str.contains(tier)) &
            (df['node_name'].str.contains(country))]
    sites = [Site.from_dataframe(df=df[df['node_name'] == name])
             for name in df['node_name'].unique()]
    return sites


class Site:

    def __init__(self, name, disk=None, cpu=None, df=None):
        self.name = name
        self.disk = disk
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
        name = df['node_name'].iloc[0]
        return cls(name=name, df=df)

    @property
    def tier(self):
        return self.name.split('_')[0]

    @property
    def country(self):
        return self.name.split('_')[1]

    def get_storage_history(self, timeline):
        size = [self.df[(date >= self.df['min_time']) & (
            date <= self.df['max_time'])]['rep_size'].sum() for date in timeline]
        return size
