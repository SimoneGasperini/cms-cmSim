import pandas as pd
import numpy as np
import pylab as plt
import itertools
import functools
import operator
from collections import Counter
from datetime import date
from cmSim import utils
from cmSim.tools import plotting


class PopularityAnalyzer:

    def __init__(self, pop_dataframe_parquet, datatier):
        self.df = self.load_dataframe(pop_dataframe_parquet)
        self.datatier = datatier

    @staticmethod
    def load_dataframe(filepath):
        print('Reading input parquet file...', end='')
        df = pd.read_parquet(filepath)
        print(' Done')
        return df

    @staticmethod
    def aggregate_dict(dict, agg_func, mapper):
        new_dict = {key: agg_func([dict[day] for day in group])
                    for key, group in itertools.groupby(dict, lambda day: mapper.get(day, None))}
        return new_dict

    def show_histogram(self, ax, colname, remove_outliers=False):
        arr = self.df[colname].to_numpy()
        if remove_outliers:
            arr = utils.remove_outliers_IQRscore(arr)
        bins = int(len(arr) ** 0.5 / 2)
        ax.hist(arr, bins=bins)
        ax.set_title(self.datatier, fontsize=24)
        ax.set_xlabel(colname, fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        ax.grid('dotted')

    def show_boxplot_by_pag(self, ax, colname, remove_outliers=False):
        pags = list(self.df['pag'].unique())
        if 'Other PWG' in pags:
            pags.remove('Other PWG')
        pags = ['Other PWG'] + pags
        data = [self.df[self.df['pag'] == pag][colname].to_numpy()
                for pag in pags]
        if remove_outliers:
            data = [utils.remove_outliers_IQRscore(arr) for arr in data]
        ax.boxplot(data, vert=False)
        ax.plot([], [], color='red', label='median')
        for i in range(len(pags)):
            ax.scatter(data[i].mean(), i+1, s=20, c='green',
                       label='mean' if i == len(pags)-1 else None)
        ax.set_title(self.datatier, fontsize=24)
        ax.set_xlabel(colname, fontsize=20)
        plt.xticks(fontsize=16)
        plt.yticks(range(1, len(pags)+1), pags, fontsize=20)
        ax.legend(fontsize=16)
        ax.grid('dotted')

    def show_totsize_by_pag(self, ax):
        pags = list(self.df['pag'].unique())
        data = [self.df[self.df['pag'] == pag]['tot_size'].sum()
                for pag in pags]
        colors = plotting.get_custom_colors(pags, groups='pags')
        ax.pie(data, labels=pags, colors=colors, normalize=True, explode=[0.05]*len(data),
               autopct='%1.1f%%', pctdistance=1.1, textprops={'fontsize': 14}, labeldistance=None)
        total = round(self.df['tot_size'].sum() / 1e15, 3)
        ax.set_title(f'{self.datatier}: tot_size = {total} PB', fontsize=24)
        ax.legend(title='PAGs', title_fontsize=20, loc='center left',
                  bbox_to_anchor=(1, 0, 0.5, 1), fontsize=16)

    def plot_features_over_time(self, ax, date1=date(2019, 1, 1), date2=date(2020, 12, 31), agg_by='month', agg_func=np.mean, norm=False):
        features = ['num_replicas', 'fract_replicas',
                    'num_sites_replicas', 'num_accesses']
        date_range = pd.date_range(start=date1, end=date2, freq='D')
        days = [utils.get_string_from_date(dt.date()) for dt in date_range]
        mapper = {'week': utils.get_day_to_week(days),
                  'month': utils.get_day_to_month(days)}[agg_by]
        data = {}
        for feature in features:
            var = [self.aggregate_dict(dict, agg_func=agg_func, mapper=mapper)
                   for dict in self.df[feature]]
            data[feature] = dict(functools.reduce(
                operator.add, map(Counter, var)))
        xs = sorted(list(data[features[0]].keys()))
        for feature in data:
            d = data[feature]
            ys = np.array([d[x] for x in xs], dtype=float)
            if norm:
                ys /= ys.max()
            ax.plot(ys, label=feature)
        ax.set_title(self.datatier, fontsize=24)
        ax.set_xticks(list(range(len(xs))), labels=xs)
        ax.locator_params(axis='x', nbins=24)
        ax.tick_params(axis='both', which='both', labelsize=14)
        ax.legend(fontsize=16)
        ax.grid('dotted')
