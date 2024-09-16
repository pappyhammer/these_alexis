import numpy as np

def sort_two_list(main_list, second_list, order="ascending"):
    """
    Return two list, using the main_list to sort both respecting re-ordering of the first one
    to order the second one
    ex: if main_list = [3, 1, 6] and second_list = ["trois", "un", "six"]
    alors pour ascending, it retursn [1, 3, 6] and ['un", "trois", "six"]
    :param main_list:  list of int
    :param second_list: list of elements of any type, should be same len as main_list
    :param order:  "ascending" or "descending"
    :return:
    """

    assert len(main_list) == len(second_list)

    values_indices_sorted = list(np.argsort(main_list))
    if order == "descending":
        values_indices_sorted = values_indices_sorted[::-1]

    ordered_main_list = list()
    ordered_second_list = list()

    for index_ordered in values_indices_sorted:
        ordered_main_list.append(main_list[index_ordered])
        ordered_second_list.append(second_list[index_ordered])

    return ordered_main_list, ordered_second_list