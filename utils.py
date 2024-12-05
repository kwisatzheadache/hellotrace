from itertools import combinations, product
from typing import Any, Callable, Tuple, List

from pandas import DataFrame
from tabulate import tabulate

def make_distinct_value_dict(table: DataFrame) -> dict:
    distinct_value_dict = {}
    for column in table.columns:
        distinct_values = table[column].dropna().unique().tolist()
        distinct_value_dict[column] = distinct_values
    return distinct_value_dict

def make_rows_per_distinct_value_dict(table: DataFrame, distinct_value_dict: dict) -> dict:
    rows_per_distinct_value = {}
    for column, distinct_values in distinct_value_dict.items():
        value_counts = table[column].value_counts(dropna=True).to_dict()
        rows_per_distinct_value[column] = value_counts
    return rows_per_distinct_value

def get_value_type(value: Any) -> tuple:
    if isinstance(value, int):
        return "int", value
    if isinstance(value, float):
        return "float", value
    return "str", value

def make_single_query_filter(dimension_value_tuple: tuple) -> str:
    """
    :param dimension_value_tuple: (dimension_name, value)
    :return:
    """
    value = dimension_value_tuple[1]
    value_type, value = get_value_type(value)
    # Note that dimension name uses backticks ``, not quotes ''
    if value_type == "str":
        query = f"`{dimension_value_tuple[0]}` == \'{value}\'"
    else:
        query = f"`{dimension_value_tuple[0]}` == {value}"
    return query

def make_many_query_filter(dimension_value_tuples: list[tuple]) -> str:
    """
    dimension_value_tuples: list of (dimension_name, value)
    :param dimension_value_tuples:
    :return:
    """
    query = ""
    for item in dimension_value_tuples:
        if query != "":
            query += " & "
        query += make_single_query_filter(item)
    return query

def build_query_from_subset_list_indices_and_index_map(subset_list: list, indices: list, index_map: dict)-> str:
    if len(subset_list) != len(indices):
        raise ValueError("subset and indices must have same length")
    dimension_value_tuples = []
    for i in range(len(subset_list)):
        value = subset_list[i]
        dimension_index = indices[i]
        dimension_name = index_map[dimension_index]
        query_tuple = (dimension_name, value)
        dimension_value_tuples.append(query_tuple)
    query = make_many_query_filter(dimension_value_tuples)
    return query


def check_valid(sublist: list, indices: list) -> bool:
    if len(sublist) != len(indices):
        raise IndexError
    # Using this function for development and testing - as it's much easier than using the table lookup
    if 1 in sublist and 3 in sublist:
        return False
    return True

def generate_combinations_and_indices(lists: list, validate_function: Callable=check_valid) -> tuple[
    list[tuple[Any, ...]], list[tuple[int, ...]]]:
    all_combinations = []
    all_indices = []
    max_depth = len(lists)

    # Iterate over all possible subset sizes (1 to n)
    for size in range(1, max_depth + 1):
        # Generate all combinations of indices for the current subset size
        for subset_indices in combinations(range(max_depth), size):
            # Extract the lists corresponding to the current subset
            selected_lists = [lists[i] for i in subset_indices]
            # Compute the Cartesian product of the selected lists
            for combo in product(*selected_lists):
                # Check if the combination itself is valid
                if validate_function(combo, subset_indices):
                    all_combinations.append(combo)
                    all_indices.append(subset_indices)

    return all_combinations, all_indices

def format_valid_combos_with_tabulate(data, headers=("Condition", "Number", "Value")):
    table = []
    for entry in data:
        condition, number, value = entry
        table.append([condition, number, f"{value:.2f}"])

    output = tabulate(table, headers=headers, tablefmt="grid", stralign="left", numalign="right")
    return output


def format_all_combos_with_tabulate(data, headers=["Condition Combination"]):
    table = []
    for condition in data:
        table.append([condition])

    output = tabulate(table, headers=headers, tablefmt="grid", stralign="left", numalign="right")
    return output


