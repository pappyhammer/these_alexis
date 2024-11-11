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


    def set_ttt_attribute(self, attr_name, keywords, verbose=True, delay_attr=None, count_it=False,
                          with_associate_keyword=None):
        """
        Set a field corresponding to a treatment prescribed by searching it
        in the prescribed ttt
        :param attr_name:
        :param keywords:
        :param verbose:
        :param delay_attr: str attribute name in Entry, if not None, set the attr to the delay between arrival
        and the time of done date
        :param count_it: if True, it counts how many times it is given and set the attribute to an int value
        :param with_associate_keyword: if not None, then we need this keyword in the prescriptioin as well with all
        the keywords
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
        # zhcd dict contains the ttt given before in urg
        if self.entry.zhcd_entry is not None:
            ttt_received_dicts = [self.entry.zhcd_entry.ttt_received_dict]

        counter = 0

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
                            # if keyword in ["salbu", "vento"]:
                            #     print(f"FOUND salbu/vento: {prescription}: {value_ttt['date']}")
                            if with_associate_keyword is None or \
                                    with_associate_keyword in unidecode(prescription).lower():
                                if count_it:
                                    list_dates = value_ttt["date"]
                                    counter += len(list_dates)
                                else:
                                    setattr(self, attr_name, True)
                                    if delay_attr is not None:
                                        list_dates = value_ttt["date"]
                                        if len(list_dates) > 0:
                                            # we take the first one prescribed
                                            done_date = list_dates[0][1]
                                            hours, hours_float, minutes = duration_bw_dates(later_date=done_date,
                                                                                            early_date=self.entry.arrival_date)
                                            setattr(self, delay_attr, minutes)
                            if verbose and hasattr(self, "ipp"):
                                print(f"- {self.ipp} with {attr_name}: {prescription}")
                            break_it = True
                            break
                    if break_it and not count_it:
                        break
                if break_it and not count_it:
                    break
        if count_it:
            setattr(self, attr_name, counter)
        else:
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

        # used for some plots
        self.group_label = None

        self.arrival_date = pd_series[fields_map["arrival_date"]]
        if entry is not None and (pd.isna(self.arrival_date) or self.arrival_date is None):
            self.arrival_date = entry.arrival_date

        self.gender = pd_series[fields_map["gender"]]
        self.set_str_attr('gender')
        if entry is not None and self.gender is None:
            self.gender = entry.gender

        self.age_years = pd_series[fields_map["age_years"]]
        self.set_int_attr('age_years')
        if entry is not None and self.age_years is None:
            self.age_years = entry.age_years

        self.age_in_years_round = pd_series[fields_map["age_in_years_round"]]
        self.set_str_attr('age_in_years_round')
        self.less_than_6_y = None
        if "<" in self.age_in_years_round:
            self.less_than_6_y = True
        elif ">" in self.age_in_years_round:
            self.less_than_6_y = False
        else:
            age = int(self.age_in_years_round)
            if age < 6:
                self.less_than_6_y = True
            else:
                self.less_than_6_y = False

        self.age_months = pd_series[fields_map["age_months"]]
        self.set_int_attr('age_months')
        if entry is not None and self.age_months is None:
            self.age_months = entry.age_months

        self.age_days = pd_series[fields_map["age_days"]]
        self.set_int_attr('age_days')
        if entry is not None and self.age_days is None:
            self.age_days = entry.age_days

        self.age_years_float = pd_series[fields_map["age_years_float"]]
        self.set_float_attr('age_years_float')
        if entry is not None and self.age_years_float is None:
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
        if self.less_than_6_y:
            self.efr_done = None

        self.annee_derniere_efr = pd_series[fields_map["annee_derniere_efr"]]
        self.set_int_attr('annee_derniere_efr')
        if self.less_than_6_y:
            self.annee_derniere_efr = None

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

        self.ttt_de_fond_ne_sais_pas = pd_series[fields_map["ttt_de_fond_ne_sais_pas"]]
        self.set_bool_attr('ttt_de_fond_ne_sais_pas')

        self.ttt_de_fond_flixotide = pd_series[fields_map["ttt_de_fond_flixotide"]]
        self.set_bool_attr('ttt_de_fond_flixotide')
        if self.ttt_de_fond_ne_sais_pas:
            self.ttt_de_fond_flixotide = None

        self.ttt_de_fond_seretide = pd_series[fields_map["ttt_de_fond_seretide"]]
        self.set_bool_attr('ttt_de_fond_seretide')
        if self.ttt_de_fond_ne_sais_pas:
            self.ttt_de_fond_seretide = None

        self.ttt_de_fond_singulair = pd_series[fields_map["ttt_de_fond_singulair"]]
        self.set_bool_attr('ttt_de_fond_singulair')
        if self.ttt_de_fond_ne_sais_pas:
            self.ttt_de_fond_singulair = None

        self.ttt_de_fond_autre = pd_series[fields_map["ttt_de_fond_autre"]]
        self.set_str_attr('ttt_de_fond_autre')
        if self.ttt_de_fond_ne_sais_pas:
            self.ttt_de_fond_autre = None

        self.ttt_de_fond_aucun = pd_series[fields_map["ttt_de_fond_aucun"]]
        self.set_bool_attr('ttt_de_fond_aucun')
        if self.ttt_de_fond_ne_sais_pas:
            self.ttt_de_fond_aucun = None

        self.ecole_asthme_connue = pd_series[fields_map["ecole_asthme_connue"]]
        self.set_bool_attr('ecole_asthme_connue')

        self.contact_ecole_asthme = pd_series[fields_map["contact_ecole_asthme"]]
        self.set_bool_attr('contact_ecole_asthme')

        self.ecole_asthme_connue_et_contact = None
        self.ecole_asthme_connue_sans_contact = None
        self.ecole_asthme_non_connue = None
        if self.ecole_asthme_connue is not None:
            if not self.ecole_asthme_connue:
                self.ecole_asthme_non_connue = True
                self.ecole_asthme_connue_et_contact = False
                self.ecole_asthme_connue_sans_contact = False
            else:
                self.ecole_asthme_non_connue = False
                if self.contact_ecole_asthme is not None:
                    if self.contact_ecole_asthme:
                        self.ecole_asthme_connue_et_contact = True
                        self.ecole_asthme_connue_sans_contact = False
                    else:
                        self.ecole_asthme_connue_et_contact = False
                        self.ecole_asthme_connue_sans_contact = True

        self.chambre_inhalation = pd_series[fields_map["chambre_inhalation"]]
        self.set_bool_attr('chambre_inhalation')

        self.calendrier_crise = pd_series[fields_map["calendrier_crise"]]
        self.set_bool_attr('calendrier_crise')

        self.peack_flow = pd_series[fields_map["peack_flow"]]
        self.set_bool_attr('peack_flow')
        if self.less_than_6_y:
            self.annee_derniere_efr = None

        self.peack_flow_bien_utilise = pd_series[fields_map["peack_flow_bien_utilise"]]
        self.set_bool_attr('peack_flow_bien_utilise')
        if self.less_than_6_y:
            self.peack_flow_bien_utilise = None

        self.comments_connaissance = pd_series[fields_map["comments_connaissance"]]
        self.set_str_attr('comments_connaissance')

        # TRAITEMENT DE LA CRISE

        self.plan_action_maison = pd_series[fields_map["plan_action_maison"]]
        self.set_bool_attr('plan_action_maison')

        self.plan_action_suivi = pd_series[fields_map["plan_action_suivi"]]
        self.set_bool_attr('plan_action_suivi')
        if self.plan_action_maison is None or not self.plan_action_maison:
            self.plan_action_suivi = None

        self.plan_action_des_urgences = pd_series[fields_map["plan_action_des_urgences"]]
        self.set_bool_attr('plan_action_des_urgences')
        if self.plan_action_maison is None or not self.plan_action_maison:
            self.plan_action_des_urgences = None

        self.plan_action_des_urgences_si_present = None
        if self.plan_action_maison is not None:
            if self.plan_action_maison:
                if self.plan_action_des_urgences:
                    self.plan_action_des_urgences_si_present = True
                else:
                    self.plan_action_des_urgences_si_present = False

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

        if (not self.inf_20m_entre_series_vento) and (not self.entre_20m_1h_entre_series_vento) and \
                (not self.entre_1h_4h_entre_series_vento) and (not self.plus_4h_entre_series_vento):
            self.inf_20m_entre_series_vento = None
            self.entre_20m_1h_entre_series_vento = None
            self.entre_1h_4h_entre_series_vento = None
            self.plus_4h_entre_series_vento = None

        self.n_repet_series_vento = pd_series[fields_map["n_repet_series_vento"]]
        self.set_str_attr('n_repet_series_vento')

        self.n_repet_series_vento_0 = None
        self.n_repet_series_vento_1 = None
        self.n_repet_series_vento_2 = None
        self.n_repet_series_vento_sup_3 = None
        if self.n_repet_series_vento is not None:
            try:
                n_repet = int(self.n_repet_series_vento)
                if n_repet == 0:
                    self.n_repet_series_vento_0 = True
                    self.n_repet_series_vento_1 = False
                    self.n_repet_series_vento_2 = False
                    self.n_repet_series_vento_sup_3 = False
                elif n_repet == 1:
                    self.n_repet_series_vento_0 = False
                    self.n_repet_series_vento_1 = True
                    self.n_repet_series_vento_2 = False
                    self.n_repet_series_vento_sup_3 = False
                elif n_repet == 2:
                    self.n_repet_series_vento_0 = False
                    self.n_repet_series_vento_1 = False
                    self.n_repet_series_vento_2 = True
                    self.n_repet_series_vento_sup_3 = False
                else:
                    self.n_repet_series_vento_0 = False
                    self.n_repet_series_vento_1 = False
                    self.n_repet_series_vento_2 = False
                    self.n_repet_series_vento_sup_3 = True
            except ValueError:
                if ">" in self.n_repet_series_vento:
                    self.n_repet_series_vento_0 = False
                    self.n_repet_series_vento_1 = False
                    self.n_repet_series_vento_2 = False
                    self.n_repet_series_vento_sup_3 = True
        elif self.ttt_vento_avant_urgences is False:
            self.n_repet_series_vento_0 = True
            self.n_repet_series_vento_1 = False
            self.n_repet_series_vento_2 = False
            self.n_repet_series_vento_sup_3 = False

        self.n_respi_chbre_inhalation = pd_series[fields_map["n_respi_chbre_inhalation"]]
        self.set_str_attr('n_respi_chbre_inhalation')

        self.n_respi_chbre_inhalation_sup_10 = None
        if self.n_respi_chbre_inhalation is not None:
            try:
                n_respi = int(self.n_respi_chbre_inhalation)
                if n_respi >= 10:
                    self.n_respi_chbre_inhalation_sup_10 = True
                else:
                    self.n_respi_chbre_inhalation_sup_10 = False
            except ValueError:
                if "s" in self.n_repet_series_vento:
                    n_respi = int(self.n_respi_chbre_inhalation[:-1])
                    if n_respi >= 10:
                        self.n_respi_chbre_inhalation_sup_10 = True
                    else:
                        self.n_respi_chbre_inhalation_sup_10 = False

        self.delai_urg_inf_2h = pd_series[fields_map["delai_urg_inf_2h"]]
        self.set_bool_attr('delai_urg_inf_2h')

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

        self.poids = pd_series[fields_map["poids"]]
        self.set_float_attr('poids')
        if self.entry is not None and self.entry.arrival_weight is not None:
            self.poids = float(self.entry.arrival_weight)

        # if True means the right number of ventoline has been done at home.
        self.correct_n_bouffee_vento = None
        if self.poids is None:
            # no need for it if weight is not None
            self.n_bouffees_vento = None
        elif self.n_bouffees_vento is not None:
            if self.poids < 4:
                n_boufees_goal = 1
            elif self.poids < 6:
                n_boufees_goal = 2
            elif self.poids < 8:
                n_boufees_goal = 3
            elif self.poids < 10:
                n_boufees_goal = 4
            elif self.poids < 12:
                n_boufees_goal = 5
            elif self.poids < 14:
                n_boufees_goal = 6
            elif self.poids < 16:
                n_boufees_goal = 7
            elif self.poids < 18:
                n_boufees_goal = 8
            elif self.poids < 20:
                n_boufees_goal = 9
            else:
                n_boufees_goal = 10

            if n_boufees_goal - self.n_bouffees_vento <= 1:
                self.correct_n_bouffee_vento = True
            else:
                # print(f"Bouffées reçues: {self.n_bouffees_vento}, goal {n_boufees_goal} pour poids {self.poids}")
                self.correct_n_bouffee_vento = False

        self.sao2_iao = pd_series[fields_map["sao2_iao"]]
        self.set_int_attr('sao2_iao')
        if self.sao2_iao is None and self.entry is not None:
            sao2 = self.entry.get_iao_constante(cste_name="sao2")
            if sao2 is not None:
                self.sao2_iao = sao2

        self.duree_sejour_urgences = pd_series[fields_map["duree_sejour_urgences"]]
        self.set_int_attr('duree_sejour_urgences')
        if self.duree_sejour_urgences is None and self.entry is not None:
            self.duree_sejour_urgences = entry.get_duration_of_stay()

        verbose_ttt = False

        self.cortico_urgences = pd_series[fields_map["cortico_urgences"]]
        self.set_bool_attr('cortico_urgences')
        self.set_ttt_attribute(attr_name="cortico_urgences", keywords=["solupred", "solumedrol", "celestene"],
                               verbose=verbose_ttt)

        self.n_nebu_salbu = pd_series[fields_map["n_nebu_salbu"]]
        self.set_int_attr('n_nebu_salbu')
        self.set_ttt_attribute(attr_name="n_nebu_salbu", keywords=["ventoline 5mg/2,5ml", "ventoline <16kg et >10kg",
                                                                   "ventoline >16 kg",
                                                                   "ventoline <10kg",
                                                                   "salbutamol (sulfate) 5 mg/2,5 ml",
                                                                   "salbutamol (sulfate) 2,5 mg/2,5 ml"],
                               verbose=verbose_ttt, count_it=True)
                               # with_associate_keyword="nebu",

        self.n_nebu_atrovent = pd_series[fields_map["n_nebu_atrovent"]]
        self.set_int_attr('n_nebu_atrovent')
        self.set_ttt_attribute(attr_name="n_nebu_atrovent", keywords=["atrovent"],
                               verbose=verbose_ttt, count_it=True)

        self.atrovent_in_first_round = pd_series[fields_map["atrovent_in_first_round"]]
        self.set_bool_attr('atrovent_in_first_round')
        if self.entry is not None and self.atrovent_in_first_round is None and \
                self.n_nebu_atrovent is not None and self.n_nebu_atrovent > 0 and \
                self.n_nebu_salbu is not None and self.n_nebu_salbu > 0:
            self.is_atrovent_in_first_round()


        self.pec_dechoc = pd_series[fields_map["pec_dechoc"]]
        self.set_bool_attr('pec_dechoc')

        if self.entry is not None and self.pec_dechoc is None:
            if self.entry.is_in_dechoc_box:
                self.pec_dechoc = True
            else:
                self.pec_dechoc = False

        self.atcd_dechoc = pd_series[fields_map["atcd_dechoc"]]
        self.set_bool_attr('atcd_dechoc')

        if self.entries_by_ipp is not None and self.n_passages_urgences is None and self.ipp in self.entries_by_ipp \
                and self.entry is not None:
            n_passages_urgences = 0
            n_passages_urgences_asthme = 0
            atcd_dechoc = False
            for other_entry in self.entries_by_ipp[self.ipp]:
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


        """
                    Plusieurs critères ont été nécessaires à prendre en compte pour définir la qualité de la prise 
                    en charge thérapeutique de la crise d’asthme. Ainsi nous avons inventé un score allant de 0 à 10 afin d’approcher au mieux son évaluation.
                    Si absence de prise de BDCA: 0/10 
                    Si prise de BDCA: +3 points
                    Si bon nombre de bouffée par rapport au poids: +1 point
                    Si prise de CSO: +2 points
                    Si prise 3 séries de BDCA: +2 points,  2 prise de BDCA: +1, 1 prise de BDCA: +0.
                    Si intervalle de prise <1h: +1 point.
                    Si appel samu: +1 point.
                    On estime donc qu’un score:
                    -mauvais: 0 à 3/10
                    -Modéré: 3 à 5/10.
                    -Bon: 5 à 7/10
                    -Parfait: 7 à 10/10.
                """
        self.score_quality = None
        self.measure_quality_score()

        self.well_controlled = None
        self.partly_controlled = None
        self.uncontrolled = None
        self.measure_asthma_control()


    def is_atrovent_in_first_round(self):
        if not hasattr(self, 'entry'):
            return

        if self.entry is None:
            return

        # prescription in urg and zhcd
        ttt_received_dicts = [self.entry.ttt_received_dict]
        if self.entry.zhcd_entry is not None:
            ttt_received_dicts = [self.entry.zhcd_entry.ttt_received_dict]

        first_atrovent_date = None

        for ttt_received_dict in ttt_received_dicts:
            if len(ttt_received_dict) > 0:
                for key_ttt, value_ttt in ttt_received_dict.items():
                    # key_ttt (prescription_date, md_name, prescription)
                    # value is a dict with key "voie" and la voie used, and "date" with value a list
                    # of tuple (due_date, done_date)
                    prescription_date, md_name, prescription = key_ttt
                    if "atrovent" in unidecode(prescription).lower():
                        list_dates = value_ttt["date"]
                        if len(list_dates) > 0:
                            # we take the first one prescribed
                            if first_atrovent_date is None:
                                first_atrovent_date = list_dates[0][1]
                                break
            if first_atrovent_date is not None:
                break

        if first_atrovent_date is None:
            return

        # date of the last of the first 3 salbu
        last_salbu_1_series_date = None
        keywords = ["ventoline 5mg/2,5ml", "ventoline <16kg et >10kg",
                    "ventoline >16 kg",
                    "ventoline <10kg",
                    "salbutamol (sulfate) 5 mg/2,5 ml",
                    "salbutamol (sulfate) 2,5 mg/2,5 ml"]
        all_salbu_dates = []
        for ttt_received_dict in ttt_received_dicts:
            if len(ttt_received_dict) > 0:
                for key_ttt, value_ttt in ttt_received_dict.items():
                    # key_ttt (prescription_date, md_name, prescription)
                    # value is a dict with key "voie" and la voie used, and "date" with value a list
                    # of tuple (due_date, done_date)
                    prescription_date, md_name, prescription = key_ttt
                    for keyword in keywords:
                        if keyword in unidecode(prescription).lower():
                            list_dates = value_ttt["date"]
                            if len(list_dates) > 0:
                                all_salbu_dates.extend([date_tuple[1] for date_tuple in list_dates])

        all_salbu_dates.sort()
        # print(f"all_salbu_dates {all_salbu_dates}")

        if len(all_salbu_dates) < 3:
            return

        if first_atrovent_date <= all_salbu_dates[2]:
            self.atrovent_in_first_round = True
        else:
            self.atrovent_in_first_round = False


    def measure_asthma_control(self):
        n_items = 0

        if self.controle_symptomes is None:
            return
        if self.controle_limitation_activite is None:
            return
        if self.controle_vento_plus_ou_1x_sem is None:
            return
        if self.controle_nuit is None:
            return

        n_items = sum([self.controle_symptomes, self.controle_limitation_activite,
                       self.controle_vento_plus_ou_1x_sem, self.controle_nuit])

        if n_items == 0:
            self.well_controlled = True
            self.partly_controlled = False
            self.uncontrolled = False
        elif n_items <= 2:
            self.well_controlled = False
            self.partly_controlled = True
            self.uncontrolled = False
        else:
            self.well_controlled = False
            self.partly_controlled = False
            self.uncontrolled = True

    def measure_quality_score(self):
        self.score_quality = 0

        if self.appel_du_15 is None:
            self.score_quality = None
            return
        if self.appel_du_15:
            self.score_quality += 1

        if self.ttt_vento_avant_urgences is None:
            self.score_quality = None
            return
        if not self.ttt_vento_avant_urgences:
            return

        self.score_quality += 3

        # if not self.ttt_vento_avant_urgences:

        if self.correct_n_bouffee_vento is None:
            self.score_quality = None
            return
        if self.correct_n_bouffee_vento:
            self.score_quality += 1

        if self.ttt_cortico_avant_urgences is None:
            self.score_quality = None
            return
        if self.ttt_cortico_avant_urgences:
            self.score_quality += 2

        if self.n_repet_series_vento_2 is None:
            self.score_quality = None
            return
        if self.n_repet_series_vento_2:
            self.score_quality += 1

        if self.n_repet_series_vento_sup_3 is None:
            self.score_quality = None
            return
        if self.n_repet_series_vento_sup_3:
            self.score_quality += 2

        if self.inf_20m_entre_series_vento is None:
            self.score_quality = None
            return
        if self.inf_20m_entre_series_vento or self.entre_20m_1h_entre_series_vento:
            self.score_quality += 1





    def update_auto_fill_attributes(self, auto_dict):
        pass

