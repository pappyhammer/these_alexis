import os
from sys import platform
from datetime import datetime
import numpy as np
from scipy import stats
import pandas as pd
import random
from plot_utils import plot_box_plots, plot_pie_chart, BREWER_COLORS, plot_scatter_family, \
    plot_group_bar_chart_from_entries
from asthma_entry import from_csv_to_asthma_entries
from utils import sort_two_list


# from code_alexis import table_1_alexis


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


def md_ranking(asthma_entries):
    md_dict = dict()
    for entry in asthma_entries:
        if entry.md_in_charge not in md_dict:
            md_dict[entry.md_in_charge] = 1
        else:
            md_dict[entry.md_in_charge] += 1

    mds = list(md_dict.keys())
    n_entries_by_md = list(md_dict.values())
    n_entries_by_md, mds = sort_two_list(main_list=n_entries_by_md, second_list=mds, order="descending")
    top_to_display = min(40, len(md_dict))
    for index_to_display in range(top_to_display):
        print(
            f"Top {index_to_display + 1}: {mds[index_to_display]} avec {n_entries_by_md[index_to_display]} questionnaires")


def plot_sao2_iao(all_entries, entries_groups_dict, path_results):
    box_plot_dict = dict()

    for key_group, entries in entries_groups_dict.items():
        values = [getattr(e, "sao2_iao") for e in entries]
        values = list(filter(lambda v: v is not None, values))
        box_plot_dict[key_group] = values

    with_box_plot = False
    if with_box_plot:
        filename = "sao2_iao_by_group"
        ordered_labels = list(box_plot_dict.keys())
        ordered_labels.sort()
        plot_box_plots(data_dict=box_plot_dict, filename=filename,
                       y_label="SaO2 (%)",
                       box_in_front=True,
                       ordered_labels=ordered_labels,
                       scatter_text_dict=None,
                       colors=BREWER_COLORS[:len(box_plot_dict)],
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
                       background_color="white",
                       link_medians=None,
                       link_means=None,
                       link_data_points=None,
                       color_link_medians="red",
                       color_link_data_point="red",
                       labels_color="black",
                       with_y_jitter=None,
                       x_labels_rotation=45,
                       fliers_symbol=None,
                       save_formats="png",
                       dpi=500,
                       xkcd_mode=False,
                       with_timestamp_in_file_name=True)

    data_dict = dict()
    colors_dict = dict()
    filename = "sao2_iao_n_salbu"
    y_label = "# salbu"
    key_labels = ["all"]
    colors_dict["all"] = "cornflowerblue"
    data_dict["all"] = [[], []]
    x_for_linear_regression = []
    y_for_linear_regression = []

    for entry in all_entries:
        if entry.sao2_iao is None:
            continue
        if entry.n_nebu_salbu is None:
            continue

        data_dict["all"][0].append(entry.sao2_iao)
        data_dict["all"][1].append(entry.n_nebu_salbu)
        x_for_linear_regression.append(entry.sao2_iao)
        y_for_linear_regression.append(entry.n_nebu_salbu)

    label_to_legend = None
    m, b, *_ = stats.linregress(x_for_linear_regression, y_for_linear_regression)
    print(f"Linear regression y = {m:.1f}x {b:+.1f}")
    plot_extra_lines_dict = dict()
    regression_line_dict = dict()
    plot_extra_lines_dict["regression_line"] = regression_line_dict
    regression_line_dict["x"] = [x for x in range(min(x_for_linear_regression), max(x_for_linear_regression) + 1)]
    regression_line_dict["y"] = [(m * x) + b for x in
                                 range(min(x_for_linear_regression), max(x_for_linear_regression) + 1)]
    regression_line_dict["legend"] = f'$y = {m:.1f}x {b:+.1f}$'
    regression_line_dict["zorder"] = 40
    regression_line_dict["color"] = "black"
    regression_line_dict["linewidth"] = 1
    regression_line_dict["linestyles"] = "dashed"

    plot_scatter_family(data_dict, colors_dict,
                        filename,
                        y_label,
                        label_to_legend=label_to_legend,
                        marker_to_legend=None,
                        path_results=path_results, y_lim=None,
                        x_label=None,
                        x_ticks_labels=None,
                        x_ticks_pos=None,
                        y_ticks_labels=None,
                        y_ticks_pos=None,
                        y_log=False,
                        scatter_size=150,
                        scatter_alpha=1,
                        background_color="white",
                        lines_plot_values=None,
                        plots_linewidth=2,
                        plot_extra_lines_dict=plot_extra_lines_dict,
                        link_scatter=False,
                        labels_color="black",
                        with_x_jitter=0.5,
                        with_y_jitter=0.5,
                        x_labels_rotation=None,
                        h_lines_y_values=None,
                        with_text=True,
                        default_marker='o',
                        text_size=5,
                        save_formats="png",
                        dpi=200,
                        cmap=None,
                        with_timestamp_in_file_name=True)


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
        database_csv_file = os.path.join(path_data, "recueil_alexis_auto_fill.csv")
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

    md_ranking(asthma_entries)

    all_group_key = "Effectif total"
    entries_groups = dict()
    entries_groups["< 6 ans"] = list(filter(lambda e: e.less_than_6_y, asthma_entries))
    entries_groups[">= 6 ans"] = list(filter(lambda e: not e.less_than_6_y, asthma_entries))
    entries_groups["6 - 11 ans"] = list(filter(lambda e: e.age_years is not None and 6 <= e.age_years < 12,
                                               asthma_entries))
    entries_groups["12 - 18 ans"] = list(filter(lambda e: e.age_years is not None and 12 <= e.age_years < 18,
                                                asthma_entries))
    entries_groups["RAD"] = list(filter(lambda e: (not e.is_hospit_tradi) and (not e.is_hospit_rea), asthma_entries))
    entries_groups["Hospit tradi"] = list(filter(lambda e: e.is_hospit_tradi, asthma_entries))
    entries_groups["Hospit réa"] = list(filter(lambda e: e.is_hospit_rea, asthma_entries))
    entries_groups["Ecole de l'asthme"] = list(filter(lambda e: e.ecole_asthme_connue_et_contact, asthma_entries))
    entries_groups["Pas d'école de l'asthme"] = list(filter(lambda e: not e.ecole_asthme_connue_et_contact,
                                                            asthma_entries))
    entries_groups["Score mauvais"] = list(filter(lambda e: e.score_quality is not None and e.score_quality <= 3,
                                                  asthma_entries))
    entries_groups["Score modéré"] = list(filter(lambda e: e.score_quality is not None and 4 <= e.score_quality <= 6,
                                                 asthma_entries))
    entries_groups["Score bon"] = list(filter(lambda e: e.score_quality is not None and 7 <= e.score_quality <= 8,
                                              asthma_entries))
    entries_groups["Score parfait"] = list(filter(lambda e: e.score_quality is not None and 9 <= e.score_quality <= 10,
                                                  asthma_entries))
    entries_groups["Bien contrôlé"] = list(filter(lambda e: e.well_controlled is not None and e.well_controlled,
                                                  asthma_entries))
    entries_groups["Partiellement contrôlé"] = list(filter(lambda e: e.partly_controlled is not None
                                                                     and e.partly_controlled, asthma_entries))
    entries_groups["Non contrôlé"] = list(filter(lambda e: e.uncontrolled is not None and e.uncontrolled,
                                                 asthma_entries))

    entries_groups["Avec EFR"] = list(filter(lambda e: e.efr_done is not None
                                                       and e.efr_done, asthma_entries))
    entries_groups["Sans EFR"] = list(filter(lambda e: e.efr_done is not None and not e.efr_done,
                                             asthma_entries))

    entries_groups["Aucun suivi"] = list(filter(is_aucun_suivi, asthma_entries))
    entries_groups["Pneumologue"] = list(filter(is_suivi_pneumo, asthma_entries))
    entries_groups["Pédiatre"] = list(filter(is_suivi_pediatre, asthma_entries))
    entries_groups["Allergologue"] = list(filter(is_suivi_allergo, asthma_entries))
    entries_groups["Généraliste"] = list(filter(is_suivi_generaliste, asthma_entries))

    entries_groups["Aucun ttt de fond"] = list(filter(lambda e: e.ttt_de_fond_aucun is not None and e.ttt_de_fond_aucun,
                                                      asthma_entries))
    entries_groups["Flixotide"] = list(filter(lambda e: e.ttt_de_fond_flixotide is not None and e.ttt_de_fond_flixotide,
                                              asthma_entries))
    entries_groups["Seretide"] = list(filter(lambda e: e.ttt_de_fond_seretide is not None and e.ttt_de_fond_seretide,
                                             asthma_entries))

    entries_groups[all_group_key] = asthma_entries

    ecole_asthme_labels = ["Ecole de l'asthme", "Pas d'école de l'asthme"]
    age_labels = ["< 6 ans", "6 - 11 ans", "12 - 18 ans"]
    orientation_labels = ["RAD", "Hospit tradi", "Hospit réa"]
    score_labels = ["Score mauvais", "Score modéré", "Score bon", "Score parfait"]
    control_labels = ["Bien contrôlé", "Partiellement contrôlé", "Non contrôlé"]
    suivi_labels = ["Aucun suivi", "Pneumologue", "Pédiatre", "Allergologue", "Généraliste"]
    ttt_fond_labels = ["Aucun ttt de fond", "Flixotide", "Seretide"]
    efr_labels = ["Avec EFR", "Sans EFR"]

    dpi = 700
    save_formats = "png"
    x_ticks_label_size = 25
    x_ticks_rotation_angle = 0
    without_count_in_y = False

    # table_1_alexis(asthma_entries=asthma_entries, path_results=path_results)
    groups_to_compute_p = ["< 6 ans", ">= 6 ans"]
    create_table_1(entries_groups_dict=entries_groups, path_results=path_results,
                   table_title="full",
                   all_group_key=all_group_key,
                   with_p_stat=False,
                   groups_to_compute_p=groups_to_compute_p)

    plot_sao2_iao(entries_groups_dict=entries_groups, path_results=path_results, all_entries=asthma_entries)

    bars_group_dict = {"ecole_asthme": ecole_asthme_labels,
                       "age": age_labels,
                       "orientation": orientation_labels,
                       "score": score_labels,
                       "controle": control_labels,
                       "suivi": suivi_labels,
                       "ttt_fond": ttt_fond_labels}

    for table_title, group_labels in bars_group_dict.items():
        bars_entries_groups = dict()
        for group_label in group_labels:
            bars_entries_groups[group_label] = entries_groups[group_label]
        bars_entries_groups[all_group_key] = entries_groups[all_group_key]
        create_table_1(entries_groups_dict=bars_entries_groups, path_results=path_results,
                       table_title=table_title,
                       all_group_key=all_group_key,
                       with_p_stat=False)

    # extra_filename = "full"
    # plot_score_bars(entries_groups=entries_groups, path_results=path_results, extra_filename=extra_filename,
    #                 all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)

    # score
    bars_group_dict = {"ecole_asthme": ecole_asthme_labels,
                       "age": age_labels,
                       "orientation": orientation_labels,
                       "controle": control_labels,
                       "suivi": suivi_labels,
                       "ttt_fond": ttt_fond_labels}
    for score_type in ["complexe"]:
        if score_type == "complexe":
            score_ranges = [(0, 3), (4, 6), (7, 8), (9, 10)]
            sub_score_labels = ["mauvais", "modéré", "bon", "parfait"]
        else:
            score_ranges = [(0, 6), (7, 10)]
            sub_score_labels = ["mauvais", "bon"]
        for extra_filename, group_labels in bars_group_dict.items():
            bars_entries_groups = dict()
            for group_label in group_labels:
                bars_entries_groups[group_label] = entries_groups[group_label]
            bars_entries_groups[all_group_key] = entries_groups[all_group_key]
            plot_score_bars(entries_groups=bars_entries_groups, path_results=path_results,
                            without_count_in_y=without_count_in_y,
                            x_ticks_label_size=x_ticks_label_size, x_ticks_rotation_angle=x_ticks_rotation_angle,
                            extra_filename=extra_filename + f"_score_{score_type}",
                            score_ranges=score_ranges, score_labels=sub_score_labels,
                            all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)
    # controle
    bars_group_dict = {"ecole_asthme": ecole_asthme_labels,
                       "age": age_labels,
                       "orientation": orientation_labels,
                       "score": score_labels,
                       "suivi": suivi_labels,
                       "ttt_fond": ttt_fond_labels}
    for extra_filename, group_labels in bars_group_dict.items():
        bars_entries_groups = dict()
        for group_label in group_labels:
            bars_entries_groups[group_label] = entries_groups[group_label]
        bars_entries_groups[all_group_key] = entries_groups[all_group_key]
        plot_control_bars(entries_groups=bars_entries_groups, path_results=path_results,
                          without_count_in_y=without_count_in_y,
                          x_ticks_label_size=x_ticks_label_size, x_ticks_rotation_angle=x_ticks_rotation_angle,
                          extra_filename=extra_filename,
                          control_labels=control_labels,
                          all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)
    # suivi
    bars_group_dict = {"ecole_asthme": ecole_asthme_labels,
                       "age": age_labels,
                       "orientation": orientation_labels,
                       "score": score_labels,
                       "controle": control_labels,
                       "efr": efr_labels,
                       "ttt_fond": ttt_fond_labels}
    for extra_filename, group_labels in bars_group_dict.items():
        bars_entries_groups = dict()
        for group_label in group_labels:
            bars_entries_groups[group_label] = entries_groups[group_label]
        bars_entries_groups[all_group_key] = entries_groups[all_group_key]
        plot_suivi_bars(entries_groups=bars_entries_groups, path_results=path_results,
                        without_count_in_y=without_count_in_y,
                        x_ticks_label_size=x_ticks_label_size, x_ticks_rotation_angle=x_ticks_rotation_angle,
                        extra_filename=extra_filename,
                        all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)

    # EFR
    bars_group_dict = {"suivi": suivi_labels}
    for extra_filename, group_labels in bars_group_dict.items():
        bars_entries_groups = dict()
        for group_label in group_labels:
            bars_entries_groups[group_label] = entries_groups[group_label]
        bars_entries_groups[all_group_key] = entries_groups[all_group_key]
        plot_efr_bars(entries_groups=bars_entries_groups, path_results=path_results,
                      without_count_in_y=without_count_in_y,
                      x_ticks_label_size=x_ticks_label_size, x_ticks_rotation_angle=x_ticks_rotation_angle,
                      extra_filename=extra_filename,
                      all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)

    # ttt de fond
    bars_group_dict = {"suivi": suivi_labels}
    sub_labels = ttt_fond_labels
    labels_to_fct_dict = {"Aucun ttt de fond": lambda e: e.ttt_de_fond_aucun is not None and e.ttt_de_fond_aucun,
                          "Flixotide": lambda e: e.ttt_de_fond_flixotide is not None and e.ttt_de_fond_flixotide,
                          "Seretide": lambda e: e.ttt_de_fond_seretide is not None and e.ttt_de_fond_seretide}
    plot_bars(entries_groups=bars_entries_groups, path_results=path_results,
              sub_labels=sub_labels, labels_to_fct_dict=labels_to_fct_dict,
              plot_name="ttt_fond",
              without_count_in_y=without_count_in_y,
              x_ticks_label_size=x_ticks_label_size, x_ticks_rotation_angle=x_ticks_rotation_angle,
              extra_filename=extra_filename,
              all_group_key=all_group_key, dpi=dpi, save_formats=save_formats)


def is_aucun_suivi(entry):
    if entry.suivi_medecin is False:
        return True
    return False


def is_suivi_pneumo(entry):
    if entry.suivi_medecin is False:
        return False
    if entry.suivi_pneumologue:
        return True
    return False


def is_suivi_pediatre(entry):
    if entry.suivi_medecin is False:
        return False
    if entry.suivi_pneumologue:
        return False
    if entry.suivi_pediatre:
        return True
    return False


def is_suivi_allergo(entry):
    if entry.suivi_medecin is False:
        return False
    if entry.suivi_pneumologue:
        return False
    if entry.suivi_pediatre:
        return False
    if entry.suivi_allergo:
        return True
    return False


def is_suivi_generaliste(entry):
    if entry.suivi_medecin is False:
        return False
    if entry.suivi_pneumologue:
        return False
    if entry.suivi_pediatre:
        return False
    if entry.suivi_allergo:
        return False
    if entry.suivi_med_traitant:
        return True

    return False


def create_table_1(entries_groups_dict, path_results, table_title, all_group_key="Tous", with_p_stat=True,
                   groups_to_compute_p=None):
    output_dict = dict()
    output_dict[""] = []

    # TODO: χ2 used for categorical variables and t test used for continuous variables.

    for key_group in entries_groups_dict.keys():
        output_dict[key_group] = []

    # key is the line in output_dict to fill afterwards
    # value is the table with n lines and 2 columns
    chi_square_data_dict = dict()

    index_group = 0
    index_group_for_stat = 0

    for key_group, group_entries in entries_groups_dict.items():
        # N
        if index_group == 0:
            output_dict[""].append("N")
        n_entries = len(group_entries)
        extra_str = ""
        if all_group_key is not None and key_group != all_group_key:
            perc_n = (n_entries / len(entries_groups_dict[all_group_key])) * 100
            extra_str = f" ({perc_n:.1f}%)"
        output_dict[key_group].append(f"{n_entries}{extra_str}")

        # unique
        if index_group == 0:
            output_dict[""].append("Unique")
        n_uniques_entries = len(set([e.ipp for e in group_entries]))
        # perc_n = (n_uniques_entries / n_entries) * 100
        # extra_str = f" ({perc_n:.1f}%)"
        extra_str = ""
        output_dict[key_group].append(f"{n_uniques_entries}{extra_str}")

        # age
        if index_group == 0:
            output_dict[""].append("Age (années)")

        ages = [e.age_years_float for e in group_entries]
        ages = list(filter(lambda v: v is not None, ages))
        median_age = np.median(ages)
        p_25 = np.percentile(ages, 25)
        p_75 = np.percentile(ages, 75)
        output_dict[key_group].append(f"{median_age:.1f} ({p_25:.1f} - {p_75:.1f})")

        # Gender
        if index_group == 0:
            output_dict[""].append("Fille %")
        genders = [e.gender for e in group_entries]
        n_female = genders.count("F")
        perc_female = (n_female / len(group_entries)) * 100
        output_dict[key_group].append(f"{n_female} ({perc_female:.1f} %)")
        if with_p_stat and key_group in groups_to_compute_p:
            line_index = len(output_dict[key_group]) - 1
            if line_index not in chi_square_data_dict:
                # cols represent the 2 groups
                chi_square_data_dict[line_index] = [[0, 0],
                                                    [0, 0]]
            chi_square_data_dict[line_index][0][index_group_for_stat] = n_female
            chi_square_data_dict[line_index][1][index_group_for_stat] = len(group_entries) - n_female

        # booleans
        # TODO: add atcd_rea ?
        bool_attr_to_name_dict = {"atcd_dechoc": "Atcd déchoc",
                                  "pec_dechoc": "Prise en charge au dechoc",
                                  "cortico_urgences": "Corticoides aux urgences",
                                  "is_hospit_tradi": "Hospit tradi",
                                  "is_hospit_rea": "Hospit réa"
                                  }

        for attr_name, label_data in bool_attr_to_name_dict.items():
            if index_group == 0:
                output_dict[""].append(label_data)

            n_values = len(list(filter(lambda e: getattr(e, attr_name),
                                       group_entries)))
            n_none_values = len(list(filter(lambda e: getattr(e, attr_name) is None,
                                            group_entries)))
            n_total = len(group_entries) - n_none_values
            if n_total == 0:
                output_dict[key_group].append("0 / 0")
            else:
                perc_value = (n_values / n_total) * 100

                if n_total != len(group_entries):
                    output_dict[key_group].append(f"{n_values} / {n_total} ({perc_value:.1f} %)")
                else:
                    output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # continuous values
        wait_time_attr_to_name_dict = {"n_passages_urgences": "N passages urgences depuis 2023",
                                       "n_passages_urgences_asthme": "N passages urgences depuis 2023 pour asthme",
                                       "sao2_iao": "SaO2",
                                       "n_nebu_salbu": "N nebu salbutamol",
                                       "duree_sejour_urgences": "Temps passe aux urgences (min)"
                                       }
        for attr_name, label_data in wait_time_attr_to_name_dict.items():
            if index_group == 0:
                output_dict[""].append(label_data)
            values = [getattr(e, attr_name) for e in group_entries]
            values = list(filter(lambda v: v is not None, values))
            if len(values) == 0:
                output_dict[key_group].append("")
                continue
            median_value = np.median(values)
            p_25 = np.percentile(values, 25)
            p_75 = np.percentile(values, 75)
            output_dict[key_group].append(f"{median_value:.1f} ({p_25:.1f} - {p_75:.1f})")

        # n_salbu <= 1
        if index_group == 0:
            output_dict[""].append("Aerosol salbu <= 1")
        values = [getattr(e, "n_nebu_salbu") for e in group_entries]
        # values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v is not None and v <= 1, values)))
        perc_value = (n_values / n_total) * 100
        output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # n_salbu 3
        if index_group == 0:
            output_dict[""].append("Aerosol salbu == 3")
        values = [getattr(e, "n_nebu_salbu") for e in group_entries]
        # values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v is not None and v == 3, values)))
        perc_value = (n_values / n_total) * 100
        output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # n_salbu 6
        if index_group == 0:
            output_dict[""].append("Aerosol salbu == 6")
        values = [getattr(e, "n_nebu_salbu") for e in group_entries]
        # values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v is not None and v == 6, values)))
        perc_value = (n_values / n_total) * 100
        output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # n_salbu > 6
        if index_group == 0:
            output_dict[""].append("Aerosol salbu > 6")
        values = [getattr(e, "n_nebu_salbu") for e in group_entries]
        # values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v is not None and v > 6, values)))
        perc_value = (n_values / n_total) * 100
        output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # with atrovent
        if index_group == 0:
            output_dict[""].append("Avec atrovent (>= 1)")
        values = [getattr(e, "n_nebu_atrovent") for e in group_entries]
        # values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v is not None and v >= 1, values)))
        perc_value = (n_values / n_total) * 100
        output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # booleans

        #
        bool_attr_to_name_dict = {"atrovent_in_first_round": "Atrovent dans 1ere serie",
                                  "enfant_danger": "Senti enfant en danger ?",
                                  "impuissant": "Sensation d'être impuissant",
                                  "ressources_full_mode": "Utilisation toutes les ressources thérapeutiques",
                                  "consult_med_dans_les_5_j": "Consult medecin 5 jours avant",
                                  "suivi_medecin": "Suivi medecin",
                                  "suivi_med_traitant": "Suivi medecin traitan",
                                  "suivi_pneumologue": "Suivi pneumologue",
                                  "suivi_pediatre": "Suivi pediatre",
                                  "suivi_allergo": "Suivi allergo",
                                  "suivi_autre": "Suivi autre",
                                  "last_consult_suivi_inf_6m": "Dernier suivi < 6 mois",
                                  "last_consult_suivi_6m_1a": "Dernier suivi entre 6 mois et 1 an",
                                  "last_consult_suivi_sup_1a": "Dernier suivi > 1 an",
                                  "efr_done": "A déjà eu une EFR ?",
                                  "pai_done": "PAI en place",
                                  "controle_symptomes": "A eu symptomes asthme > 1 j/semaine",
                                  "controle_limitation_activite": "Limitation activite",
                                  "controle_vento_plus_ou_1x_sem": "Vento plus d'une ou 2 fois par semaine",
                                  "controle_nuit": "Reveil la nuit a cause asthme",
                                  "allergies_classiques": "Allergies classiques",
                                  "atcd_cortico_6_mois": "A recu des corticoides dans les 6 mois precedent",
                                  "atcd_rea": "Antecedent rea",
                                  "atcd_hospit": "Antecedent hospit tradi",
                                  "ttt_de_fond_flixotide": "Ttt de fond Flixotide",
                                  "ttt_de_fond_seretide": "Ttt de fond Seretide",
                                  "ttt_de_fond_singulair": "Ttt de fond Singulair",
                                  "ttt_de_fond_ne_sais_pas": "Ttt de fond non connu",
                                  "ttt_de_fond_aucun": "Pas de ttt de fond",
                                  "ecole_asthme_connue_et_contact": "Ecole de l'asthme connue et consultee",
                                  "ecole_asthme_connue_sans_contact": "Ecole de l'asthme connue uniquement",
                                  "ecole_asthme_non_connue": "Ecole de l'asthme non connue",
                                  "chambre_inhalation": "Pense bien savoir utiliser la chambre d'inhalation",
                                  "calendrier_crise": "Tenue d'un calendrier de crise",
                                  "peack_flow": "Peack flow à la maison",
                                  "peack_flow_bien_utilise": "Pense bien savoir utiliser le peack flow",
                                  "plan_action_maison": "Plan d'action present au domicile",
                                  "plan_action_suivi": "Plan d'action suivi",
                                  "plan_action_des_urgences_si_present": "Plan d'action fourni par les urgences",
                                  "prescription_vento": "Vento ou prescription dispo",
                                  "ttt_vento_avant_urgences": "Vento donnee avant arrivee urgences",
                                  "ttt_cortico_avant_urgences": "Cortico donnes avant arrivee urgences",
                                  "aucun_ttt_avant_urgences": "Aucun ttt donne avant arrivee urgences",
                                  "correct_n_bouffee_vento": "Bon nombre de bouffees par rapport au poids",
                                  "inf_20m_entre_series_vento": "Intervalle prise vento < 20 min ",
                                  "entre_20m_1h_entre_series_vento": "Intervalle prise vento 20 min - 1h",
                                  "entre_1h_4h_entre_series_vento": "Intervalle prise vento 1h - 4h",
                                  "plus_4h_entre_series_vento": "Intervalle prise vento > 4h",
                                  "delai_urg_inf_2h": "Delai entre debut symptome et cs urgences < 2h",
                                  "delai_urg_2h_6h": "Delai entre debut symptome et cs urgences 2h - 6h",
                                  "delai_urg_6h_24h": "Delai entre debut symptome et cs urgences 6h - 24h",
                                  "delai_urg_sup_24h": "Delai entre debut symptome et cs urgences > 24h",
                                  "appel_du_15": "Appel du SAMU",
                                  "n_repet_series_vento_0": "0 serie de vento",
                                  "n_repet_series_vento_1": "1 serie de vento",
                                  "n_repet_series_vento_2": "2 serie de vento",
                                  "n_repet_series_vento_sup_3": ">= 3 serie de vento",
                                  "n_respi_chbre_inhalation_sup_10": "Au moins 10 respirations ou 10 sec dans chambre"
                                  # "": "",
                                  }

        # 	n_respi_chbre_inhalation

        for attr_name, label_data in bool_attr_to_name_dict.items():
            if index_group == 0:
                output_dict[""].append(label_data)

            n_values = len(list(filter(lambda e: getattr(e, attr_name),
                                       group_entries)))
            n_none_values = len(list(filter(lambda e: getattr(e, attr_name) is None,
                                            group_entries)))
            n_total = len(group_entries) - n_none_values
            if n_total == 0:
                output_dict[key_group].append("0 / 0")
            else:
                perc_value = (n_values / n_total) * 100
                output_dict[key_group].append(f"{n_values} / {n_total} ({perc_value:.1f} %)")
                # if n_total != len(group_entries):
                #     output_dict[key_group].append(f"{n_values} / {n_total} ({perc_value:.1f} %)")
                # else:
                #     output_dict[key_group].append(f"{n_values} ({perc_value:.1f} %)")

        # continuous values
        wait_time_attr_to_name_dict = {"age_premiere_ventoline": "Age premiere ventoline (mois)"
                                       }
        for attr_name, label_data in wait_time_attr_to_name_dict.items():
            if index_group == 0:
                output_dict[""].append(label_data)
            values = [getattr(e, attr_name) for e in group_entries]
            values = list(filter(lambda v: v is not None, values))
            if len(values) == 0:
                output_dict[key_group].append("")
                continue
            median_value = np.median(values)
            p_25 = np.percentile(values, 25)
            p_75 = np.percentile(values, 75)
            output_dict[key_group].append(f"{median_value:.1f} ({p_25:.1f} - {p_75:.1f})")

        # Dernière EFR depuis 2023
        if index_group == 0:
            output_dict[""].append("Dernière EFR depuis 2023")
        values = [getattr(e, "annee_derniere_efr") for e in group_entries]
        values = list(filter(lambda v: v is not None, values))
        n_total = len(values)
        n_values = len(list(filter(lambda v: v >= 2023, values)))
        if n_total > 0:
            perc_value = (n_values / n_total) * 100
            output_dict[key_group].append(f"{n_values} / {n_total} ({perc_value:.1f} %)")
        else:
            output_dict[key_group].append("0 / 0")

        score_ranges = [(0, 3), (4, 6), (7, 8), (9, 10)]
        score_labels = ["mauvais", "modéré", "bon", "parfait"]

        for score_range, score_label in zip(score_ranges, score_labels):

            if index_group == 0:
                output_dict[""].append(f"Score qualite {score_label} ({score_range[0]}-{score_range[1]})")

            n_total = 0
            n_values = 0
            for entry in group_entries:
                if entry.score_quality is None:
                    continue
                n_total += 1
                if score_range[0] <= entry.score_quality <= score_range[1]:
                    n_values += 1
            if n_total > 0:
                perc_value = (n_values / n_total) * 100
                output_dict[key_group].append(f"{n_values} / {n_total} ({perc_value:.1f} %)")
            else:
                output_dict[key_group].append("0 / 0")

        index_group += 1
        if groups_to_compute_p is not None:
            if key_group in groups_to_compute_p:
                index_group_for_stat += 1

    if with_p_stat:
        output_dict["p"] = [""] * len(output_dict[""])
        for line_index, chi_square_data in chi_square_data_dict.items():
            res = stats.chi2_contingency(chi_square_data)
            output_dict["p"][line_index] = f"{res.pvalue:.4f}"

    df = pd.DataFrame(output_dict)
    export_file_name = os.path.join(path_results, f"these_alexis_table_{table_title}.csv")
    df.to_csv(export_file_name, encoding="utf-8", index=False)


def plot_score_bars(entries_groups, path_results, score_ranges, score_labels,
                    x_ticks_label_size, x_ticks_rotation_angle, extra_filename="",
                    all_group_key="Tous", dpi=700, save_formats="png", exclude_group_all=True,
                    without_count_in_y=True):
    for mode_tous in [True, False]:
        if exclude_group_all and mode_tous:
            continue
        entries_to_plot = list()
        for group_label, asthma_entries in entries_groups.items():
            if (not mode_tous) and group_label == all_group_key:
                continue

            entries_to_analyse = list(filter(lambda e: e.score_quality is not None, asthma_entries))

            for asthma_entry in entries_to_analyse:
                final_score_label = None
                for score_range, score_label in zip(score_ranges, score_labels):
                    if score_range[0] <= asthma_entry.score_quality <= score_range[1]:
                        final_score_label = score_label
                        break
                entry_as_dict = {"score": final_score_label, "cohort_group": group_label}
                entries_to_plot.append(entry_as_dict)

        for mode_y in ["perc", "count"]:
            if without_count_in_y and mode_y == "count":
                continue
            filename = f"asthma_score_bars_{extra_filename}_{mode_y}"
            if mode_tous:
                filename = f"asthma_score_bars_{extra_filename}_{mode_y}_avec_tous"
            fct_by_level = [lambda e: e["cohort_group"], lambda e: e["score"]]
            percentage_in_y = mode_y == "perc"
            with_text = True
            text_with_percentage = True
            if mode_y == "perc":
                y_label = "% patients"
            else:
                y_label = "# patients"
            # might bug if the names change
            sub_labels = score_labels
            main_labels = list(entries_groups.keys())
            if not mode_tous:
                main_labels = list(filter(lambda label: label != all_group_key, main_labels))
            plot_group_bar_chart_from_entries(entries=entries_to_plot, fct_by_level=fct_by_level,
                                              filename=filename,
                                              y_label=y_label,
                                              with_text=with_text,
                                              text_with_percentage=text_with_percentage,
                                              main_labels=main_labels,
                                              sub_labels=sub_labels,
                                              background_color="white",
                                              labels_color="black",
                                              figsize=(18, 12),
                                              x_ticks_label_size=x_ticks_label_size,
                                              x_ticks_rotation_angle=x_ticks_rotation_angle,
                                              percentage_in_y=percentage_in_y,
                                              path_results=path_results,
                                              save_formats=save_formats, dpi=dpi)


def plot_control_bars(entries_groups, path_results,
                      x_ticks_label_size, x_ticks_rotation_angle,
                      control_labels,
                      extra_filename="",
                      all_group_key="Tous", dpi=700, save_formats="png", exclude_group_all=True,
                      without_count_in_y=True):
    for mode_tous in [True, False]:
        if exclude_group_all and mode_tous:
            continue
        entries_to_plot = list()
        for group_label, asthma_entries in entries_groups.items():
            if (not mode_tous) and group_label == all_group_key:
                continue

            for asthma_entry in asthma_entries:
                if asthma_entry.well_controlled is None:
                    continue
                if asthma_entry.well_controlled:
                    final_control_label = "Bien contrôlé"
                elif asthma_entry.partly_controlled:
                    final_control_label = "Partiellement contrôlé"
                else:
                    final_control_label = "Non contrôlé"

                entry_as_dict = {"control": final_control_label, "cohort_group": group_label}
                entries_to_plot.append(entry_as_dict)

        for mode_y in ["perc", "count"]:
            if without_count_in_y and mode_y == "count":
                continue
            filename = f"asthma_control_bars_{extra_filename}_{mode_y}"
            if mode_tous:
                filename = f"asthma_control_bars_{extra_filename}_{mode_y}_avec_tous"
            fct_by_level = [lambda e: e["cohort_group"], lambda e: e["control"]]
            percentage_in_y = mode_y == "perc"
            with_text = True
            text_with_percentage = True
            if mode_y == "perc":
                y_label = "% patients"
            else:
                y_label = "# patients"
            # might bug if the names change
            sub_labels = control_labels
            main_labels = list(entries_groups.keys())
            if not mode_tous:
                main_labels = list(filter(lambda label: label != all_group_key, main_labels))
            plot_group_bar_chart_from_entries(entries=entries_to_plot, fct_by_level=fct_by_level,
                                              filename=filename,
                                              y_label=y_label,
                                              with_text=with_text,
                                              text_with_percentage=text_with_percentage,
                                              main_labels=main_labels,
                                              sub_labels=sub_labels,
                                              background_color="white",
                                              labels_color="black",
                                              figsize=(18, 12),
                                              x_ticks_label_size=x_ticks_label_size,
                                              x_ticks_rotation_angle=x_ticks_rotation_angle,
                                              percentage_in_y=percentage_in_y,
                                              path_results=path_results,
                                              save_formats=save_formats, dpi=dpi)


def plot_suivi_bars(entries_groups, path_results,
                    x_ticks_label_size, x_ticks_rotation_angle,
                    extra_filename="",
                    all_group_key="Tous", dpi=700, save_formats="png", exclude_group_all=True,
                    without_count_in_y=True):
    for mode_tous in [True, False]:
        if exclude_group_all and mode_tous:
            continue
        entries_to_plot = list()
        for group_label, asthma_entries in entries_groups.items():
            if (not mode_tous) and group_label == all_group_key:
                continue

            for asthma_entry in asthma_entries:
                if asthma_entry.suivi_medecin is None:
                    continue
                if asthma_entry.suivi_medecin is False:
                    suivi_label = "Aucun suivi"
                elif asthma_entry.suivi_pneumologue:
                    suivi_label = "Pneumologue"
                elif asthma_entry.suivi_pediatre:
                    suivi_label = "Pédiatre"
                elif asthma_entry.suivi_allergo:
                    suivi_label = "Allergologue"
                elif asthma_entry.suivi_med_traitant:
                    suivi_label = "Généraliste"
                # elif asthma_entry.suivi_autre:
                #     suivi_label = "Suivi autre"
                else:
                    continue

                entry_as_dict = {"suivi": suivi_label, "cohort_group": group_label}
                entries_to_plot.append(entry_as_dict)

        for mode_y in ["perc", "count"]:
            if without_count_in_y and mode_y == "count":
                continue
            filename = f"asthma_suivi_bars_{extra_filename}_{mode_y}"
            if mode_tous:
                filename = f"asthma_suivi_bars_{extra_filename}_{mode_y}_avec_tous"
            fct_by_level = [lambda e: e["cohort_group"], lambda e: e["suivi"]]
            percentage_in_y = mode_y == "perc"
            with_text = True
            text_with_percentage = True
            if mode_y == "perc":
                y_label = "% patients"
            else:
                y_label = "# patients"
            # might bug if the names change
            sub_labels = ["Aucun suivi", "Généraliste", "Pneumologue",
                          "Pédiatre", "Allergologue"]
            main_labels = list(entries_groups.keys())
            if not mode_tous:
                main_labels = list(filter(lambda label: label != all_group_key, main_labels))
            plot_group_bar_chart_from_entries(entries=entries_to_plot, fct_by_level=fct_by_level,
                                              filename=filename,
                                              y_label=y_label,
                                              with_text=with_text,
                                              text_with_percentage=text_with_percentage,
                                              main_labels=main_labels,
                                              sub_labels=sub_labels,
                                              background_color="white",
                                              labels_color="black",
                                              figsize=(18, 12),
                                              x_ticks_label_size=x_ticks_label_size,
                                              x_ticks_rotation_angle=x_ticks_rotation_angle,
                                              percentage_in_y=percentage_in_y,
                                              path_results=path_results,
                                              save_formats=save_formats, dpi=dpi)


def plot_efr_bars(entries_groups, path_results,
                  x_ticks_label_size, x_ticks_rotation_angle,
                  extra_filename="",
                  all_group_key="Tous", dpi=700, save_formats="png", exclude_group_all=True,
                  without_count_in_y=True):
    for mode_tous in [True, False]:
        if exclude_group_all and mode_tous:
            continue
        entries_to_plot = list()
        for group_label, asthma_entries in entries_groups.items():
            if (not mode_tous) and group_label == all_group_key:
                continue

            for asthma_entry in asthma_entries:
                if asthma_entry.efr_done is None:
                    continue
                if asthma_entry.efr_done:
                    efr_label = "Avec EFR"
                elif not asthma_entry.efr_done:
                    efr_label = "Sans EFR"
                else:
                    continue

                entry_as_dict = {"efr": efr_label, "cohort_group": group_label}
                entries_to_plot.append(entry_as_dict)

        for mode_y in ["perc", "count"]:
            if without_count_in_y and mode_y == "count":
                continue
            filename = f"asthma_efr_bars_{extra_filename}_{mode_y}"
            if mode_tous:
                filename = f"asthma_efr_bars_{extra_filename}_{mode_y}_avec_tous"
            fct_by_level = [lambda e: e["cohort_group"], lambda e: e["efr"]]
            percentage_in_y = mode_y == "perc"
            with_text = True
            text_with_percentage = True
            if mode_y == "perc":
                y_label = "% patients"
            else:
                y_label = "# patients"
            # might bug if the names change
            sub_labels = ["Avec EFR", "Sans EFR"]
            main_labels = list(entries_groups.keys())
            if not mode_tous:
                main_labels = list(filter(lambda label: label != all_group_key, main_labels))
            plot_group_bar_chart_from_entries(entries=entries_to_plot, fct_by_level=fct_by_level,
                                              filename=filename,
                                              y_label=y_label,
                                              with_text=with_text,
                                              text_with_percentage=text_with_percentage,
                                              main_labels=main_labels,
                                              sub_labels=sub_labels,
                                              background_color="white",
                                              labels_color="black",
                                              figsize=(18, 12),
                                              x_ticks_label_size=x_ticks_label_size,
                                              x_ticks_rotation_angle=x_ticks_rotation_angle,
                                              percentage_in_y=percentage_in_y,
                                              path_results=path_results,
                                              save_formats=save_formats, dpi=dpi)


def plot_bars(entries_groups, path_results,
              sub_labels, labels_to_fct_dict,
              plot_name,
              x_ticks_label_size, x_ticks_rotation_angle,
              extra_filename="",
              all_group_key="Tous", dpi=700, save_formats="png", exclude_group_all=True,
              without_count_in_y=True):
    """

    :param entries_groups:
    :param path_results:
    :param sub_labels: list of str
    :param labels_to_fct_dict: key is a sub label, fct takes an entry return True if the entry match the label
    :param plot_name: name of the plot used for file_name
    :param x_ticks_label_size:
    :param x_ticks_rotation_angle:
    :param extra_filename:
    :param all_group_key:
    :param dpi:
    :param save_formats:
    :param exclude_group_all:
    :param without_count_in_y:
    :return:
    """
    for mode_tous in [True, False]:
        if exclude_group_all and mode_tous:
            continue
        entries_to_plot = list()
        for group_label, asthma_entries in entries_groups.items():
            if (not mode_tous) and group_label == all_group_key:
                continue

            for asthma_entry in asthma_entries:
                label_to_use = None

                for label, fct_to_use in labels_to_fct_dict.items():
                    if fct_to_use(asthma_entry):
                        label_to_use = label
                        break

                if label_to_use is None:
                    continue

                entry_as_dict = {plot_name: label_to_use, "cohort_group": group_label}
                entries_to_plot.append(entry_as_dict)

        for mode_y in ["perc", "count"]:
            if without_count_in_y and mode_y == "count":
                continue
            filename = f"asthma_{plot_name}_bars_{extra_filename}_{mode_y}"
            if mode_tous:
                filename = f"asthma_{plot_name}_bars_{extra_filename}_{mode_y}_avec_tous"
            fct_by_level = [lambda e: e["cohort_group"], lambda e: e[plot_name]]
            percentage_in_y = mode_y == "perc"
            with_text = True
            text_with_percentage = True
            if mode_y == "perc":
                y_label = "% patients"
            else:
                y_label = "# patients"
            # might bug if the names change
            main_labels = list(entries_groups.keys())
            if not mode_tous:
                main_labels = list(filter(lambda label: label != all_group_key, main_labels))
            plot_group_bar_chart_from_entries(entries=entries_to_plot, fct_by_level=fct_by_level,
                                              filename=filename,
                                              y_label=y_label,
                                              with_text=with_text,
                                              text_with_percentage=text_with_percentage,
                                              main_labels=main_labels,
                                              sub_labels=sub_labels,
                                              background_color="white",
                                              labels_color="black",
                                              figsize=(18, 12),
                                              x_ticks_label_size=x_ticks_label_size,
                                              x_ticks_rotation_angle=x_ticks_rotation_angle,
                                              percentage_in_y=percentage_in_y,
                                              path_results=path_results,
                                              save_formats=save_formats, dpi=dpi)


def create_table_2(path_result, asthma_entries):
    vento = list()
    nbserie = list()
    tpserie = list()
    nbbouf = list()
    cortico = list()
    samu = list()

    vento_dict["vento"] = dict()
    nbserie_dict["serie>2"] = dict()
    tpserie_dict["tpserie"] = dict()
    nbbouf_dict["bouf"] = dict()
    cortico_dict["cortico"] = dict()
    samu_dict["appel"] = dict()

    for entry in asthma_entries:
        vento_dict["vento"].append("ttt_vento_avant_urgences")
        samu_dict["appel"].append("appel_du_15")
        tpserir_dict["tpserie"].append("inf_20m_entre_series_vento", "entre_20m_1h_entre_series_vento")
        if n_repet_series_vento > 2:
            nbserie_dict["vento"].append("n_repet_series_vento")
            # manque l'adatation au poids pour cortico et samu
            # if (poids>20 and "n_bouffees_vento">=10):
            # nbbouf_dict[bouf].append("n_bouffees_vento")
            # if poids in range(18,19) and "n_bouffees_vento"=9:
            # if poids in range(16,17) and "n_bouffees_vento"=8:
            # if poids in range(14,15) and "n_bouffees_vento"=7:
            # if poids in range(12,13) and "n_bouffees_vento"=6:
            # if poids in range(10,11) and "n_bouffees_vento"=5:
            # if poids in range(8,9) and "n_bouffees_vento"=4:
            # if poids in range(7) and "n_bouffees_vento"=3:

    simple_fct_table_2 = {"vento", "nbserie", "tpserie", "nbbouf", "cortico", "samu"}
    for ttt_vento_avant_urgences, vento in vento_dict.item():
        print(f'-N{ttt_vento_avant_urgences}:{len(vento)}passes')
        print()
