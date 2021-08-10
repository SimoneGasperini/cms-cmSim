import numpy as np
import pandas as pd


def get_sites(df, tier=None, country=None):
  tier = tier + '_' if tier is not None else ''
  country = '_' + country + '_' if country is not None else ''
  filtered_df = df.filter((df['node_name'].contains(tier)) & (df['node_name'].contains(country)))
  all_rows = filtered_df.collect()
  sites = []
  for dr in filtered_df.select('node_name').distinct().collect():
    site_rows = [row for row in all_rows if row['node_name'] == dr['node_name']]
    sites.append(Site.from_rowslist(rowslist=site_rows))
  return sites


class Site:

  def __init__(self, name, disk=None, cpu=None, rowslist=None):
    self.name = name
    self.disk = disk
    self.cpu = cpu
    self._rowslist = rowslist

  def __repr__(self):
    class_name = self.__class__.__qualname__
    args = ', '.join([f'name={self.name}', f'disk={self.disk}', f'cpu={self.cpu}',
                      f'tier={self.tier}', f'country={self.country}'])
    return f'{class_name}({args})'

  @classmethod
  def from_rowslist(cls, rowslist):
    name = rowslist[0]['node_name']
    return cls(name=name, rowslist=rowslist)

  @property
  def tier(self):
    return self.name.split('_')[0]

  @property
  def country(self):
    return self.name.split('_')[1]

  def get_storage_history(self, timeline):
    storage_history = {dt: 0. for dt in timeline}
    freq = timeline.freq
    for row in self._rowslist:
      for dt in pd.date_range(start=row['min_time'], end=row['max_time'], freq=freq):
        storage_history[dt] += row['rep_size']
    return storage_history
