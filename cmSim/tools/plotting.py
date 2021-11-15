import numpy as np
from cmSim import utils


def norm_stacked_areas(time_series):
    time_series = np.array(time_series)
    tot_time_series = time_series.sum(axis=0)
    normed_time_series = time_series / tot_time_series
    return normed_time_series


def sort_stacked_areas(time_series, labels, more_labels):
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
