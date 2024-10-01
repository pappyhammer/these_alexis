import os
from sys import platform
from datetime import datetime
import numpy as np
import pandas as pd
import random
from plot_utils import plot_box_plots, plot_pie_chart, BREWER_COLORS
from asthma_entry import from_csv_to_asthma_entries
from utils import sort_two_list
from code_alexis import table_1_alexis


def count_boolean_attr_in_entries(entries, attr_name):
    """
    Return the number of entries at True, the number at False, and the number at None for a given attribute
    :param entries:
    :param attr_name:
    :return:
    """
    n_true = 0
    n_false = 0
    n_none = 0

    for entry in entries:
        if hasattr(entry, attr_name):
            value_attr = getattr(entry, attr_name)
            if value_attr:
                n_true += 1
            elif value_attr is None:
                n_none += 1
            else:
                n_false += 1
        else:
            print(f"Something wrong, no attribute {attr_name} found in entry")

    return n_true, n_false, n_none


def sandbox(path_results):
    print("Hello world")


def run_exemples(path_results, asthma_entries):
    save_formats = "png"

    ages_inf_6 = list()
    ages_sup_6 = list()
    for entry in asthma_entries:
        if entry.age_years_float < 6:
            ages_inf_6.append(entry.age_years_float)
        else:
            ages_sup_6.append(entry.age_years_float)

    data_dict = dict()
    data_dict["< 6 ans"] = ages_inf_6
    data_dict["> 6 ans"] = ages_sup_6

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

    attributes_for_pies = ["enfant_danger", "impuissant", "ressources_full_mode", "consult_med_dans_les_5_j",
                           "plan_action_maison", "plan_action_suivi"]

    for attr_name in attributes_for_pies:
        n_true, n_false, n_none = count_boolean_attr_in_entries(entries=asthma_entries, attr_name=attr_name)

        data_dict = dict()
        data_dict["Oui"] = n_true
        data_dict["Non"] = n_false

        background_color = "white"

        filename = attr_name + "_pie"
        label_data = attr_name
        plot_pie_chart(data_dict=data_dict, label_data=label_data,
                       path_results=path_results, filename=filename,
                       background_color=background_color,
                       color_discrete_map=None,
                       save_formats=save_formats)

    md_dict = dict()
    for entry in asthma_entries:
        if entry.md_in_charge not in md_dict:
            md_dict[entry.md_in_charge] = 1
        else:
            md_dict[entry.md_in_charge] += 1

    mds = list(md_dict.keys())
    n_entries_by_md = list(md_dict.values())
    n_entries_by_md, mds = sort_two_list(main_list=n_entries_by_md, second_list=mds, order="descending")
    top_to_display = min(5, len(md_dict))
    for index_to_display in range(top_to_display):
        print(f"Top {index_to_display+1}: {mds[index_to_display]} avec {n_entries_by_md[index_to_display]} questionnaires")


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
    path_data_alexis = "C:/Users/Utilisateur/Desktop/donnes_these"

    if platform == "win32":
        path_data = path_data_alexis
        database_csv_file = os.path.join(path_data,"recueil_alexis_auto_fill.csv")
    else:
        path_data = path_data_julien
        database_csv_file = os.path.join(path_data, "auto_fill", "recueil_alexis_auto_fill.csv")

    # print("hy world, this is Julien")

    asthma_entries = from_csv_to_asthma_entries(csv_file=database_csv_file)

    if False:
        run_sandbox = False

        if run_sandbox:
            sandbox(path_results=path_results)
        else:
            run_exemples(path_results=path_results, asthma_entries=asthma_entries)

    table_1_alexis(asthma_entries=asthma_entries, path_results=path_results)
    # create_table1(asthma_entries=asthma_entries, path_results=path_results)


def create_table1(asthma_entries, path_results):
    ages_inf_6=list()
    ages_sup_6=list()

    ages_dict = dict()
    ages_dict["Age < 6 ans"] = list()
    ages_dict["Age >= 6 ans"] = list()
    ages_dict["Ages"] = list()

    for entry in asthma_entries:
        ages_dict["Ages"].append(entry.age_years_float)
        if entry.age_years_float<6:
            ages_dict["Age < 6 ans"].append(entry.age_years_float)
        else:
            ages_dict["Age >= 6 ans"].append(entry.age_years_float)


    #all_ages = ages_inf_6+ages_sup_6
    #all_ages = [entry.age_years_float for entry in asthma_entries]

    simple_fct_dict = {"moyenne": np.mean, "std": np.std, "median": np.median, "min": np.min, "max": np.max}

    for label_ages, ages in ages_dict.items():
        print(f"- N {label_ages}: {len(ages)} passes")
        for fonction_name, fct in simple_fct_dict.items():
            result_fct = fct(ages)
            print(f"{fonction_name} {label_ages}: {result_fct:.2f}")

        perc_25 = np.percentile(ages, 25)
        perc_75 = np.percentile(ages, 75)
        print(f"Percentile 25: {perc_25:.2f}, 75: {perc_75:.2f}")
        #mean_ages = np.mean(ages)
        #print(f"moyenne {label_ages}: {mean_ages:.2f}")

        #median_age=np.median(ages)
        #print(f"median {label_ages}: {median_age:.2f}")
        print()



