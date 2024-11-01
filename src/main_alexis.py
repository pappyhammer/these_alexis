import os
from sys import platform
from datetime import datetime
import numpy as np
from scipy import stats
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
    top_to_display = min(5, len(md_dict))
    for index_to_display in range(top_to_display):
        print(
            f"Top {index_to_display + 1}: {mds[index_to_display]} avec {n_entries_by_md[index_to_display]} questionnaires")


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

    md_ranking(asthma_entries)

    entries_groups = dict()
    entries_groups["< 6 ans"] = list(filter(lambda e: e.age_years < 6, asthma_entries))
    entries_groups[">= 6 ans"] = list(filter(lambda e: e.age_years >= 6, asthma_entries))
    entries_groups["6 - 11 ans"] = list(filter(lambda e: 6 <= e.age_years < 12, asthma_entries))
    entries_groups["12 - 18 ans"] = list(filter(lambda e: 12 <= e.age_years < 18, asthma_entries))
    entries_groups["RAD"] = list(filter(lambda e: (not e.is_hospit_tradi) and (not e.is_hospit_rea), asthma_entries))
    entries_groups["Hospit tradi"] = list(filter(lambda e: e.is_hospit_tradi, asthma_entries))
    entries_groups["Hospit rea"] = list(filter(lambda e: e.is_hospit_rea, asthma_entries))
    entries_groups["Effectif total"] = asthma_entries

    # table_1_alexis(asthma_entries=asthma_entries, path_results=path_results)
    groups_to_compute_p = ["< 6 ans", ">= 6 ans"]
    create_table_1(entries_groups=entries_groups, path_results=path_results, all_group_key="Effectif total",
                   with_p_stat=False,
                   groups_to_compute_p=groups_to_compute_p)


def create_table_1(entries_groups, path_results, all_group_key="Tous", with_p_stat=True,
                   groups_to_compute_p=None):
    output_dict = dict()
    output_dict[""] = []

    # TODO: χ2 used for categorical variables and t test used for continuous variables.

    for key_group in entries_groups.keys():
        output_dict[key_group] = []

    # key is the line in output_dict to fill afterwards
    # value is the table with n lines and 2 columns
    chi_square_data_dict = dict()

    index_group = 0
    index_group_for_stat = 0

    for key_group, group_entries in entries_groups.items():
        # N
        if index_group == 0:
            output_dict[""].append("N")
        n_entries = len(group_entries)
        extra_str = ""
        if all_group_key is not None and key_group != all_group_key:
            perc_n = (n_entries / len(entries_groups[all_group_key])) * 100
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
        # allergies_classiques	allergies_autres	atcd_cortico_6_mois	atcd_rea	atcd_hospit
        bool_attr_to_name_dict = {"enfant_danger": "Senti enfant en danger ?",
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
                                  "atcd_hospit": "Antecedent hospit tradi"
                                  # "": "",
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

        index_group += 1
        if key_group in groups_to_compute_p:
            index_group_for_stat += 1

    if with_p_stat:
        output_dict["p"] = [""] * len(output_dict[""])
        for line_index, chi_square_data in chi_square_data_dict.items():
            res = stats.chi2_contingency(chi_square_data)
            output_dict["p"][line_index] = f"{res.pvalue:.4f}"

    df = pd.DataFrame(output_dict)
    export_file_name = os.path.join(path_results, "these_alexis_table_1.csv")
    df.to_csv(export_file_name, encoding="utf-8", index=False)


def create_table_2(path_result,asthma_entries):
    vento=list()
    nbserie=list()
    tpserie=list()
    nbbouf=list()
    cortico=list()
    samu=list()

    vento_dict["vento"]=dict()
    nbserie_dict["serie>2"]=dict()
    tpserie_dict["tpserie"]=dict()
    nbbouf_dict["bouf"]=dict()
    cortico_dict["cortico"]=dict()
    samu_dict["appel"]=dict()

    for entry in asthma_entries:
        vento_dict["vento"].append("ttt_vento_avant_urgences")
        samu_dict["appel"].append("appel_du_15")
        tpserir_dict["tpserie"].append("inf_20m_entre_series_vento","entre_20m_1h_entre_series_vento")
        if n_repet_series_vento>2:
            nbserie_dict["vento"].append("n_repet_series_vento")
            #manque l'adatation au poids pour cortico et samu
            #if (poids>20 and "n_bouffees_vento">=10):
            #nbbouf_dict[bouf].append("n_bouffees_vento")
            #if poids in range(18,19) and "n_bouffees_vento"=9:
            #if poids in range(16,17) and "n_bouffees_vento"=8:
            #if poids in range(14,15) and "n_bouffees_vento"=7:
            #if poids in range(12,13) and "n_bouffees_vento"=6:
            #if poids in range(10,11) and "n_bouffees_vento"=5:
            #if poids in range(8,9) and "n_bouffees_vento"=4:
            #if poids in range(7) and "n_bouffees_vento"=3:

    simple_fct_table_2 ={"vento","nbserie","tpserie","nbbouf", "cortico","samu"}
    for ttt_vento_avant_urgences,vento in vento_dict.item():
        print(f'-N{ttt_vento_avant_urgences}:{len(vento)}passes')
        print()



