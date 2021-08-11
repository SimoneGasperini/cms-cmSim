import numpy as np
import pandas as pd
from datetime import date


def get_datasets(df, substring=None, format=None):
    substring = substring if substring is not None else ''
    format = format if format is not None else ''
    df = df[(df['dataset_name'].str.contains(substring))
            & (df['dataset_name'].str.contains(format))]
    datasets = [Dataset.from_dataframe(df=df[df['dataset_name'] == name])
                for name in df['dataset_name'].unique()]
    return datasets


class Dataset:

    def __init__(self, name, ID, format, df=None):
        self.name = name
        self.ID = ID
        self.format = format
        self.df = df

    def __repr__(self):
        class_name = self.__class__.__qualname__
        args = ', '.join([f'name={self.name}', f'ID={self.ID}', f'format={self.format}',
                          f'totsize={round(self.totsize * 1e-9, 3)}[GB]'])
        return f'{class_name}({args})'

    @classmethod
    def from_dataframe(cls, df):
        name = df['dataset_name'].iloc[0]
        ID = df['dataset_id'].iloc[0]
        format = df['tier'].iloc[0]
        return cls(name=name, ID=ID, format=format, df=df)

    @property
    def totsize(self):
        return self.df['rep_size'].max()  # assuming totsize == max(rep_size)

    def get_history(self, freq='M'):
        history = {}
        for _, row in self.df.iterrows():
            for dt in pd.date_range(start=row['min_time'], end=row['max_time'], freq=freq):
                node = row['node_name']
                d = {'number of data blocks': 0, 'total data fraction': 0.}
                history.setdefault(dt, {}).setdefault(node, d)
                history[dt][node]['number of data blocks'] += 1
                history[dt][node]['total data fraction'] += row['rep_size']
        return history

    def get_history_dataframe(self, start_date=date(2019, 1, 1), end_date=date(2020, 12, 31), freq='M'):
        history = self.get_history(freq=freq)
        data = {}
        for dt in history:
            if start_date <= dt.date() <= end_date:
                data[dt] = [{'node/site': n,
                             'number of data blocks': history[dt][n]['number of data blocks'],
                             'total data fraction': round(history[dt][n]['total data fraction'] / self.totsize, 4)}
                            for n in history[dt]]
        df = pd.concat({dt.strftime('%Y-%m-%d'): pd.DataFrame(data[dt])
                        for dt in sorted(list(data.keys()))})
        return df
