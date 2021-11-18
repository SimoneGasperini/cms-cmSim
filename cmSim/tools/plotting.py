import numpy as np
from cmSim import utils


def norm_stacked_areas(time_series):
    time_series = np.array(time_series)
    tot_time_series = time_series.sum(axis=0)
    normed_time_series = time_series / tot_time_series
    return normed_time_series


def sort_stacked_areas(time_series, labels, more_labels=[]):
    time_series = np.array(time_series)
    labels = np.array(labels)
    l = len(labels)
    sorting = time_series[:l].mean(axis=1).argsort()[::-1]
    sorted_time_series = np.vstack((time_series[:l][sorting], time_series[l:]))
    sorted_labels = np.append(labels[sorting], more_labels)
    return sorted_time_series, sorted_labels


def get_colors(labels, groups):
    if groups == 'pags':
        lab_to_col = utils.get_pag_to_color()
    if groups == 'datatiers':
        lab_to_col = utils.get_datatier_to_color()
    if groups == 'datalakes':
        lab_to_col = utils.get_datalake_to_color()
    colors = [lab_to_col[lab] for lab in labels]
    return colors


def set_stackplot_settings(ax, ylabel, legend_title, legend_labels):
    ax.tick_params(axis='both', labelsize=14)
    ax.set_ylabel(ylabel, fontsize=18)
    handles, labels = _sort_legend_labels(ax, legend_labels)
    ax.legend(handles, labels, title=legend_title, title_fontsize=18,
              loc='center left', bbox_to_anchor=(1, 0.5), fontsize=16)
    ax.grid(linestyle='dotted')


def _sort_legend_labels(ax, labels):
    _handles, _labels = ax.get_legend_handles_labels()
    sorting = [np.where(np.array(_labels) == lab)[0][0] for lab in labels]
    sorted_handles = np.array(_handles)[sorting]
    sorted_labels = np.array(_labels)[sorting]
    return sorted_handles, sorted_labels


def plot_piechart_by_pag(ax, df, pags, datatiers=None):
    if datatiers is not None:
        df = df[df['tier'].isin(datatiers)]
    data = [df[df['pwg'] == pag]['dsize'].sum() for pag in pags]
    # Other PWG
    df_other = df[(df['pwg'] != 'None') & (~df['pwg'].isin(pags))]
    data.append(df_other['dsize'].sum())
    # PWG not found
    df_not_found = df[df['pwg'] == 'None']
    data.append(df_not_found['dsize'].sum())
    labels = pags + ['Other PWG', 'Not found']
    sorted_colors = get_colors(labels=labels, groups='pags')
    ax.pie(data, labels=labels, colors=sorted_colors, normalize=True, explode=[0.1]*len(data),
           autopct='%1.1f%%', pctdistance=1.1, textprops={'fontsize': 16}, labeldistance=None)
    total = round(df['dsize'].sum() / 1e15, 3)
    ax.set_title(f'Total size = {total} PB', fontsize=20)
    ax.legend(title='PAGs', title_fontsize=18, loc='center left',
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=16)
