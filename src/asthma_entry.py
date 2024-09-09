from abc import ABC, abstractmethod
import pandas as pd
from unidecode import unidecode
from date_utils import duration_bw_dates

class AsthmaEntry:

    def __init__(self, csv_file):
        pass


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