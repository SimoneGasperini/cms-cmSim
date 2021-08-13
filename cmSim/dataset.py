import pandas as pd


def get_datasets(df, info_df, name_substr=None, format=None):
    """
    Return a list of Dataset objects created from the given dataframe and the given info,
    and applying the optional filters by substring (of dataset's name) and by format/tier.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe from which to extract data about the datasets
    info_df : pandas.Dataframe
        Dataframe from which to extract general info about the datasets
    substring : str, optional
        Substring to filter the dataset names, by default None
    format : str, optional
        Dataset format, by default None

    Returns
    -------
    List[Dataset]
        List containing the selected Dataset objects
    """
    substring = name_substr if name_substr is not None else ''
    format = format if format is not None else ''
    df = df[(df['dataset_name'].str.contains(substring))
            & (df['dataset_name'].str.contains(format))]
    datasets = [Dataset.from_dataframe(df=df[df['dataset_name'] == name],
                                       info=info_df[info_df['d_dataset'] == name].iloc[0])
                for name in df['dataset_name'].unique()]
    return datasets


class Dataset:
    """
    Class representing a physics dataset.

    Parameters
    ----------
    name : str
        Name
    ID : int
        ID
    size : float, optional
        Total size, by default None
    nfiles : int, optional
        Number of files in which the data is split, by default None
    nevents : int, optional
        Number of events, by default None
    format : str, optional
        Data format/tier, by default None
    df : pandas.DataFrame, optional
        Dataframe containing data about the dataset, by default None
    """

    def __init__(self, name, ID, size=None, nfiles=None, nevents=None, format=None, df=None):
        self.name = name
        self.ID = ID
        self.size = size
        self.nfiles = nfiles
        self.nevents = nevents
        self.format = format
        self.df = df

    def __repr__(self):
        class_name = self.__class__.__qualname__
        params = list(self.__init__.__code__.co_varnames)
        params.remove('self')
        params.remove('df')
        args = ', '.join([f'{key}={getattr(self, key)}' for key in params])
        return f'{class_name}({args})'

    @classmethod
    def from_dataframe(cls, df, info=None):
        """
        Return the Dataset object created from data in the given dataframe and the given info.

        Parameters
        ----------
        df : pandas.DataFrame
            Dataframe containing data about the dataset
        info : pandas.Series, optional
            Series containing general info about the dataset (size, # events, etc), by default None

        Returns
        -------
        Dataset
            Dataset object created
        """
        name = df.iloc[0]['dataset_name']
        ID = df.iloc[0]['dataset_id']
        size, nfiles, nevents, format = None, None, None, None
        if info is not None:
            size = info['dsize']
            nfiles = info['nfiles']
            nevents = info['devts']
            format = info['tier']
        return cls(name=name, ID=ID, size=size, nfiles=nfiles, nevents=nevents, format=format, df=df)

    def get_history_dataframe(self, freq='M'):
        """
        Return a dataframe representing the dataset's storage history (following the given
        timeline frequency). The dataframe contains the following fields:
        - site where the dataset is stored;
        - number of different data blocks;
        - total fraction of stored data over the entire dataset's size.

        Parameters
        ----------
        freq : str, optional
            Timeline frequency (month: 'M', week: 'W', etc), by default 'M'

        Returns
        -------
        pandas.DataFrame
            Dataframe representing the dataset's storage history
        """
        history = {}
        for _, row in self.df.iterrows():
            for dt in pd.date_range(start=row['min_time'], end=row['max_time'], freq=freq):
                node = row['node_name']
                d = {'number of data blocks': 0, 'total data fraction': 0.}
                history.setdefault(dt, {}).setdefault(node, d)
                history[dt][node]['number of data blocks'] += 1
                history[dt][node]['total data fraction'] += row['rep_size']
        data = {}
        for dt in history:
            data[dt] = [{'node/site': n,
                         'number of data blocks': history[dt][n]['number of data blocks'],
                         'total data fraction': round(history[dt][n]['total data fraction'] / self.size, 4)}
                        for n in history[dt]]
        df = pd.concat({dt.strftime('%Y-%m-%d'): pd.DataFrame(data[dt])
                        for dt in sorted(list(data.keys()))})
        return df
