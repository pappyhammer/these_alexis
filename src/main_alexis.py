import os
from sys import platform
from datetime import datetime
import numpy as np
import random
from plot_utils import plot_box_plots, plot_pie_chart, BREWER_COLORS
from asthma_entry import AsthmaEntry

def main():
    path_results_alexis = "C:/Users/Utilisateur/Desktop/figures_code"
    path_results_julien = "/Users/pappyhammer/Documents/academique/python_code_output/urg_ped"

    if platform == "win32":
        path_results = path_results_alexis
    else:
        path_results = path_results_julien

    time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
    path_results = os.path.join(path_results, time_str)
    os.mkdir(path_results)

    path_data_julien = "/Users/pappyhammer/Documents/academique/python_code_output/alexis"
    path_data_alexis = ""

    if platform == "win32":
        path_data = path_data_alexis
    else:
        path_data = path_data_julien

    print("hy world")

    save_formats = "png"

    test_list_1 = [random.randint(0, 15) for i in range(100)]
    test_list_2 = [random.randint(0, 15) for i in range(100)]

    data_dict = dict()
    data_dict["Age 1"] = test_list_1
    data_dict["Age 2"] = test_list_2

    colors = BREWER_COLORS

    filename = "box_plot_age"

    plot_box_plots(data_dict=data_dict, filename=filename,
                   y_label="Age (années)",
                   box_in_front=True,
                   ordered_labels=list(data_dict.keys()),
                   scatter_text_dict=None,
                   colors=colors,
                   path_results=path_results, y_lim=None,
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
                   link_medians=None,
                   link_means=None,
                   link_data_points=None,
                   color_link_medians="red",
                   color_link_data_point="red",
                   labels_color="white",
                   with_y_jitter=None,
                   x_labels_rotation=45,
                   fliers_symbol=None,
                   save_formats=save_formats,
                   dpi=500,
                   xkcd_mode=False,
                   with_timestamp_in_file_name=True)

    data_dict = dict()
    data_dict["Plan d'action respecté"] = 25
    data_dict["Plan d'action non respecté"] = 92

    background_color = "white"

    filename = "plan_action_pie"
    label_data = "plan_action"
    plot_pie_chart(data_dict=data_dict, label_data=label_data,
                   path_results=path_results, filename=filename,
                   background_color=background_color,
                   color_discrete_map=None,
                   save_formats=save_formats)


