from abc import ABC, abstractmethod
import pandas as pd
from unidecode import unidecode
from date_utils import duration_bw_dates
from file_utils import from_csv_to_df


class AutoEntry(ABC):

    def __init__(self, auto_dict, bool_as_int=False):
        pass
        self.auto_dict = auto_dict
        # if set to True, then True will be represented by a 1, and False by a 0
        self.bool_as_int = bool_as_int
        self.entry_id = None
        self.entry = None

    def set_str_attr(self, attr_name):
        if attr_name in self.auto_dict:
            attr_value = self.auto_dict[attr_name]
            setattr(self, attr_name, attr_value)
        else:
            attr_value = getattr(self, attr_name)

        if pd.isna(attr_value):
            setattr(self, attr_name, None)
            return
        setattr(self, attr_name, str(attr_value))

    def set_float_attr(self, attr_name):
        if attr_name in self.auto_dict:
            attr_value = self.auto_dict[attr_name]
            setattr(self, attr_name, attr_value)
        else:
            attr_value = getattr(self, attr_name)

        if pd.isna(attr_value):
            setattr(self, attr_name, None)
            return
        elif isinstance(attr_value, float) or isinstance(attr_value, int) or \
                (isinstance(attr_value, str) and attr_value.isnumeric()):
            setattr(self, attr_name, float(attr_value))
            return
        # all other cases are set to None
        setattr(self, attr_name, None)

    def set_int_attr(self, attr_name):
        if attr_name in self.auto_dict:
            attr_value = self.auto_dict[attr_name]
            setattr(self, attr_name, attr_value)
        else:
            attr_value = getattr(self, attr_name)

        if pd.isna(attr_value):
            setattr(self, attr_name, None)
            return
        elif isinstance(attr_value, int) or (isinstance(attr_value, str) and attr_value.isdigit()):
            setattr(self, attr_name, int(attr_value))
            return
        try:
            int_value = int(attr_value)
            setattr(self, attr_name, int_value)
            return
        except ValueError:
            pass
        # all other cases are set to None
        setattr(self, attr_name, None)

    def set_bool_attr(self, attr_name, ignore_auto_dict=False):
        if not ignore_auto_dict and attr_name in self.auto_dict:
            attr_value = self.auto_dict[attr_name]
            setattr(self, attr_name, attr_value)
        else:
            attr_value = getattr(self, attr_name)
        if pd.isna(attr_value):
            setattr(self, attr_name, None)
            return
        elif not isinstance(attr_value, bool):
            if isinstance(attr_value, str):
                if attr_value.lower().strip() == "non":
                    if self.bool_as_int:
                        setattr(self, attr_name, 0)
                    else:
                        setattr(self, attr_name, False)
                    return
                elif attr_value.lower().strip() == "oui":
                    if self.bool_as_int:
                        setattr(self, attr_name, 1)
                    else:
                        setattr(self, attr_name, True)
                    return
                elif attr_value.lower().strip() == "true":
                    if self.bool_as_int:
                        setattr(self, attr_name, 1)
                    else:
                        setattr(self, attr_name, True)
                    return
                elif attr_value.lower().strip() == "false":
                    if self.bool_as_int:
                        setattr(self, attr_name, 0)
                    else:
                        setattr(self, attr_name, False)
                    return
            elif isinstance(attr_value, int):
                if attr_value == 0:
                    if self.bool_as_int:
                        setattr(self, attr_name, 0)
                    else:
                        setattr(self, attr_name, False)
                    return
                else:
                    if self.bool_as_int:
                        setattr(self, attr_name, 1)
                    else:
                        setattr(self, attr_name, True)
                    return

        else:
            if self.bool_as_int:
                if attr_value:
                    setattr(self, attr_name, 1)
                else:
                    setattr(self, attr_name, 0)
            else:
                # means it's already a boolean and we are ok with that
                pass
            return
        # all other cases are set to None
        setattr(self, attr_name, None)

    def __hash__(self):
        return hash(self.entry_id)

    def __eq__(self, other):
        if not isinstance(other, AutoEntry):
            return False
        return self.entry_id == other.entry_id

    def set_ttt_attribute(self, attr_name, keywords, verbose=True, delay_attr=None):
        """
        Set a field corresponding to a treatment prescribed by searching it
        in the prescribed ttt
        :param attr_name:
        :param keywords:
        :param verbose:
        :param delay_attr: str attribute name in Entry, if not None, set the attr to the delay between arrival
        and the time of done date
        :return:
        """
        if not hasattr(self, 'entry'):
            return

        if self.entry is None:
            return

        if getattr(self, attr_name) is not None:
            return

        # prescription in urg and zhcd
        ttt_received_dicts = [self.entry.ttt_received_dict]
        if self.entry.zhcd_entry is not None:
            ttt_received_dicts.append(self.entry.zhcd_entry.ttt_received_dict)

        break_it = False
        for ttt_received_dict in ttt_received_dicts:
            if len(ttt_received_dict) > 0:
                for key_ttt, value_ttt in ttt_received_dict.items():
                    # key_ttt (prescription_date, md_name, prescription)
                    # value is a dict with key "voie" and la voie used, and "date" with value a list
                    # of tuple (due_date, done_date)
                    prescription_date, md_name, prescription = key_ttt
                    for keyword in keywords:
                        if keyword in unidecode(prescription).lower():
                            setattr(self, attr_name, True)
                            if delay_attr is not None:
                                list_dates = value_ttt["date"]
                                if len(list_dates) > 0:
                                    # we take the first one prescribed
                                    done_date = list_dates[0][1]
                                    hours, hours_float, minutes = duration_bw_dates(later_date=done_date,
                                                                                    early_date=self.entry.arrival_date)
                                    setattr(self, delay_attr, minutes)
                            if verbose:
                                print(f"- {self.ipp} with {attr_name}: {prescription}")
                            break_it = True
                            break
                    if break_it:
                        break
                if break_it:
                    break

        if getattr(self, attr_name) is None:
            setattr(self, attr_name, False)

    def set_field_from_pandas(self, pd_series, pandas_field_name, field_name=None, if_not_nan=True,
                              verbose=False, eq_none=None):
        """
        Set a field value
        :param pd_series:
        :param pandas_field_name:
        :param field_name: if None so the same as pandas_field_name
        :param if_not_nan: if True we don't change the field value if the panda field is nan
        :param verbose:
        :param eq_none: (str or list of str) if value of the field is this value, then it's equivalen to None and we replace
        the value by None
        :return:
        """
        if field_name is None:
            field_name = pandas_field_name

        if isinstance(eq_none, str):
            eq_none = [eq_none]

        if pandas_field_name in pd_series:
            pandas_value = pd_series[pandas_field_name]
            if pd.isna(pandas_value) and if_not_nan:
                return
            value_before = getattr(self, field_name)
            if value_before is not None:
                # we keep the longer version
                if len(str(value_before)) > len(str(pandas_value)):
                    return
                # else:
                #     print(f"value_before of {field_name} was {value_before} |||| "
                #           f"will be changed by {pandas_value}")
            setattr(self, field_name, pd_series[pandas_field_name])
            attribute_value = getattr(self, field_name)
            if pd.isna(attribute_value):
                setattr(self, field_name, None)
            if eq_none is not None:
                for each_eq_none in eq_none:
                    if attribute_value == each_eq_none:
                        setattr(self, field_name, None)
                        attribute_value = None
                        break
            if verbose and attribute_value is not None:
                print(f"{field_name}: {attribute_value}")

    @abstractmethod
    def update_auto_fill_attributes(self, auto_dict):
        self.auto_dict = auto_dict

def find_orientation_category(orientation_description, entry, orientations_keywords=None,
                              mode="detailed"):
    """
    Fct for orientation_distribution() ->
    :param orientations_keywords: dict with value is a category, value is a list of keywords
    :param orientation_description: the description in which to look for the keywords
    :param mode: could detailed with a low grouping or summary with wide group and only a few returned
    :return:
    """

    if orientations_keywords is None or len(orientations_keywords) == 0:
        if mode == "detailed":
            # 4650 -> aile A
            # 4570 -> chir ped
            # 4651 -> onco-ped
            # 4682 -> soins intensifs
            # 4681 -> rea ped
            # 4680 -> rea neonat
            # 4660 -> UK
            orientations_keywords = dict()
            # {"reoriente": , "retour domicile", "parti sans attendre", "non pris en charge",
            #                           "4650", "4570", "4651"}
            orientations_keywords["reoriente"] = ["reoriente", "mmg", "mmdg", "maison medicale de garde"]
            orientations_keywords["retour domicile"] = ["retour domicile"]
            orientations_keywords["parti sans attendre"] = ["parti sans attendre"]
            orientations_keywords["non pris en charge"] = ["non pris en charge"]
            orientations_keywords["Ped A"] = ["4650"]
            orientations_keywords["Onco-ped B"] = ["4651"]
            orientations_keywords["Chir ped C"] = ["4570"]
            orientations_keywords["Soins intensifs ped"] = ["4682"]
            orientations_keywords["Rea ped"] = ["4681"]
            orientations_keywords["Rea neonat"] = ["4680"]
            orientations_keywords["UK"] = ["4660"]
            orientations_keywords["Ped trinite"] = ["Transfert CENTRE HOSPITALIER LOUIS DOMERGUE TRINITE", "TRINITE",
                                                    "HC PEDIATRIE TNT", "1711"]
            orientations_keywords["Mangot Vulcin"] = ["MANGOT VULCIN"]
            orientations_keywords["Consultation"] = ["consultation"]
            orientations_keywords["Medecin traitant"] = ["medecin traitant"]
            orientations_keywords["Contre avis medical"] = ["contre avis", "evasion"]
            orientations_keywords["Police"] = ["police"]
            orientations_keywords["Non precisee"] = ["Non precisee"]

            orientations_keywords["ZHCD"] = ["4721"]
        else:
            orientations_keywords = dict()
            orientations_keywords["reoriente"] = ["reoriente", "mmg", "mmdg", "maison medicale de garde",
                                                  "MEDECIN DE GARDE"]
            orientations_keywords["retour domicile"] = ["retour domicile", "medecin traitant", "consultation"]
            # 4551 -> gyneco, 3813 -> USC Urgences, "2711" chir generale, "3801" -> UHCD FDF
            orientations_keywords["hospit tradi"] = ["4650", "4651", "4570", "4660",
                                                     "Transfert CENTRE HOSPITALIER LOUIS DOMERGUE TRINITE",
                                                     "TRINITE", "4551",  "2711", "4720", "3801", "PZQ",
                                                     "HC PEDIATRIE TNT", "1711", "MANGOT VULCIN"]
            orientations_keywords["rea"] = ["4682", "4681", "4680", "3813"]
            orientations_keywords["autres"] = ["Non precisee",  "police"]
            orientations_keywords["non_pec"] = ["parti sans attendre", "non pris en charge", "contre avis", "evasion"]

            orientations_keywords["ZHCD"] = ["4721"]

    # first we check if it's a ZHCD:
    if "4721" in orientation_description:
        if entry.zhcd_entry is not None:
            # that way the final destination of the patient is the orientation we keep
            # if the ZHCD is not found, then the patient is "lost"
            zhcd_entry = entry.zhcd_entry
            orientation_description = unidecode(zhcd_entry.orientation.lower())
            return find_orientation_category(orientations_keywords=orientations_keywords,
                                             orientation_description=orientation_description, entry=zhcd_entry)

    else:
        for orientation_category, keywords in orientations_keywords.items():
            for keyword in keywords:
                keyword = unidecode(keyword.lower())
                if keyword in orientation_description:
                    return orientation_category
    return None


def get_fields_map(dfs_list):
    """

    :param dfs_list: list Pandas df, can be used to fill the fields map
    :return:
    """
    # map the content title of the column to the name of the column in the csv
    fields_map = dict()

    if dfs_list is not None:
        if not isinstance(dfs_list, list):
            dfs_list = [dfs_list]
        for df in dfs_list:
            columns = list(df)
            for column_name in columns:
                if column_name not in fields_map:
                    fields_map[column_name] = column_name

    return fields_map


def from_csv_to_asthma_entries(csv_file):
    df = from_csv_to_df(csv_file=csv_file, verbose=False)

    # map the content title of the column to the name of the column in the csv
    fields_map = get_fields_map(df)

   # df[fields_map["arrival_date"]] = pd.to_datetime(df[fields_map["arrival_date"]], dayfirst=True)
    asthma_entries = list()
    for n, pd_series in df.iterrows():
        asthma_entry = AsthmaEntry(entry=None, pd_series=pd_series, fields_map=fields_map, entries_by_ipp=None)
        asthma_entries.append(asthma_entry)
    return asthma_entries


class AsthmaEntry(AutoEntry):

    def __init__(self, pd_series, fields_map, entry=None, entries_by_ipp=None, bool_as_int=False):
        """

        :param entry:
        :param pd_series:
        :param fields_map:
        :param entries_by_ipp:
        :param bool_as_int:
        """
        super().__init__(auto_dict=dict(), bool_as_int=bool_as_int)
        self.entry = entry
        self.entries_by_ipp = entries_by_ipp
        self.fields_map = fields_map

        self.ipp = pd_series[fields_map["ipp"]]
        self.set_int_attr('ipp')

        self.iep = pd_series[fields_map["iep"]]
        self.set_int_attr('iep')

        # ID used to identify this entry
        self.entry_id = self.iep

        self.arrival_date = pd_series[fields_map["arrival_date"]]
        if entry is not None and (pd.isna(self.arrival_date) or self.arrival_date is None):
            self.arrival_date = entry.arrival_date

        self.gender = pd_series[fields_map["gender"]]
        self.set_str_attr('gender')
        if entry is not None and self.gender is None:
            self.gender = entry.gender

        self.age_years = pd_series[fields_map["age_years"]]
        self.set_int_attr('age_years')
        if self.age_years is None:
            self.age_years = entry.age_years

        self.age_in_years_round = pd_series[fields_map["age_in_years_round"]]
        self.set_int_attr('age_in_years_round')

        self.age_months = pd_series[fields_map["age_months"]]
        self.set_int_attr('age_months')
        if self.age_months is None:
            self.age_months = entry.age_months

        self.age_days = pd_series[fields_map["age_days"]]
        self.set_int_attr('age_days')
        if self.age_days is None:
            self.age_days = entry.age_days

        self.age_years_float = pd_series[fields_map["age_years_float"]]
        self.set_float_attr('age_years_float')
        if self.age_years_float is None:
            self.age_years_float = entry.age_years_float

        # Avez-vous senti votre enfant en danger ?
        self.enfant_danger = pd_series[fields_map["enfant_danger"]]
        self.set_bool_attr('enfant_danger')

        # Vous êtes-vous senti impuissant face à la situation (perte de contrôle) ?
        self.impuissant = pd_series[fields_map["impuissant"]]
        self.set_bool_attr('impuissant')

        # Avez-vous eu l’impression d’avoir utilisé toutes les ressources thérapeutiques possibles
        self.ressources_full_mode = pd_series[fields_map["ressources_full_mode"]]
        self.set_bool_attr('ressources_full_mode')

        # Avez-vous consultez un médecin dans les 5 jours précédents concernant cette crise d'asthme
        self.consult_med_dans_les_5_j = pd_series[fields_map["consult_med_dans_les_5_j"]]
        self.set_bool_attr('consult_med_dans_les_5_j')

        self.comments_fact_venue = pd_series[fields_map["comments_fact_venue"]]
        self.set_str_attr('comments_fact_venue')

        # SUIVI



        # L’asthme de votre enfant est il suivi par un médecin
        self.suivi_medecin = pd_series[fields_map["suivi_medecin"]]
        self.set_bool_attr('suivi_medecin')

        self.suivi_med_traitant = pd_series[fields_map["suivi_med_traitant"]]
        self.set_bool_attr('suivi_med_traitant')

        self.suivi_pneumologue = pd_series[fields_map["suivi_pneumologue"]]
        self.set_bool_attr('suivi_pneumologue')

        self.suivi_pediatre = pd_series[fields_map["suivi_pediatre"]]
        self.set_bool_attr('suivi_pediatre')

        self.suivi_allergo = pd_series[fields_map["suivi_allergo"]]
        self.set_bool_attr('suivi_allergo')

        self.suivi_autre = pd_series[fields_map["suivi_autre"]]
        self.set_bool_attr('suivi_autre')

        self.age_premiere_ventoline = pd_series[fields_map["age_premiere_ventoline"]]
        self.set_int_attr('age_premiere_ventoline')

        # la dernière consultation avec le médecin en charge de l’asthme date de moins de 6 mois
        self.last_consult_suivi_inf_6m = pd_series[fields_map["last_consult_suivi_inf_6m"]]
        self.set_bool_attr('last_consult_suivi_inf_6m')

        self.last_consult_suivi_6m_1a = pd_series[fields_map["last_consult_suivi_6m_1a"]]
        self.set_bool_attr('last_consult_suivi_6m_1a')

        self.last_consult_suivi_sup_1a = pd_series[fields_map["last_consult_suivi_sup_1a"]]
        self.set_bool_attr('last_consult_suivi_sup_1a')

        self.efr_done = pd_series[fields_map["efr_done"]]
        self.set_bool_attr('efr_done')

        self.annee_derniere_efr = pd_series[fields_map["annee_derniere_efr"]]
        self.set_int_attr('annee_derniere_efr')

        self.pai_done = pd_series[fields_map["pai_done"]]
        self.set_bool_attr('pai_done')

        self.pai_fait_par = pd_series[fields_map["pai_fait_par"]]
        self.set_str_attr('pai_fait_par')

        self.comments_suivi = pd_series[fields_map["comments_suivi"]]
        self.set_str_attr('comments_suivi')

        # CONTROLE

        # Sur les 4 dernières semaines, votre enfant a-t-il eu des symptômes liés à l’asthme
        # pendant plusieurs minutes, et plus de 2 jours par semaine.
        self.controle_symptomes = pd_series[fields_map["controle_symptomes"]]
        self.set_bool_attr('controle_symptomes')

        # Sur les 4 dernières semaines, votre enfant a-t-il eu une limitation de ses activités
        # habituelles dû à l’asthme
        self.controle_limitation_activite = pd_series[fields_map["controle_limitation_activite"]]
        self.set_bool_attr('controle_limitation_activite')

        # Sur les 4 dernières semaines, votre enfant a utilisé un inhalateur de secours,
        # ou pris un traitement par nébulisation (par exemple la Ventoline) moins de 1 fois par semaine
        self.controle_vento_inf_1x_sem = pd_series[fields_map["controle_vento_inf_1x_sem"]]
        self.set_bool_attr('controle_vento_inf_1x_sem')

        self.controle_vento_plus_ou_1x_sem = pd_series[fields_map["controle_vento_plus_ou_1x_sem"]]
        self.set_bool_attr('controle_vento_plus_ou_1x_sem')

        # Sur les 4 dernière semaines votre enfant s’est-il réveillé pendant la nuit à cause de son
        # asthme ?
        self.controle_nuit = pd_series[fields_map["controle_nuit"]]
        self.set_bool_attr('controle_nuit')

        self.comments_controle = pd_series[fields_map["comments_controle"]]
        self.set_str_attr('comments_controle')

        # ATCD
        self.allergies_classiques = pd_series[fields_map["allergies_classiques"]]
        self.set_bool_attr('allergies_classiques')

        self.allergies_autres = pd_series[fields_map["allergies_autres"]]
        self.set_str_attr('allergies_autres')

        self.atcd_cortico_6_mois = pd_series[fields_map["atcd_cortico_6_mois"]]
        self.set_bool_attr('atcd_cortico_6_mois')

        self.atcd_rea = pd_series[fields_map["atcd_rea"]]
        self.set_bool_attr('atcd_rea')

        self.atcd_hospit = pd_series[fields_map["atcd_hospit"]]
        self.set_bool_attr('atcd_hospit')

        self.comments_atcd = pd_series[fields_map["comments_atcd"]]
        self.set_str_attr('comments_atcd')

        # CONNAISSANCE

        self.ttt_de_fond_flixotide = pd_series[fields_map["ttt_de_fond_flixotide"]]
        self.set_bool_attr('ttt_de_fond_flixotide')

        self.ttt_de_fond_seretide = pd_series[fields_map["ttt_de_fond_seretide"]]
        self.set_bool_attr('ttt_de_fond_seretide')

        self.ttt_de_fond_singulair = pd_series[fields_map["ttt_de_fond_singulair"]]
        self.set_bool_attr('ttt_de_fond_singulair')

        self.ttt_de_fond_ne_sais_pas = pd_series[fields_map["ttt_de_fond_ne_sais_pas"]]
        self.set_bool_attr('ttt_de_fond_ne_sais_pas')

        self.ttt_de_fond_autre = pd_series[fields_map["ttt_de_fond_autre"]]
        self.set_str_attr('ttt_de_fond_autre')

        self.ttt_de_fond_aucun = pd_series[fields_map["ttt_de_fond_aucun"]]
        self.set_bool_attr('ttt_de_fond_aucun')

        self.ecole_asthme_connue = pd_series[fields_map["ecole_asthme_connue"]]
        self.set_bool_attr('ecole_asthme_connue')

        self.contact_ecole_asthme = pd_series[fields_map["contact_ecole_asthme"]]
        self.set_bool_attr('contact_ecole_asthme')

        self.chambre_inhalation = pd_series[fields_map["chambre_inhalation"]]
        self.set_bool_attr('chambre_inhalation')

        self.calendrier_crise = pd_series[fields_map["calendrier_crise"]]
        self.set_bool_attr('calendrier_crise')

        self.peack_flow = pd_series[fields_map["peack_flow"]]
        self.set_bool_attr('peack_flow')

        self.peack_flow_bien_utilise = pd_series[fields_map["peack_flow_bien_utilise"]]
        self.set_bool_attr('peack_flow_bien_utilise')

        self.comments_connaissance = pd_series[fields_map["comments_connaissance"]]
        self.set_str_attr('comments_connaissance')

        # TRAITEMENT DE LA CRISE

        self.plan_action_maison = pd_series[fields_map["plan_action_maison"]]
        self.set_bool_attr('plan_action_maison')

        self.plan_action_suivi = pd_series[fields_map["plan_action_suivi"]]
        self.set_bool_attr('plan_action_suivi')

        self.plan_action_des_urgences = pd_series[fields_map["plan_action_des_urgences"]]
        self.set_bool_attr('plan_action_des_urgences')

        self.prescription_vento = pd_series[fields_map["prescription_vento"]]
        self.set_bool_attr('prescription_vento')

        self.ttt_vento_avant_urgences = pd_series[fields_map["ttt_vento_avant_urgences"]]
        self.set_bool_attr('ttt_vento_avant_urgences')

        self.ttt_cortico_avant_urgences = pd_series[fields_map["ttt_cortico_avant_urgences"]]
        self.set_bool_attr('ttt_cortico_avant_urgences')

        self.aucun_ttt_avant_urgences = pd_series[fields_map["aucun_ttt_avant_urgences"]]
        self.set_bool_attr('aucun_ttt_avant_urgences')

        self.autre_ttt_avant_urgences = pd_series[fields_map["autre_ttt_avant_urgences"]]
        self.set_str_attr('autre_ttt_avant_urgences')
        if self.autre_ttt_avant_urgences is not None:
            if self.autre_ttt_avant_urgences.lower().strip() in ["false", "nr"]:
                self.autre_ttt_avant_urgences = None

        self.n_bouffees_vento = pd_series[fields_map["n_bouffees_vento"]]
        self.set_int_attr('n_bouffees_vento')

        self.inf_20m_entre_series_vento = pd_series[fields_map["inf_20m_entre_series_vento"]]
        self.set_bool_attr('inf_20m_entre_series_vento')

        self.entre_20m_1h_entre_series_vento = pd_series[fields_map["entre_20m_1h_entre_series_vento"]]
        self.set_bool_attr('entre_20m_1h_entre_series_vento')

        self.entre_1h_4h_entre_series_vento = pd_series[fields_map["entre_1h_4h_entre_series_vento"]]
        self.set_bool_attr('entre_1h_4h_entre_series_vento')
        #

        self.plus_4h_entre_series_vento = pd_series[fields_map["plus_4h_entre_series_vento"]]
        self.set_bool_attr('plus_4h_entre_series_vento')

        self.n_repet_series_vento = pd_series[fields_map["n_repet_series_vento"]]
        self.set_bool_attr('n_repet_series_vento')

        self.n_respi_chbre_inhalation = pd_series[fields_map["n_respi_chbre_inhalation"]]
        self.set_str_attr('n_respi_chbre_inhalation')

        self.delai_urg_inf_2h = pd_series[fields_map["delai_urg_inf_2h"]]
        self.set_str_attr('delai_urg_inf_2h')

        #
        self.delai_urg_2h_6h = pd_series[fields_map["delai_urg_2h_6h"]]
        self.set_bool_attr('delai_urg_2h_6h')

        self.delai_urg_6h_24h = pd_series[fields_map["delai_urg_6h_24h"]]
        self.set_bool_attr('delai_urg_6h_24h')

        self.delai_urg_sup_24h = pd_series[fields_map["delai_urg_sup_24h"]]
        self.set_bool_attr('delai_urg_sup_24h')

        self.appel_du_15 = pd_series[fields_map["appel_du_15"]]
        self.set_bool_attr('appel_du_15')

        self.comments_ttt_crise = pd_series[fields_map["comments_ttt_crise"]]
        self.set_str_attr('comments_ttt_crise')

        self.comments = pd_series[fields_map["comments"]]
        self.set_str_attr('comments')

        self.is_zhcd = pd_series[fields_map["is_zhcd"]]
        self.set_bool_attr('is_zhcd')

        if self.is_zhcd is None and self.entry is not None:
            if entry.zhcd_entry is not None:
                self.is_zhcd = True
            else:
                self.is_zhcd = False

        self.is_hospit_tradi = pd_series[fields_map["is_hospit_tradi"]]
        self.set_bool_attr('is_hospit_tradi')

        self.is_hospit_rea = pd_series[fields_map["is_hospit_rea"]]
        self.set_bool_attr('is_hospit_rea')

        if self.is_hospit_tradi is None or self.is_hospit_rea is None:
            if self.entry is not None and self.entry.orientation is not None:
                orientation_lower = unidecode(self.entry.orientation.lower())
                orientation_category = find_orientation_category(orientation_description=orientation_lower,
                                                                 entry=self.entry, mode="short")
                if orientation_category is None:
                    print(f"{self.entry.ipp}: Error: orientation_category is None: {self.entry.orientation}")
                    if self.entry.zhcd_entry is not None:
                        print(f"zhcd -> {self.entry.zhcd_entry.orientation}")
                    self.is_hospit = None
                    self.is_hospit_rea = None
                else:
                    if "hospit tradi" in orientation_category:
                        self.is_hospit_tradi = True
                    else:
                        self.is_hospit_tradi = False

                    if "rea" in orientation_category:
                        self.is_hospit_rea = True
                    else:
                        self.is_hospit_rea = False

        self.n_passages_urgences = pd_series[fields_map["n_passages_urgences"]]
        self.set_int_attr('n_passages_urgences')

        self.n_passages_urgences_asthme = pd_series[fields_map["n_passages_urgences_asthme"]]
        self.set_int_attr('n_passages_urgences_asthme')

        # TODO: ajout sao2_iao, n_nebu_salbu	n_nebu_atrovent	cortico_urgences

        self.atcd_dechoc = pd_series[fields_map["atcd_dechoc"]]
        self.set_bool_attr('atcd_dechoc')

        if self.entries_by_ipp is not None and self.n_passages_urgences is None and self.ipp in self.entries_by_ipp:
            n_passages_urgences = 0
            n_passages_urgences_asthme = 0
            atcd_dechoc = False
            for other_entry in self.entries_by_ipp[self.entry.ipp]:
                if other_entry == self.entry:
                    continue
                if other_entry.arrival_date < self.entry.arrival_date:
                    n_passages_urgences += 1
                    if other_entry.main_diagnostic is not None:
                        if "asthme" in other_entry.main_diagnostic.lower():
                            n_passages_urgences_asthme += 1
                            if other_entry.is_in_dechoc_box:
                                atcd_dechoc = True
            self.n_passages_urgences = n_passages_urgences
            self.n_passages_urgences_asthme = n_passages_urgences_asthme
            self.atcd_dechoc = atcd_dechoc

        self.md_in_charge = pd_series[fields_map["md_in_charge"]]
        self.set_str_attr('md_in_charge')

        if self.md_in_charge is None and entry is not None:
            if entry.medical_team is not None:
                team_members = unidecode(entry.medical_team.lower()).split()
                # the first two should be the first person connected (first name and last name or the other way around)
                if len(team_members) > 1:
                    self.md_in_charge = " ".join(team_members[:2])

    def update_auto_fill_attributes(self, auto_dict):
        pass

