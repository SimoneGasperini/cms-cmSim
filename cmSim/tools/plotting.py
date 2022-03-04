import numpy as np
import pylab as plt
import seaborn as sns
from cmSim import utils
import matplotlib.colors as mc
from matplotlib.ticker import FormatStrFormatter


def norm_stacked_areas(time_series):
    tot_time_series = time_series.sum(axis=0)
    normed_time_series = time_series / tot_time_series
    return normed_time_series


def sort_stacked_areas(time_series, labels, more_labels=[]):
    labels = np.array(labels)
    n = len(labels)
    sorting = time_series[:n].mean(axis=1).argsort()[::-1]
    sorted_time_series = np.vstack((time_series[:n][sorting], time_series[n:]))
    sorted_labels = np.append(labels[sorting], more_labels)
    return sorted_time_series, sorted_labels


def adjust_colors_lightness(colors, lightness=0.6):
    new_colors = []
    for col in colors:
        lightness = lightness if col != 'black' else 0.2
        rgb = mc.ColorConverter.to_rgb(col)
        new_col = sns.set_hls_values(color=rgb, h=None, l=lightness, s=None)
        new_colors.append(new_col)
    return new_colors


def get_default_colors(labels, cmap=plt.cm.tab10):
    colors = [cmap(i) for i in range(len(labels))]
    if 'Not found' in labels:
        i = np.where(labels == 'Not found')[0][0]
        colors[i] = 'black'
    colors = adjust_colors_lightness(colors)
    return colors


def get_custom_colors(labels, groups):
    if groups == 'pags':
        lab_to_col = utils.get_pag_to_color()
    if groups == 'datatiers':
        lab_to_col = utils.get_datatier_to_color()
    if groups == 'datalakes':
        lab_to_col = utils.get_datalake_to_color()
    colors = [lab_to_col[lab] for lab in labels]
    if groups == 'pags' or groups == 'datalakes':
        colors = adjust_colors_lightness(colors)
    return colors


def set_legend_settings(ax, title, labels):
    _handles, _labels = ax.get_legend_handles_labels()
    sorting = [np.where(np.array(_labels) == lab)[0][0] for lab in labels]
    sorted_handles = np.array(_handles)[sorting]
    sorted_labels = np.array(_labels)[sorting]
    ax.legend(sorted_handles, sorted_labels, title=title, title_fontsize=28,
              loc='center left', bbox_to_anchor=(1, 0.5), fontsize=20)


def plot_piechart_by_pag(ax, df, pags, datatiers=None):
    if datatiers is not None:
        df = df[df['tier'].isin(datatiers)]
    data = [df[df['pwg'] == pag]['dsize'].sum() for pag in pags]
    df_other = df[(df['pwg'] != 'None') & (~df['pwg'].isin(pags))]
    data.append(df_other['dsize'].sum())
    df_not_found = df[df['pwg'] == 'None']
    data.append(df_not_found['dsize'].sum())
    labels = pags + ['Other PWG', 'Not found']
    sorted_colors = get_custom_colors(labels=labels, groups='pags')
    ax.pie(data, labels=labels, colors=sorted_colors, normalize=True, explode=[0.1]*len(data),
           autopct='%1.1f%%', pctdistance=1.1, textprops={'fontsize': 16}, labeldistance=None)
    total = round(df['dsize'].sum() / 1e15, 3)
    ax.set_title(f'Total size = {total} PB', fontsize=20)
    ax.legend(title='PAGs', title_fontsize=20, loc='center left',
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=16)


def plot_average_size_per_event(ax, df, datatiers):
    df = df[df['tier'].isin(datatiers)]
    years = sorted(list(df['year'].unique()))
    data = {}
    for dtier in datatiers:
        df_dtier = df[df['tier'] == dtier]
        data[dtier] = []
        for year in years:
            df_year = df_dtier[df_dtier['year'] == year]
            tot_size = df_year['dsize'].sum() / 1e3
            num_events = df_year['devts'].sum()
            data[dtier].append(
                tot_size / num_events if num_events != 0 else 0.)
    pos = np.arange(len(years))
    width = 0.9 / len(datatiers)
    colors = get_custom_colors(datatiers, groups='datatiers')
    bars = [ax.bar(pos + i*width, data[datatiers[i]], width=width, label=datatiers[i], color=colors[i])
            for i in range(len(datatiers))]
    ax.set_xticks(pos + (width / 2 * (len(datatiers) - 1)))
    ax.set_xticklabels(years, fontdict={'fontsize': 20})
    ax.set_yscale('log')
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    ax.yaxis.set_minor_formatter(FormatStrFormatter('%.0f'))
    ax.tick_params(axis='y', which='both', labelsize=14)
    ax.set_ylabel('Average size/event [KB]', fontsize=24)
    ax.grid(which='both', linestyle='dotted')
    ax.legend(bars, datatiers, title='Data tiers', title_fontsize=28, loc='center left',
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=20)
