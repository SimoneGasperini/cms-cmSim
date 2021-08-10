import numpy as np
import pandas as pd


def get_sites(df, tier=None, country=None):
  tier = tier + '_' if tier is not None else ''
  country = '_' + country + '_' if country is not None else ''
  df = df[(df['node_name'].str.contains(tier)) & (df['node_name'].str.contains(country))]
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
    args = ', '.join([f'name={self.name}', f'disk={self.disk}', f'cpu={self.cpu}',
                      f'tier={self.tier}', f'country={self.country}'])
    return f'{class_name}({args})'

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
    storage_history = {dt: 0. for dt in timeline}
    freq = timeline.freq
    for _, row in self.df.iterrows():
      for dt in pd.date_range(start=row['min_time'], end=row['max_time'], freq=freq):
        storage_history[dt] += row['rep_size']
    return storage_history
