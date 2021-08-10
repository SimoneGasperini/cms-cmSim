import numpy as np
import pandas as pd
from datetime import date


def get_datasets(df, substring=None, format=None):
  substring = substring if substring is not None else ''
  format = format if format is not None else ''
  filtered_df = df.filter((df['dataset_name'].contains(substring)) & (df['dataset_name'].contains(format)))
  all_rows = filtered_df.collect()
  datasets = []
  for dr in filtered_df.select('dataset_name').distinct().collect():
    dataset_rows = [row for row in all_rows if row['dataset_name'] == dr['dataset_name']]
    datasets.append(Dataset.from_rowslist(rowslist=dataset_rows))
  return datasets


class Dataset:

  def __init__(self, name, ID, format, rowslist=None):
    self.name = name
    self.ID = ID
    self.format = format
    self._rowslist = rowslist

  def __repr__(self):
    class_name = self.__class__.__qualname__
    args = ', '.join([f'name={self.name}', f'ID={self.ID}', f'format={self.format}',
                      f'totsize={round(self.totsize * 1e-9, 3)}[GB]'])
    return f'{class_name}({args})'

  @classmethod
  def from_rowslist(cls, rowslist):
    name = rowslist[0]['dataset_name']
    ID = rowslist[0]['dataset_id']
    format = rowslist[0]['tier']
    return cls(name=name, ID=ID, format=format, rowslist=rowslist)

  @property
  def totsize(self):
    return np.max([row['rep_size'] for row in self._rowslist])  # assuming totsize == max(rep_size)

  def get_history(self, freq='M'):
    history = {}
    for row in self._rowslist:
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
