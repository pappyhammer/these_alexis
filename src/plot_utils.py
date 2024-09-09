import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import plotly.express as px
# from plotly.subplots import make_subplots
# from plotly.graph_objects import Layout
# import matplotlib.gridspec as gridspec
# from matplotlib import patches
# import seaborn as sns
from datetime import datetime
# import matplotlib.cm as cm
import numpy as np
import math
import os
import pandas as pd
from matplotlib import rcParams
import seaborn as sns

# qualitative 12 colors : http://colorbrewer2.org/?type=qualitative&scheme=Paired&n=12 + 11 diverting
BREWER_COLORS = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c', '#fdbf6f',
                 '#ff7f00', '#cab2d6', '#6a3d9a', '#ffff99', '#b15928', '#a50026', '#d73027',
                 '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9',
                 '#74add1', '#4575b4', '#313695']


# matplotlib: https://matplotlib.org/stable/gallery/index.html

def extend_brewer_colors(data):
    """
    Return a list of colors of length > len(data)
    :param data:
    :return:
    """
    colors = BREWER_COLORS
    while len(colors) < len(data):
        colors = colors + BREWER_COLORS
    return colors


class EpilepsiaColor:
    colors = {"rose pale": "#e4b8b4",
              "rose normal": "#ce8080",
              "rose fonce": "#a30234",
              "rose fonce++": "#511c23",
              "orange clair": "#f1b682",
              "orange fonce": "#e37c1d",
              "jaune": "#ffde75",
              "vert clair": "#abb47d",
              "vert fonce": "#677719",
              "vert emeraude clair": "#a1c5cb",
              "vert emeraude normal": "#5698a3",
              "vert emeraude fonce": "#00545e",
              "vert emeraude fonce++": "#002e30",
              "bleu clair": "#bacfec",
              "bleu normal": "#0076c0",
              "bleu fonce": "#002157",
              "bleu mauve": "#7a5071"}

    def __init__(self):
        pass


def plot_pie_chart_px(data_dict, label_data, path_results, filename,
                      background_color="white",
                      uniformtext_minsize=30,
                      save_formats="png",
                      show_legend=False,
                      color_discrete_map=None,
                      with_timestamp_in_file_name=True):
    """
    Produce a pie chart
    :param data_dict: dict each key is a label and the value is an integer representing the number of elements of each
    label
    :param path_results: path where to save the figure
    :param filename: name of the figure without extension
    :param background_color: background color
    :param uniformtext_minsize:  text size if uniform
    :param save_formats: (str or list of str) format in which to save the data
    :param show_legend: (bool)
    :param color_discrete_map: if not None, used to color each label, key is a label, same as data_dict,
    value is a color. Otherwise color are random, from BREWER_COLORS set.
    :param with_timestamp_in_file_name:
    :return:
    """

    data_dict_pie = dict()
    data_dict_pie[label_data] = []
    data_dict_pie["n"] = []
    if color_discrete_map is not None:
        colors_set = True
    else:
        color_discrete_map = dict()
        colors_set = False
    index_data = 0
    if not colors_set:
        colors = BREWER_COLORS
        while len(colors) < len(data_dict):
            colors = colors + BREWER_COLORS
    for key_label, n in data_dict.items():
        data_dict_pie[label_data].append(key_label)
        if not colors_set:
            color_discrete_map[key_label] = colors[index_data]
        index_data += 1
        data_dict_pie["n"].append(n)

    plot_pie_chart_px_raw(data_dict_pie, names=label_data, values="n",
                          path_results=path_results, filename=filename,
                          background_color=background_color,
                          color_discrete_map=color_discrete_map,
                          save_formats=save_formats,
                          show_legend=show_legend,
                          uniformtext_minsize=uniformtext_minsize,
                          with_timestamp_in_file_name=with_timestamp_in_file_name)


def plot_pie_chart(data_dict, path_results, filename, label_data=None,
                   with_sizes=True,
                   dpi=400, save_formats="png",
                   background_color="white",
                   fontsize=16,
                   labels_color="black",
                   color_discrete_map=None,
                   with_timestamp_in_file_name=True):
    """

    :param data_dict:
    :param path_results:
    :param filename:
    :param label_data:
    :param with_sizes:
    :param dpi:
    :param save_formats:
    :param background_color:
    :param fontsize:
    :param labels_color:
    :param color_discrete_map:
    :param with_timestamp_in_file_name:
    :return:
    """
    # https://proclusacademy.com/blog/customize_matplotlib_piechart/
    labels = list(data_dict.keys())
    sizes = list(data_dict.values())

    rcParams.update({'figure.autolayout': True})

    fig, axe_plot = plt.subplots(nrows=1, ncols=1,
                                 gridspec_kw={'height_ratios': [1]},
                                 figsize=(12, 12), dpi=dpi)

    axe_plot.set_facecolor(background_color)

    fig.patch.set_facecolor(background_color)

    if color_discrete_map is not None:
        colors = [color_discrete_map[label] for label in labels]
    else:
        colors = extend_brewer_colors(data=list(data_dict.keys()))[:len(data_dict)]

    if with_sizes:
        labels = [label + f"\n({s})" for label, s in zip(labels, sizes)]

    # autotexts A list of Text instances for the numeric labels.
    # This will only be returned if the parameter autopct is not None.
    patches, texts, autotexts = axe_plot.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontsize': fontsize},
                                             pctdistance=1.15, labeldistance=.6, colors=colors)

    for text in texts:
        text.set_fontweight('bold')
        text.set_horizontalalignment('center')

    for text in autotexts:
        text.set_fontweight('bold')
        text.set_horizontalalignment('center')

    axe_plot.spines['bottom'].set_visible(False)
    axe_plot.spines['right'].set_visible(False)
    axe_plot.spines['top'].set_visible(False)
    axe_plot.spines['left'].set_visible(False)

    axe_plot.grid(False)
    axe_plot.xaxis.set_ticks_position('none')
    axe_plot.yaxis.set_ticks_position('none')

    rcParams.update({'figure.autolayout': True})

    if with_timestamp_in_file_name:
        time_str = "_" + datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
    else:
        time_str = ""

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def plot_pie_chart_px_raw(data_dict, names, values, path_results, filename,
                          background_color=None,
                          uniformtext_minsize=30,
                          save_formats="png",
                          show_legend=False,
                          color_discrete_map=None,
                          with_timestamp_in_file_name=True):
    """

    :param data_dict: dict with 2 keys, one being the label data and the other the number representing the label.
    Values are list
    :param names: (str) name of the key in data_dict containing the label data
    :param values: (str) name of the key in data_dict containing the values
    :param path_results: path where to save the figure
    :param filename: name of the figure without extension
    :param background_color: background color
    :param uniformtext_minsize:  text size if uniform
    :param save_formats: (str or list of str) format in which to save the data
    :param show_legend: (bool)
    :param color_discrete_map:
    :param with_timestamp_in_file_name:
    :return:
    """
    # layout = Layout(plot_bgcolor=background_color)
    df = pd.DataFrame(data_dict)
    if color_discrete_map is not None:
        fig = px.pie(df, values=values, names=names, color=names, color_discrete_map=color_discrete_map)
    else:
        fig = px.pie(df, values=values, names=names)
    # text=['$' + price for price in pie_chart.price.values],
    # textinfo='text',
    # fig.update_traces(textposition='inside', textinfo='percent+label')
    # TODO: see to change the font
    fig.update_traces(textposition='inside', textinfo='label+value')
    fig.update_layout(uniformtext_minsize=uniformtext_minsize, uniformtext_mode='hide')
    # fig.update_traces(textinfo='percent+label')
    # textinfo='value'
    if background_color is not None:
        fig.update_layout(paper_bgcolor=background_color)
    # fig.patch.set_facecolor(background_color)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    fig_perc_option = True
    if fig_perc_option:
        if color_discrete_map is not None:
            fig_perc = px.pie(df, values=values, names=names, color=names, color_discrete_map=color_discrete_map)
        else:
            fig_perc = px.pie(df, values=values, names=names)
        fig_perc.update_traces(textposition='outside', textinfo='percent')
        # fig.update_layout(uniformtext_minsize=uniformtext_minsize, uniformtext_mode='hide')
        # fig.update_traces(textinfo='percent+label')
        # textinfo='value'
        if background_color is not None:
            fig_perc.update_layout(paper_bgcolor=background_color)

    if fig_perc_option:
        fig_perc.add_traces(list(fig.select_traces()))
        fig_perc.update_layout(showlegend=show_legend)
        for save_format in save_formats:
            fig_perc.write_image(f'{path_results}/{filename}_{time_str}.{save_format}', scale=6,
                                 width=1080, height=1080)
    else:
        for save_format in save_formats:
            fig.write_image(f'{path_results}/{filename}_{time_str}.{save_format}', scale=6, width=1080, height=1080)


def plot_sunburst(filename, save_formats="pdf",
                  dpi=200,
                  with_timestamp_in_file_name=True):
    pass


def plot_stackplots(data_dict, xticklabels, path_results, filename,
                    x_label, y_label,
                    colors,
                    y_lim=None,
                    x_labels_rotation=None,
                    labels_color="black",
                    dpi=400, save_formats="png",
                    background_color="white",
                    with_timestamp_in_file_name=True):
    """

    :param data_dict: (str, list) key is will be a legend (a color to fill), value is the size at each x to fill.
    :param xticklabels: (list) name of the x-ticks, should be the length as list in values of data_dict
    :param path_results:
    :param filename:
    :param x_label:
    :param y_label:
    :param colors: same length as values in data_dict
    :param y_lim:
    :param x_labels_rotation:
    :param labels_color:
    :param dpi:
    :param save_formats:
    :param background_color:
    :param with_timestamp_in_file_name:
    :return:
    """
    rcParams.update({'figure.autolayout': True})

    fig, ax1 = plt.subplots(nrows=1, ncols=1,
                            gridspec_kw={'height_ratios': [1]},
                            figsize=(12, 12), dpi=dpi)

    ax1.set_facecolor(background_color)

    fig.patch.set_facecolor(background_color)
    ax1.stackplot(xticklabels, data_dict.values(),
                  labels=data_dict.keys(), alpha=0.8, colors=colors,
                  edgecolor="black",
                  linewidth=2)

    ax1.legend()

    # add tick at every ...
    # axe_plot.yaxis.set_minor_locator(mticker.MultipleLocator(.2))

    ax1.set_ylabel(f"{y_label}", fontsize=30, labelpad=20, fontweight="bold")
    if y_lim is not None:
        ax1.set_ylim(y_lim[0], y_lim[1])
    if x_label is not None:
        ax1.set_xlabel(x_label, fontsize=30, labelpad=20)
    ax1.xaxis.label.set_color(labels_color)
    ax1.yaxis.label.set_color(labels_color)

    ax1.yaxis.set_tick_params(labelsize=20)
    # if y_ticks_locations is not None and y_ticks_labels is not None:
    #     plt.yticks(y_ticks_locations, y_ticks_labels)

    ax1.spines['bottom'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)

    ax1.xaxis.set_tick_params(labelsize=15)
    ax1.tick_params(axis='y', colors=labels_color)
    ax1.tick_params(axis='x', colors=labels_color)
    plt.xticks(fontweight="bold")
    xticks = np.arange(0, len(xticklabels))
    ax1.set_xticks(xticks)
    # ax1.set_xlim(0, len(data_dict))
    # removing the ticks but not the labels
    ax1.xaxis.set_ticks_position('none')
    # sce clusters labels

    # ax1.set_xticklabels(labels)
    if x_labels_rotation is not None:
        for tick in ax1.get_xticklabels():
            tick.set_rotation(x_labels_rotation)

    # if colorfull_xticklabels:
    #     for i_label in range(n_box_plots):
    #         # we put for the label of the tick the same color as the boxplot
    #         ax1.get_xticklabels()[i_label].set_color(colors[i_label])

    # padding between ticks label and  label axis
    # ax1.tick_params(axis='both', which='major', pad=15)
    fig.tight_layout()
    # adjust the space between axis and the edge of the figure
    # https://matplotlib.org/faq/howto_faq.html#move-the-edge-of-an-axes-to-make-room-for-tick-labels
    # fig.subplots_adjust(left=0.2)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def plot_box_plots(data_dict, filename,
                   y_label,
                   box_in_front=False,
                   ordered_labels=None,
                   scatter_text_dict=None,
                   colors=None,
                   path_results=None, y_lim=None,
                   x_label=None, with_scatters=True,
                   xticklabels_dict=None,
                   y_log=False,
                   scatters_with_same_colors=None,
                   special_scatters=None,
                   scatter_size=20,
                   scatter_alpha=0.5,
                   box_alpha=0.8,
                   h_lines_y_values=None,
                   h_lines_colors=None,
                   h_lines_styles="dashed",
                   n_sessions_dict=None,
                   y_ticks_locations=None,
                   y_ticks_labels=None,
                   median_color=None,
                   background_color="black",
                   link_medians=False,
                   link_means=False,
                   link_data_points=None,
                   color_link_medians="red",
                   color_link_means="red",
                   color_link_data_point="red",
                   labels_color="white",
                   with_y_jitter=None,
                   x_labels_rotation=None,
                   fliers_symbol=None,
                   save_formats="pdf",
                   dpi=200,
                   xkcd_mode=False,
                   with_timestamp_in_file_name=True):
    """

    :param data_dict: each key is a label for the data, and each value is a list of int or float
    :param scatter_text_dict: same dimension of data_dict, for each value associate a string that will be displayed
    in the scatter if with_scatters is True
    :param ordered_labels: if not None, list of str (same as key of data_dict) allowing to sort the boxplots according
    to this order
    :param box_in_front: if True, but the boxplot in front of the scatter, with some transparency
    :param colors: list of colors, if not None, the colors will be used to color the boxplot. If there are
    less colors than boxplot, then it will be looped
    :param median_color: color of the line representing the median in the boxplot, if None will be the
    same as the background if colorful boxplot otherwise labels_color
    :param n_sessions_dict: should be the same keys as data_dict, value is an int reprenseing the number of sessions
    that gave those data (N), a n will be display representing the number of poins in the boxplots if n != N
    :param link_medians: if True then links the median of each boxplots. Can also take a list of value, the list will
    be a list of list containing an ensemble of boxplot index to link, from 0 to n_boxplots-1
    :param link_means: same as link_medians but with the mean value
    :param filename:
    :param y_label:
    :param y_ticks_locations:
    :param y_ticks_labels:
    :param h_lines_y_values: if not None, list of float reprenting y-axis coordinate where to plot o line
    :param h_lines_styles: (str) style of horizontal lines, such as "dashed"
    :param h_lines_colors: None or list of same length of h_lines_y_values containing colors
    of the horizontal lines
    :param special_scatters: plot some special scatter, dict with key is a label from boxplot and value is a list
    of lists of length 4 with 1st element being the y_coord, then the color and 3rd being the marker (str such as '*"),
    4th scatter size (int)
    :param xticklabels_dict: dict with key the label (idem key in data_dict) and value a str to display for the boxplot
    :param y_lim: tuple of int,
    :param color_link_data_point: color of the links between data points. Can be just a color (same for all)
    or a list of colors, if the list is shorter than the number of links, then a modulo will be used to loop
    the list
    :param link_data_points: if not None, represent the indexes of the points to link.
    It's a list of list, each list is composed of int there should be as many int as there are boxplots.
    :param scatters_with_same_colors: scatter that have the same index in the data_dict,, will be colors
    with the same colors, using the list of colors given by scatters_with_same_colors
    :param save_formats:
    :return:
    """
    fig, ax1 = plt.subplots(nrows=1, ncols=1,
                            gridspec_kw={'height_ratios': [1]},
                            figsize=(12, 12), dpi=dpi)

    colorfull = (colors is not None)

    if median_color is None:
        median_color = background_color if colorfull else labels_color

    scatter_edgecolors = labels_color

    if xkcd_mode:
        plt.xkcd()

    ax1.set_facecolor(background_color)

    fig.patch.set_facecolor(background_color)

    labels = []
    data_list = []
    scatter_text_list = []
    medians_values = []
    means_values = []
    label_to_index_dict = dict()
    if ordered_labels is None:
        ordered_labels = list(data_dict.keys())
    for label_index, label in enumerate(ordered_labels):
        label_to_index_dict[label] = label_index
        data = data_dict[label]
        data_list.append(data)
        if scatter_text_dict is not None:
            scatter_text_list.append(scatter_text_dict[label])
        medians_values.append(np.median(data))
        means_values.append(np.mean(data))
        if xticklabels_dict is not None and label in xticklabels_dict:
            labels.append(xticklabels_dict[label])
        else:
            labels.append(label)
    sym = ""
    if fliers_symbol is not None:
        sym = fliers_symbol

    n_box_plots = len(data_list)

    if box_in_front:
        z_order_box = 25
    else:
        z_order_box = 20
    bplot = plt.boxplot(data_list, patch_artist=colorfull,
                        labels=labels, sym=sym, zorder=z_order_box)  # whis=[5, 95], sym='+'
    # color=["b", "cornflowerblue"],
    # fill with colors

    # edge_color="silver"

    for element in ['boxes', 'whiskers', 'fliers', 'caps']:
        plt.setp(bplot[element], color="white")

    for element in ['means', 'medians']:
        plt.setp(bplot[element], color=median_color)

    if colorfull:
        while len(colors) < len(data_dict):
            colors.extend(colors)
        colors = colors[:len(data_dict)]
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
            r, g, b, a = patch.get_facecolor()
            # for transparency purpose
            patch.set_facecolor((r, g, b, box_alpha))

    if with_scatters:
        # used to link data_points if asked
        # key is an int representing the index of the list of link_data_points, the value
        # is the value (flot or int) that represents the coordinates of each point of the line
        x_pos_links = dict()
        y_pos_links = dict()
        for data_index, data in enumerate(data_list):
            # data_index == box_plot_index
            # Adding jitter
            x_pos = [1 + data_index + ((np.random.random_sample() - 0.5) * 0.5) for x in np.arange(len(data))]

            if with_y_jitter is not None:
                y_pos = [value + (((np.random.random_sample() - 0.5) * 2) * with_y_jitter) for value in data]
            else:
                y_pos = data

            if link_data_points is not None:
                for list_index, data_points_indices in enumerate(link_data_points):
                    if list_index not in x_pos_links:
                        x_pos_links[list_index] = []
                    if list_index not in y_pos_links:
                        y_pos_links[list_index] = []
                    data_point_index = data_points_indices[data_index]
                    x_pos_links[list_index].append(x_pos[data_point_index])
                    y_pos_links[list_index].append(y_pos[data_point_index])

            colors_scatters = []
            if scatters_with_same_colors is not None:
                while len(colors_scatters) < len(y_pos):
                    colors_scatters.extend(scatters_with_same_colors)
            else:
                colors_scatters = [colors[data_index]]

            if box_in_front:
                z_order_scatter = 21
            else:
                z_order_scatter = 21
            ax1.scatter(x_pos, y_pos,
                        color=colors_scatters[:len(y_pos)],
                        alpha=scatter_alpha,
                        marker="o",
                        edgecolors=scatter_edgecolors,
                        s=scatter_size, zorder=z_order_scatter)
            # plotting text in the scatter if given so
            if scatter_text_dict is not None:
                scatter_text_data = scatter_text_list[data_index]
                for scatter_index in np.arange(len(data)):
                    scatter_text = str(scatter_text_data[scatter_index])
                    if len(scatter_text) > 3:
                        font_size = 2
                    else:
                        font_size = 3
                    ax1.text(x=x_pos[scatter_index], y=y_pos[scatter_index],
                             s=scatter_text, color=labels_color, zorder=22,
                             ha='center', va="center", fontsize=font_size, fontweight='bold')
    if link_medians:
        if isinstance(link_medians, list):
            for coords in link_medians:
                median_values_to_link = [medians_values[c] for c in coords]
                ax1.plot([c + 1 for c in coords], median_values_to_link, zorder=30, color=color_link_medians,
                         linewidth=2)
        else:
            ax1.plot(np.arange(1, len(medians_values) + 1), medians_values, zorder=30, color=color_link_medians,
                     linewidth=2)

    if link_means:
        if isinstance(link_means, list):
            for coords in link_means:
                mean_values_to_link = [means_values[c] for c in coords]
                ax1.plot([c + 1 for c in coords], mean_values_to_link, zorder=30, color=color_link_means,
                         linewidth=2)
        else:
            ax1.plot(np.arange(1, len(means_values) + 1), means_values, zorder=30, color=color_link_means,
                     linewidth=2)

    if special_scatters:
        for label in ordered_labels:
            if label not in special_scatters:
                continue
            for scatter_data in special_scatters[label]:
                ax1.scatter(label_to_index_dict[label] + 1, scatter_data[0],
                            # color=colors[label_to_index_dict[label]],
                            color=scatter_data[1],
                            alpha=1,
                            marker=scatter_data[2],  # "*",
                            edgecolors=scatter_edgecolors,
                            s=scatter_data[3], zorder=35)

    if link_data_points is not None and with_scatters:
        for key_index, x_positions in x_pos_links.items():
            y_positions = y_pos_links[key_index]
            color_link = color_link_data_point
            if isinstance(color_link, list):
                color_link = color_link[key_index % len(color_link)]
            if box_in_front:
                z_order_links = 23
            else:
                z_order_links = 35
            ax1.plot(x_positions, y_positions, zorder=z_order_links, color=color_link,
                     linewidth=0.5)

    # plt.xlim(0, 100)
    # plt.title(title)

    if h_lines_y_values is not None:
        for index_h_line, y_value in enumerate(h_lines_y_values):
            color_line = labels_color
            if h_lines_colors is not None:
                color_line = h_lines_colors[index_h_line]
            ax1.hlines(y_value, 0,
                       n_box_plots, color=color_line, linewidth=0.5,
                       linestyles=h_lines_styles, zorder=1)

    ax1.set_ylabel(f"{y_label}", fontsize=30, labelpad=20, fontweight="bold")
    if y_lim is not None:
        ax1.set_ylim(y_lim[0], y_lim[1])
    if x_label is not None:
        ax1.set_xlabel(x_label, fontsize=30, labelpad=20)
    ax1.xaxis.label.set_color(labels_color)
    ax1.yaxis.label.set_color(labels_color)
    if y_log:
        ax1.set_yscale("log")

    ax1.yaxis.set_tick_params(labelsize=20)
    if y_ticks_locations is not None and y_ticks_labels is not None:
        plt.yticks(y_ticks_locations, y_ticks_labels)

    if n_box_plots > 20:
        ax1.xaxis.set_tick_params(labelsize=5)
    elif n_box_plots > 14:
        ax1.xaxis.set_tick_params(labelsize=7)
    elif n_box_plots > 8:
        ax1.xaxis.set_tick_params(labelsize=12)
    else:
        ax1.xaxis.set_tick_params(labelsize=15)
    ax1.tick_params(axis='y', colors=labels_color)
    ax1.tick_params(axis='x', colors=labels_color)
    plt.xticks(fontweight="bold")
    xticks = np.arange(1, len(data_dict) + 1)
    ax1.set_xticks(xticks)
    # removing the ticks but not the labels
    ax1.xaxis.set_ticks_position('none')
    # sce clusters labels

    ax1.set_xticklabels(labels)
    if x_labels_rotation is not None:
        for tick in ax1.get_xticklabels():
            tick.set_rotation(x_labels_rotation)

    if colorfull:
        for i_label in range(n_box_plots):
            # we put for the label of the tick the same color as the boxplot
            ax1.get_xticklabels()[i_label].set_color(colors[i_label])

    # padding between ticks label and  label axis
    # ax1.tick_params(axis='both', which='major', pad=15)
    fig.tight_layout()
    # adjust the space between axis and the edge of the figure
    # https://matplotlib.org/faq/howto_faq.html#move-the-edge-of-an-axes-to-make-room-for-tick-labels
    # fig.subplots_adjust(left=0.2)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def sns_scatter_plot(data_frame, file_name, colors=None, save_formats="pdf", labels_color="white",
                     background_color="black", figsize=(16, 10)):
    """
    Scatter plot using seaborn
    :param data_frame:
    :param file_name:
    :param colors: if NOne, no colors
    :param save_formats:
    :param labels_color:
    :param background_color:
    :param figsize:
    :return:
    """
    plt.figure(figsize=figsize)
    # plt.setp(svm.get_legend().get_texts(), fontcolor=labels_color)
    ax = plt.gca()
    ax.set_facecolor(background_color)

    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    sns.set(rc={'axes.facecolor': background_color, 'figure.facecolor': background_color})

    if colors is None:
        svm = sns.scatterplot(
            x="tsne-2d-one", y="tsne-2d-two",
            data=data_frame,
            legend="full",
            alpha=1
        )
    else:
        svm = sns.scatterplot(
            x="tsne-2d-one", y="tsne-2d-two",
            hue="color",
            palette=sns.color_palette(palette=colors),
            data=data_frame,
            legend="full",
            alpha=1
        )
    plt.setp(svm.get_legend().get_title(), color=labels_color)
    plt.setp(svm.get_legend().get_texts(), color=labels_color)
    # for text in svm.get_legend().get_texts():
    #     text.set_color(labels_color)
    svm.set(xticklabels=[])
    svm.set(yticklabels=[])
    svm.set(xlabel=None)
    svm.set(ylabel=None)
    svm.grid(False)
    # Turns off grid on the secondary (right) Axis.
    # svm.right_ax.grid(False)
    svm.tick_params(bottom=False)
    svm.tick_params(left=False)

    fig = svm.get_figure()
    fig.patch.set_facecolor(background_color)

    for save_format in save_formats:
        fig.savefig(f'{file_name}'
                    f'.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())
    plt.close()


def plot_image(image, path_results, filename, interpolation="bilinear", save_formats="pdf",
               dpi=200, with_timestamp_in_file_name=True):
    rcParams.update({'figure.autolayout': True})

    fig, axe_plot = plt.subplots(nrows=1, ncols=1,
                                 gridspec_kw={'height_ratios': [1]},
                                 figsize=(12, 12), dpi=dpi)

    axe_plot.imshow(image, interpolation=interpolation)

    axe_plot.spines['bottom'].set_visible(False)
    axe_plot.spines['right'].set_visible(False)
    axe_plot.spines['top'].set_visible(False)
    axe_plot.spines['left'].set_visible(False)

    axe_plot.grid(False)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def plot_stacked_bar(data_dict,
                     data_colors,
                     data_legends,
                     x_ticks_labels,
                     path_results,
                     y_label,
                     x_ticks_label_size,
                     filename,
                     color_each_bar=False,
                     h_lines_y_values=None,
                     h_lines_colors=None,
                     y_ticks_locations=None,
                     y_ticks_labels=None,
                     x_ticks_colors_dict=None,
                     x_label=None,
                     bars_text_dict=None,
                     bars_text_color="white",
                     width_bar=0.5,
                     background_color="black",
                     labels_color="white",
                     x_ticks_vertical_rotation=True,
                     x_ticks_rotation_angle=45,
                     save_formats="pdf",
                     legend_text_color="black",
                     xkcd_mode=False,
                     dpi=200,
                     with_timestamp_in_file_name=True,
                     verbose=False):
    """

    :param data_dict:  len == number of bar, key is the xticks label (str), value is a list of float
    or int representing a subpart of a bar
    :param data_colors: list of colors, same order as the data in data_dict values
    :param data_legends: list of str, same order as the data in data_dict values
    :param x_ticks_labels: list of str, each one should be in  data_dict keys, the order of the list will be the order of the bar
    :param bars_text_dict: if None, no text is displayed in the bars, if not, dict with keys being the xticks label
    (str), value is a list of str representing the text to display in the subpart of a bar (list should be the same
    length of the one if data_dict)
    :param bars_text_color: color of the text to display in bars (if bars_text_dict is not None)
    :param path_results:
    :param color_each_bar: if True, instead of coloring each sector of a bar in a different color, each bar
    has its own color defined in data_colors
    :param h_lines_y_values: if not None, list of int reprenseting y value at which draw an horizontal line
    :param h_lines_colors: if not None, list of colors (same len as h_lines_y_values) representing the color
    of the horizontal lines
    :param y_label:
    :param x_ticks_label_size:
    :param filename:
    :param y_ticks_locations:
    :param y_ticks_labels:
    :param x_ticks_colors_dict: key is x_tick_label str, and value a color. if None or no color for a given label
    labels_color will be used
    :param x_label:
    :param background_color:
    :param labels_color:
    :param x_ticks_vertical_rotation:
    :param save_formats:
    :param with_timestamp_in_file_name:
    :param verbose:
    :return:
    """
    if x_ticks_colors_dict is None:
        x_ticks_colors_dict = dict()

    rcParams.update({'figure.autolayout': True})

    fig, axe_plot = plt.subplots(nrows=1, ncols=1,
                                 gridspec_kw={'height_ratios': [1]},
                                 figsize=(12, 12), dpi=dpi)

    if xkcd_mode:
        plt.xkcd()

    axe_plot.set_facecolor(background_color)

    fig.patch.set_facecolor(background_color)

    x_pos = np.arange(0, len(x_ticks_labels))
    plt_bar_list = [None] * len(data_legends)
    for x_ticks_index, x_ticks_label in enumerate(x_ticks_labels):
        # linewidth = np.repeat(1, len(x_ticks_labels))
        # linewidth[reg_variants_freq[i, :] == 0] = 0
        bar_values = data_dict[x_ticks_label]
        for index_bar_value, bar_value in enumerate(bar_values):
            if color_each_bar:
                p = plt.bar(x_ticks_index,
                            bar_value, color=data_colors[x_ticks_index],
                            edgecolor=background_color, linewidth=1, width=width_bar,
                            bottom=np.sum(bar_values[:index_bar_value]), zorder=18)
            else:
                p = plt.bar(x_ticks_index,
                            bar_value, color=data_colors[index_bar_value],
                            edgecolor=background_color, linewidth=1, width=width_bar,
                            bottom=np.sum(bar_values[:index_bar_value]), zorder=18)
            plt_bar_list[index_bar_value] = p
        if bars_text_dict:
            bars_text_data = bars_text_dict[x_ticks_label]
            for index_bar_value, bar_text in enumerate(bars_text_data):
                if bar_values[index_bar_value] == 0:
                    # no text if no bar
                    continue
                y_pos = np.sum(bar_values[:index_bar_value]) + (bar_values[index_bar_value] / 2)
                fontsize = 14
                if len(x_ticks_labels) > 3:
                    fontsize -= 1
                if len(x_ticks_labels) > 6:
                    fontsize -= 5
                if len(x_ticks_labels) > 20:
                    fontsize -= 3
                plt.text(x=x_ticks_index, y=y_pos,
                         s=str(bar_text),
                         color=bars_text_color, zorder=22,
                         ha='center', va="center", fontsize=fontsize, fontweight='bold')

    if h_lines_y_values:
        for h_lines_y_value in h_lines_y_values:
            axe_plot.hlines(h_lines_y_value, x_pos[0],
                            x_pos[-1], color=h_lines_colors, linewidth=2,
                            linestyles="dashed", zorder=1)

    if len(x_pos) > 10:
        x_ticks_label_size -= 2
    if x_ticks_vertical_rotation:
        plt.xticks(x_pos, x_ticks_labels, fontsize=x_ticks_label_size, fontweight="bold",
                   rotation=x_ticks_rotation_angle)
    else:
        plt.xticks(x_pos, x_ticks_labels, fontsize=x_ticks_label_size, fontweight="bold")

    x_ticks_colors = []
    for label in x_ticks_labels:
        if label in x_ticks_colors_dict:
            x_ticks_colors.append(x_ticks_colors_dict[label])
        else:
            x_ticks_colors.append(labels_color)
    for color, tick in zip(x_ticks_colors, axe_plot.xaxis.get_major_ticks()):
        tick.label1.set_color(color)

    axe_plot.spines['bottom'].set_visible(False)
    axe_plot.spines['right'].set_visible(False)
    axe_plot.spines['top'].set_visible(False)
    axe_plot.spines['left'].set_visible(False)

    axe_plot.grid(False)
    # axe_plot.set_ylim(-0.05, max_variant_freq)

    # y_pos = np.arange(0, int(np.ceil(max_variant_freq)) + 1)
    if y_ticks_locations is not None and y_ticks_labels is not None:
        plt.yticks(y_ticks_locations, y_ticks_labels)
    axe_plot.tick_params(axis='y', colors=labels_color)
    # axe_plot.tick_params(axis='x', colors=labels_color)
    # removing the ticks but not the labels
    axe_plot.xaxis.set_ticks_position('none')
    axe_plot.yaxis.set_tick_params(labelsize=15)
    plt.ylabel(y_label, fontweight="bold", fontsize=30, labelpad=20)
    if x_label is not None:
        axe_plot.set_xlabel(x_label, fontsize=30, labelpad=20)
    axe_plot.xaxis.label.set_color(labels_color)
    axe_plot.yaxis.label.set_color(labels_color)

    if len(data_dict) == 1:
        axe_plot.set_xlim(-1, 1)

    # grid
    # for i in np.arange(1, int(np.ceil(local_max_variant_freq) + 1)):
    #     plt.hlines(i, -0.4, n_aeds - 1 + 0.4, color="grey", linewidth=1, linestyles="dashed", zorder=1, alpha=0.2)

    rcParams['axes.titlepad'] = 40

    rcParams.update({'figure.autolayout': True})

    if len(data_legends) > 1:
        leg = plt.legend(plt_bar_list, data_legends)
        plt.setp(axe_plot.get_legend().get_texts(), color=legend_text_color)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def plot_hist_distribution(distribution_data,
                           filename=None,
                           values_to_scatter=None,
                           n_bins=None,
                           use_log=False,
                           x_range=None,
                           labels=None,
                           scatter_shapes=None,
                           colors=None,
                           tight_x_range=False,
                           twice_more_bins=False,
                           scale_them_all=False,
                           background_color="black",
                           hist_facecolor="white",
                           hist_edgeccolor="white",
                           axis_labels_color="white",
                           axis_color="white",
                           axis_label_font_size=20,
                           ticks_labels_color="white",
                           ticks_label_size=14,
                           xlabel=None,
                           ylabel=None,
                           fontweight=None,
                           fontfamily=None,
                           size_fig=None,
                           dpi=100,
                           path_results=None,
                           save_formats="pdf",
                           ax_to_use=None,
                           color_to_use=None, legend_str=None,
                           density=False,
                           save_figure=False,
                           with_timestamp_in_file_name=True,
                           max_value=None):
    """
    Plot a distribution in the form of an histogram, with option for adding some scatter values
    :param distribution_data:
    :param description:
    :param param:
    :param values_to_scatter:
    :param labels:
    :param scatter_shapes:
    :param colors:
    :param tight_x_range:
    :param twice_more_bins:
    :param xlabel:
    :param ylabel:
    :param save_formats:
    :return:
    """
    distribution = np.array(distribution_data)

    if x_range is not None:
        min_range = x_range[0]
        max_range = x_range[1]
    elif tight_x_range:
        max_range = np.max(distribution)
        min_range = np.min(distribution)
    else:
        max_range = 100
        min_range = 0
    weights = (np.ones_like(distribution) / (len(distribution))) * 100
    # weights=None

    if ax_to_use is None:
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=size_fig, dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
    else:
        ax1 = ax_to_use
    if n_bins is not None:
        bins = n_bins
    else:
        bins = int(np.sqrt(len(distribution)))
        if twice_more_bins:
            bins *= 2

    hist_color = hist_facecolor
    if bins > 100:
        edge_color = hist_color
    else:
        edge_color = hist_edgeccolor
    ax1.spines['bottom'].set_color(axis_color)
    ax1.spines['left'].set_color(axis_color)

    if labels is None:
        labels = []

    hist_plt, edges_plt, patches_plt = ax1.hist(distribution, bins=bins, range=(min_range, max_range),
                                                facecolor=hist_color, log=use_log,
                                                edgecolor=edge_color, label=legend_str,
                                                weights=weights, density=density)
    if values_to_scatter is not None:
        scatter_bins = np.ones(len(values_to_scatter), dtype="int16")
        scatter_bins *= -1

        for i, edge in enumerate(edges_plt):
            # print(f"i {i}, edge {edge}")
            if i >= len(hist_plt):
                # means that scatter left are on the edge of the last bin
                scatter_bins[scatter_bins == -1] = i - 1
                break

            if len(values_to_scatter[values_to_scatter <= edge]) > 0:
                if (i + 1) < len(edges_plt):
                    bool_list = values_to_scatter < edge  # edges_plt[i + 1]
                    for i_bool, bool_value in enumerate(bool_list):
                        if bool_value:
                            if scatter_bins[i_bool] == -1:
                                new_i = max(0, i - 1)
                                scatter_bins[i_bool] = new_i
                else:
                    bool_list = values_to_scatter < edge
                    for i_bool, bool_value in enumerate(bool_list):
                        if bool_value:
                            if scatter_bins[i_bool] == -1:
                                scatter_bins[i_bool] = i

        decay = np.linspace(1.1, 1.15, len(values_to_scatter))
        for i, value_to_scatter in enumerate(values_to_scatter):
            if i < len(labels):
                ax1.scatter(x=value_to_scatter, y=hist_plt[scatter_bins[i]] * decay[i], marker=scatter_shapes[i],
                            color=colors[i], s=60, zorder=20, label=labels[i])
            else:
                ax1.scatter(x=value_to_scatter, y=hist_plt[scatter_bins[i]] * decay[i], marker=scatter_shapes[i],
                            color=colors[i], s=60, zorder=20)
    if len(labels) > 0:
        ax1.legend()

    if tight_x_range:
        ax1.set_xlim(min_range, max_range)
    else:
        ax1.set_xlim(0, 100)
        xticks = np.arange(0, 110, 10)

        ax1.set_xticks(xticks)
        # sce clusters labels
        ax1.set_xticklabels(xticks)
    ax1.yaxis.set_tick_params(labelsize=ticks_label_size)
    ax1.xaxis.set_tick_params(labelsize=ticks_label_size)
    ax1.tick_params(axis='y', colors=axis_labels_color)
    ax1.tick_params(axis='x', colors=axis_labels_color)
    # TO remove the ticks but not the labels
    # ax1.xaxis.set_ticks_position('none')

    if ylabel is None:
        ax1.set_ylabel("Distribution (%)", fontsize=axis_label_font_size, labelpad=20, fontweight=fontweight,
                       fontfamily=fontfamily)
    else:
        ax1.set_ylabel(ylabel, fontsize=axis_label_font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
    ax1.set_xlabel(xlabel, fontsize=axis_label_font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)

    ax1.xaxis.label.set_color(axis_labels_color)
    ax1.yaxis.label.set_color(axis_labels_color)

    if ax_to_use is None:
        # padding between ticks label and  label axis
        # ax1.tick_params(axis='both', which='major', pad=15)
        fig.tight_layout()
        if save_figure and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        plt.close()


def plot_violin_distribution(distribution_data,
                             filename=None,
                             hue=None,
                             order=None,
                             hue_order=None,
                             scale='area',
                             scale_hue=True,
                             gridsize=100,
                             width=0.8,
                             inner=None,
                             split=False,
                             dodge=True,
                             linewidth=None,
                             specify_ins=False,
                             cell_type=None,
                             palette_ins=None,
                             scale_them_all=False,
                             violin_color="white",
                             violin_edgecolor="white",
                             background_color="black",
                             axis_labels_color="white",
                             axis_color="white",
                             axis_label_font_size=20,
                             ticks_label_size=14,
                             ticks_labels_color="white",
                             xlabel=None,
                             ylabel=None,
                             fontweight=None,
                             fontfamily=None,
                             size_fig=None,
                             dpi=100,
                             path_results=None,
                             save_figure=False,
                             save_formats="pdf",
                             with_timestamp_in_file_name=True,
                             ax_to_use=None,
                             max_value=None):
    distribution = np.array(distribution_data)
    ncells = len(distribution)

    if ax_to_use is None:
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=size_fig, dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)
    else:
        ax1 = ax_to_use

    if specify_ins is True:
        hue = "Cell Type"
        palette = palette_ins
        split = True
        order = ["Pyramidal", "Interneuron"]
    if specify_ins is False:
        hue = None
        palette = None
        split = False
        order = None

    df_subset = pd.DataFrame()
    df_subset['Distribution'] = distribution
    df_subset['Xlabel'] = xlabel
    df_subset['Cell Type'] = cell_type
    svm = sns.violinplot(data=df_subset,
                         x="Xlabel",
                         y="Distribution",
                         hue=hue,
                         order=None,
                         hue_order=order,
                         bw='scott',
                         cut=0,
                         scale='area',
                         scale_hue=True,
                         gridsize=100,
                         width=0.8,
                         inner=inner,
                         split=split,
                         dodge=True,
                         orient=None,
                         linewidth=None,
                         color=violin_color,
                         palette=palette,
                         saturation=0.75,
                         ax=ax1)

    if specify_ins is False:
        svm.collections[0].set_edgecolor(violin_edgecolor)

    svm.set_xticklabels('')
    svm.set_xlabel('')
    svm.set_ylabel('')

    scale_them_all = scale_them_all
    if scale_them_all is True:
        ax1.set_ylim([0, max_value])

    ax1.set_ylabel(ylabel, fontsize=axis_label_font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
    ax1.set_xlabel(xlabel, fontsize=axis_label_font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
    ax1.xaxis.label.set_color(axis_labels_color)
    ax1.yaxis.label.set_color(axis_labels_color)
    ax1.spines['left'].set_color(axis_color)
    ax1.spines['right'].set_color(background_color)
    ax1.spines['bottom'].set_color(background_color)
    ax1.spines['top'].set_color(background_color)
    ax1.yaxis.set_tick_params(labelsize=ticks_label_size)
    ax1.xaxis.set_tick_params(labelsize=ticks_label_size)
    ax1.tick_params(axis='y', colors=ticks_labels_color)
    ax1.tick_params(axis='x', colors=background_color)

    if ax_to_use is None:
        # padding between ticks label and  label axis
        # ax1.tick_params(axis='both', which='major', pad=15)
        fig.tight_layout()
        if save_figure and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        plt.close()


def plot_multiple_violin_distributions(distribution_data,
                                       filename=None,
                                       hue=None,
                                       order=None,
                                       hue_order=None,
                                       scale='area',
                                       scale_hue=True,
                                       gridsize=100,
                                       width=0.8,
                                       inner=None,
                                       split=False,
                                       dodge=True,
                                       linewidth=None,
                                       specify_ins=False,
                                       cell_type=None,
                                       palette_ins=None,
                                       scale_them_all=False,
                                       violin_color="white",
                                       violin_edgecolor="white",
                                       background_color="black",
                                       axis_labels_color="white",
                                       axis_color="white",
                                       axis_label_font_size=15,
                                       ticks_label_size=8,
                                       ticks_labels_color="white",
                                       xlabel=None,
                                       ylabel=None,
                                       fontweight=None,
                                       fontfamily=None,
                                       size_fig=None,
                                       dpi=100,
                                       path_results=None,
                                       save_figure=False,
                                       save_formats="pdf",
                                       with_timestamp_in_file_name=True):
    distribution_list = distribution_data
    n_sessions = len(distribution_list)
    cell_type_lists = cell_type
    id_list = xlabel
    n_violin_plots = len(distribution_list)
    print(f"Plotting {n_violin_plots} violin-plots ")
    n_plots = n_violin_plots
    ins_spec = np.zeros(len(distribution_list))
    if isinstance(specify_ins, list):
        for session in range(n_sessions):
            if specify_ins[session] is True:
                ins_spec[session] = 1

    max_values = []
    for distribution_index in range(n_plots):
        max_values.append(np.nanmax(distribution_list[distribution_index]))
    max_value = np.nanmax(max_values)

    if n_plots > 6:
        max_n_lines = 5
    else:
        max_n_lines = 2
    n_lines = n_plots if n_plots <= max_n_lines else max_n_lines
    n_col = math.ceil(n_plots / n_lines)
    print(f"n_lines {n_lines}, n_cols {n_col}")
    fig, axes = plt.subplots(nrows=n_lines, ncols=n_col,
                             gridspec_kw={'width_ratios': [1] * n_col, 'height_ratios': [1] * n_lines},
                             figsize=size_fig)
    fig.set_tight_layout({'rect': [0, 0, 1, 0.95], 'pad': 1.5, 'h_pad': 1.5})
    fig.patch.set_facecolor(background_color)

    if n_lines + n_col == 2:
        axes = [axes]
    else:
        axes = axes.flatten()

    for ax_index, ax in enumerate(axes):
        ax.set_facecolor(background_color)
        ax.spines['left'].set_color(background_color)
        ax.spines['right'].set_color(background_color)
        ax.spines['bottom'].set_color(background_color)
        ax.spines['top'].set_color(background_color)
        ax.tick_params(axis='y', colors=background_color)
        ax.tick_params(axis='x', colors=background_color)
        if ax_index >= n_violin_plots:
            continue
        if ins_spec[ax_index] == 1:
            specify_ins = True
        if ins_spec[ax_index] == 0:
            specify_ins = False

        distribution = distribution_list[ax_index]
        if cell_type is not None:
            cell_type = cell_type_lists[ax_index]

        xlabel = id_list[ax_index]
        print(f"Plotting {xlabel}: specify interneurons is {specify_ins}")
        plot_violin_distribution(distribution,
                                 filename=filename,
                                 hue=None,
                                 order=None,
                                 hue_order=None,
                                 scale='area',
                                 scale_hue=True,
                                 gridsize=100,
                                 width=0.8,
                                 inner=inner,
                                 split=False,
                                 dodge=True,
                                 linewidth=None,
                                 specify_ins=specify_ins,
                                 cell_type=cell_type,
                                 palette_ins=palette_ins,
                                 scale_them_all=scale_them_all,
                                 violin_color=violin_color,
                                 violin_edgecolor=violin_edgecolor,
                                 background_color=background_color,
                                 axis_labels_color=axis_labels_color,
                                 axis_color=axis_color,
                                 axis_label_font_size=axis_label_font_size,
                                 ticks_label_size=ticks_label_size,
                                 ticks_labels_color=ticks_labels_color,
                                 xlabel=xlabel,
                                 ylabel=ylabel,
                                 fontweight=fontweight,
                                 fontfamily=fontfamily,
                                 size_fig=None,
                                 dpi=dpi,
                                 path_results=None,
                                 save_figure=False,
                                 save_formats="pdf",
                                 with_timestamp_in_file_name=True,
                                 ax_to_use=ax,
                                 max_value=max_value)

    if save_figure and (path_results is not None):
        # transforming a string in a list
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        time_str = ""
        if with_timestamp_in_file_name:
            time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
        for save_format in save_formats:
            if not with_timestamp_in_file_name:
                fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())
            else:
                fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                            format=f"{save_format}",
                            facecolor=fig.get_facecolor())
    plt.close()


def plot_scatter_family(data_dict, colors_dict,
                        filename,
                        y_label,
                        label_to_legend=None,
                        marker_to_legend=None,
                        path_results=None, y_lim=None,
                        x_label=None,
                        x_ticks_labels=None,
                        x_ticks_pos=None,
                        y_ticks_labels=None,
                        y_ticks_pos=None,
                        y_log=False,
                        scatter_size=200,
                        scatter_alpha=1,
                        background_color="black",
                        lines_plot_values=None,
                        plots_linewidth=2,
                        link_scatter=False,
                        labels_color="white",
                        with_x_jitter=0.2,
                        with_y_jitter=None,
                        x_labels_rotation=None,
                        h_lines_y_values=None,
                        with_text=False,
                        default_marker='o',
                        text_size=5,
                        save_formats="pdf",
                        dpi=200,
                        cmap=None,
                        with_timestamp_in_file_name=True):
    """
    Plot family of scatters (same color and label) with possibly lines that are associated to it.
    :param data_dict: key is a label, value is a list of up to 4 (2 mandatory) list of int, of same size,
    first one are the x-value,
    second one is the y-values
    Third one is a text to write in the scatter, non mandatory
    Fourth one is the marker to display, could be absent, default_marker will be used
    Fifth one is the number of elements that allows to get this number (like number
    of sessions)
    :param colors_dict = key is a label, value is a color
    :param label_to_legend: (dict) if not None, key are label of data_dict, value is the label to be displayed as legend
    :param marker_to_legend: (dict) if not None, key are marker of data_dict, value is the label to be displayed as legend
    :param filename:
    :param lines_plot_values: (dict) same keys as data_dict, value is a list of list of 2 list of int or float,
    representing x & y value of plot to trace
    :param y_label:
    :param y_lim: tuple of int,
    :param link_scatter: draw a line between scatters
    :param save_formats:
    :param with_text: if True and data available in data_dict, then text is plot in the scatter
    :return:
    """
    fig, ax1 = plt.subplots(nrows=1, ncols=1,
                            gridspec_kw={'height_ratios': [1]},
                            figsize=(12, 12), dpi=dpi)

    ax1.set_facecolor(background_color)

    fig.patch.set_facecolor(background_color)

    # labels = []
    # data_list = []
    # scatter_text_list = []
    # medians_values = []
    min_x_value = 10000
    max_x_value = 0

    for label, data_to_scatters in data_dict.items():
        min_x_value = min(min_x_value, np.min(data_to_scatters[0]))
        max_x_value = max(max_x_value, np.max(data_to_scatters[0]))

        # Adding jitter
        if (with_x_jitter > 0) and (with_x_jitter < 1):
            x_pos = [x + ((np.random.random_sample() - 0.5) * with_x_jitter) for x in data_to_scatters[0]]
        else:
            x_pos = data_to_scatters[0]

        if with_y_jitter is not None:
            y_pos = [y + (((np.random.random_sample() - 0.5) * 2) * with_y_jitter) for y in data_to_scatters[1]]
        else:
            y_pos = data_to_scatters[1]

        colors_scatters = []
        while len(colors_scatters) < len(y_pos):
            colors_scatters.extend(colors_dict[label])

        label_legend = label_to_legend[label] if label_to_legend is not None else label
        if len(data_to_scatters) > 3:
            markers = data_to_scatters[3]
            for index in range(len(x_pos)):
                # if too slow, see to regroup by scatter value
                sc = ax1.scatter(x_pos[index], y_pos[index],
                                 color=colors_dict[label],
                                 alpha=scatter_alpha,
                                 marker=markers[index],
                                 edgecolors=labels_color,
                                 # label=label_legend,
                                 s=scatter_size, zorder=21)
                # , cmap=cmap
        else:
            sc = ax1.scatter(x_pos, y_pos,
                             color=colors_dict[label],
                             alpha=scatter_alpha,
                             marker=default_marker,
                             edgecolors=labels_color,
                             # label=label_legend,
                             s=scatter_size, zorder=21)
            # , cmap=cmap

        if with_text and len(data_to_scatters) > 2:
            # then the third dimension is a text to plot in the scatter
            for scatter_index in np.arange(len(data_to_scatters[2])):
                scatter_text = str(data_to_scatters[2][scatter_index])
                if len(scatter_text) > 3:
                    font_size = text_size - 2
                else:
                    font_size = text_size
                ax1.text(x=x_pos[scatter_index], y=y_pos[scatter_index],
                         s=scatter_text, color="black", zorder=50,
                         ha='center', va="center", fontsize=font_size, fontweight='bold')

        if link_scatter:
            ax1.plot(x_pos, y_pos, zorder=30, color=colors_dict[label],
                     linewidth=plots_linewidth)

        if lines_plot_values is not None:
            if label in lines_plot_values:
                for lines_coordinates in lines_plot_values[label]:
                    x_pos, y_pos = lines_coordinates
                    ax1.plot(x_pos, y_pos, zorder=35, color=colors_dict[label],
                             linewidth=plots_linewidth)

    if h_lines_y_values is not None:
        for y_value in h_lines_y_values:
            ax1.hlines(y_value, min_x_value,
                       max_x_value, color=labels_color, linewidth=0.5,
                       linestyles="dashed", zorder=25)

    ax1.set_ylabel(f"{y_label}", fontsize=30, labelpad=20)
    if y_lim is not None:
        ax1.set_ylim(y_lim[0], y_lim[1])
    if x_label is not None:
        ax1.set_xlabel(x_label, fontsize=30, labelpad=20)
    ax1.xaxis.label.set_color(labels_color)
    ax1.yaxis.label.set_color(labels_color)
    if y_log:
        ax1.set_yscale("log")

    legend_elements = []
    for label, color in colors_dict.items():
        if label_to_legend is None or label not in label_to_legend:
            continue
        label_legend = label_to_legend[label] if label_to_legend is not None else label
        legend_elements.append(Patch(facecolor=color,
                                     edgecolor='black', label=label_legend))
    if (marker_to_legend is not None) and (len(marker_to_legend) > 0):
        for marker, marker_legend in marker_to_legend.items():
            legend_elements.append(Line2D([0], [0], marker=marker, color="w", lw=0, label=marker_legend,
                                          markerfacecolor='black', markersize=12))
    ax1.legend(handles=legend_elements)

    ax1.yaxis.set_tick_params(labelsize=20)
    ax1.xaxis.set_tick_params(labelsize=15)
    ax1.tick_params(axis='y', colors=labels_color)
    ax1.tick_params(axis='x', colors=labels_color)

    # so colormap color is also updated
    params = {"text.color": labels_color,
              "xtick.color": labels_color,
              "ytick.color": labels_color}
    plt.rcParams.update(params)

    ax1.spines['right'].set_color(background_color)
    ax1.spines['top'].set_color(background_color)
    if x_ticks_pos is not None:
        ax1.set_xticks(x_ticks_pos)
    # removing the ticks but not the labels
    # ax1.xaxis.set_ticks_position('none')
    # sce clusters labels
    if x_ticks_labels is not None:
        ax1.set_xticklabels(x_ticks_labels)

    if y_ticks_pos is not None and y_ticks_labels is not None:
        # plt.yticks(y_ticks_pos, y_ticks_labels)
        ax1.set_yticks(y_ticks_pos)
    if y_ticks_labels is not None:
        ax1.set_yticklabels(y_ticks_labels)

    # if cmap is not None:
    # pcm = ax1.get_children()[2]
    # clb = plt.colorbar(sc, ax=ax1)
    # cmin=0
    # cmax=1
    # sc.set_clim([cmin, cmax])
    # cb = fig.colorbar(sc)
    # plt.colorbar(sc)
    # clb.ax.tick_params(color="white")
    # if x_labels_rotation is not None:
    #     for tick in ax1.get_xticklabels():
    #         tick.set_rotation(x_labels_rotation)

    # padding between ticks label and  label axis
    # ax1.tick_params(axis='both', which='major', pad=15)
    fig.tight_layout()
    # adjust the space between axis and the edge of the figure
    # https://matplotlib.org/faq/howto_faq.html#move-the-edge-of-an-axes-to-make-room-for-tick-labels
    # fig.subplots_adjust(left=0.2)

    if with_timestamp_in_file_name:
        time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

    if isinstance(save_formats, str):
        save_formats = [save_formats]

    for save_format in save_formats:
        fig.savefig(f'{path_results}/{filename}'
                    f'_{time_str}.{save_format}',
                    format=f"{save_format}",
                    facecolor=fig.get_facecolor())

    plt.close()


def plot_serie_of_values(results_path, time_x_values, y_values, color_plot, x_label=None, y_label=None,
                         color_ticks="white",
                         axes_label_color="white",
                         axes_border_color="white",
                         color_v_line="white", label_legend=None, line_width=2,
                         v_lines_coords=None,
                         vspan_color="gray", vspan_coords=None,
                         line_mode=True, background_color="black", ax_to_use=None,
                         figsize=(15, 10),
                         ticks_labels_size=5,
                         axis_label_size=30,
                         axis_label_pad=20,
                         legend_police_size=10,
                         ticks_length=6,
                         ticks_width=2,
                         top_border_visible=False,
                         right_border_visible=False,
                         bottom_border_visible=False,
                         left_border_visible=False,
                         y_lim_values=None,
                         file_name=None,
                         save_formats="pdf",
                         put_mean_line_on_plt=False,
                         threshold_line_y_value=None):
    """
    Plot a serie of value using lines or bars
    Args:
        results_path: (string) path of dir where to save the results
        time_x_values: 1d array containing the time from -n to +n corresponding to psth_values
        y_values: list of 1d array, from 1 to 3 1d array of the same length as time_x_values.
        First one represents the mean or median values, if 2 elements then the second represents the std, if
        3 elements then the 2nd and 3rd elements represents a low and high percentile (such as 25th and 75th percentile)
        color_plot: color of the plot
        x_label:
        y_label:
        color_ticks:
        axes_label_color:
        y_lim_values: (tuple of float), None or 2 values used to set the y_lim
        color_v_line: color of the line representing the "stim"
        v_lines_coords: (list flat) if not None, display v_lines at the x coords given in the list
        vspan_color: color of the vspan areas
        vspan_coords: if not None, list of tuple of float representing the beginning and end of a vertical span
        label_legend: None if no label, otherwise the label legend
        line_width:
        line_mode: (bool) if False, bar mode is activated
        background_color:
        ax_to_use: None if we plot a unique figure, file_name should not be None then, otherwise the ax
        in which to plot.
        figsize: tuple of int (width, height)
        ticks_labels_size: (int) size of the ticks label
        axis_label_size: (int) size of the axes label size
        axis_label_pad: (int) padding betwwen the axes and their label
        file_name:
        save_formats: string or list of string, like "pdf", "png"
        put_mean_line_on_plt: if True, means we use a trick to plot on the last "grid" so we collect
        all the plots in one place.
        threshold_line_y_value: float, if not None, an horizontal line is displayed representing for example a
        threshold value

    Returns:

    """
    y_max = 0
    y_min = 0
    if ax_to_use is None:
        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=figsize)
        fig.patch.set_facecolor(background_color)

        ax1.set_facecolor(background_color)
    else:
        ax1 = ax_to_use

    if line_mode:
        ax1.plot(time_x_values,
                 y_values[0], color=color_plot, lw=line_width, label=label_legend)
        if threshold_line_y_value is not None:
            ax1.hlines(threshold_line_y_value, np.min(time_x_values), np.max(time_x_values),
                       lw=1, linestyles="dashed", color="white", zorder=10)
        if put_mean_line_on_plt:
            plt.plot(time_x_values,
                     y_values[0], color=color_plot, lw=2)
        y_max = np.max((y_max, np.max(y_values[0])))
        y_min = np.min((y_min, np.min(y_values[0])))
        if len(y_values) == 2:
            ax1.fill_between(time_x_values, y_values[0] - y_values[1],
                             y_values[0] + y_values[1],
                             alpha=0.5, facecolor=color_plot)
            y_max = np.max((y_max, np.max(y_values[0] + y_values[1])))
            y_min = np.min((y_min, np.min(y_values[0] - y_values[1])))
        elif len(y_values) == 3:
            ax1.fill_between(time_x_values, y_values[1], y_values[2],
                             alpha=0.5, facecolor=color_plot)
            y_max = np.max((y_max, np.max(y_values[2])))
            y_min = np.min((y_min, np.min(y_values[1])))
    else:
        hist_color = color_plot
        edge_color = color_plot
        ax1.bar(time_x_values,
                y_values[0], color=hist_color, edgecolor=edge_color,
                label=label_legend)
        if threshold_line_y_value:
            ax1.hlines(threshold_line_y_value, np.min(time_x_values), np.max(time_x_values),
                       lw=1, linestyles="dashed", color="white", zorder=10)
        y_max = np.max((y_max, np.max(y_values[0])))
        y_min = np.min((y_min, np.min(y_values[0])))

    if vspan_coords:
        for vspan_coord in vspan_coords:
            ax1.axvspan(vspan_coord[0], vspan_coord[1], alpha=0.3, facecolor=vspan_color, zorder=2)

    if v_lines_coords:
        for v_line_coords in v_lines_coords:
            ax1.vlines(v_line_coords, y_min,
                       y_max, color=color_v_line, linewidth=2,
                       linestyles="dashed")

    if put_mean_line_on_plt and v_lines_coords:
        for v_line_coords in v_lines_coords:
            plt.vlines(v_line_coords, y_min,
                       y_max, color=color_v_line, linewidth=2,
                       linestyles="dashed")

    ax1.tick_params(axis='y', colors=color_ticks, labelsize=ticks_labels_size, length=ticks_length, width=ticks_width)
    ax1.tick_params(axis='x', colors=color_ticks, labelsize=ticks_labels_size, length=ticks_length, width=ticks_width)

    if label_legend is not None:
        ax1.legend(prop={'size': legend_police_size})

    if y_label is not None:
        ax1.set_ylabel(y_label, fontsize=axis_label_size, labelpad=axis_label_pad)
    if x_label is not None:
        ax1.set_xlabel(x_label, fontsize=axis_label_size, labelpad=axis_label_pad)
    if y_lim_values is not None:
        ax1.set_ylim(y_lim_values[0], y_lim_values[1])
    else:
        ax1.set_ylim(y_min, y_max + (y_max / 10))

    ax1.xaxis.label.set_color(axes_label_color)
    ax1.yaxis.label.set_color(axes_label_color)

    ax1.xaxis.set_tick_params(rotation=45)

    ax1.spines['top'].set_visible(top_border_visible)
    ax1.spines['right'].set_visible(right_border_visible)
    ax1.spines['bottom'].set_visible(bottom_border_visible)
    ax1.spines['left'].set_visible(left_border_visible)

    ax1.spines['bottom'].set_color(axes_border_color)
    ax1.spines['top'].set_color(axes_border_color)
    ax1.spines['right'].set_color(axes_border_color)
    ax1.spines['left'].set_color(axes_border_color)

    # xticks = np.arange(0, len(data_dict))
    # ax1.set_xticks(time_x_values)
    # # sce clusters labels
    # ax1.set_xticklabels(labels)

    if ax_to_use is None and (file_name is not None):
        if isinstance(save_formats, str):
            save_formats = [save_formats]
        for save_format in save_formats:
            fig.savefig(f'{results_path}/{file_name}.{save_format}',
                        format=f"{save_format}",
                        facecolor=fig.get_facecolor())
    if ax_to_use is None:
        plt.close()
