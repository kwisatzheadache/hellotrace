from enum import Enum
from itertools import combinations, product
from typing import Any

import pandas as pd
from pandas import DataFrame


class Dimension(Enum):
    AGE_IN_5_YEAR_GROUPS = "Age in 5-year groups"
    TYPE_OF_PLACE_OF_RESIDENCE = "Type of place of residence"
    NUMBER_OF_HOUSEHOLD_MEMBERS = "Number of household members"
    SOURCE_OF_DRINKING_WATER = "Source of drinking water"
    TIME_TO_GET_TO_WATER_SOURCE_MINUTES = "Time to get to water source (minutes)"
    TYPE_OF_TOILET_FACILITY = "Type of toilet facility"
    HAS_ELECTRICITY = "Has electricity"
    HAS_RADIO = "Has radio"
    AGE_OF_HEAD_OF_HOUSEHOLD = "Age of head of household"

class KeyDimension(Enum):
    HOUSEHOLD_NUMBER = "Household number"
    CLUSTER_NUMBER = "Cluster number"
    TOTAL_CHILDREN_EVER_BORN = "Total children ever born"
    SONS_WHO_HAVE_DIED = "Sons who have died"
    DAUGHTERS_WHO_HAVE_DIED = "Daughters who have died"

household_csv = "./data/household.csv"
women_csv = "./data/women.csv"

"""
1. Read the files
   Get the headers
2. Join the files on Cluster Number and HouseHold Number
3. Load it into a dataframe
4. Make table of distinct values for each dimension
5. Make table with number of rows per dimension
6. Make algorithm to generate all combinations of dimensions:

"""

def join_tables(household: DataFrame, women: DataFrame)->DataFrame:
    """ Join on household.cluster_number and women.household_number"""
    join_columns = [
        KeyDimension.CLUSTER_NUMBER.value,
        KeyDimension.HOUSEHOLD_NUMBER.value
    ]

    joined_df = pd.merge(
        household,
        women,
        how='inner',
        on=join_columns,
        suffixes=('_household', '_women')  # To differentiate columns with the same name
    )

    return joined_df

def make_distinct_value_dict(table: DataFrame) -> dict:
    distinct_value_dict = {}
    for column in table.columns:
        # Get unique values and convert them to a list
        distinct_values = table[column].dropna().unique().tolist()
        distinct_value_dict[column] = distinct_values
    return distinct_value_dict

def make_rows_per_distinct_value_dict(table: DataFrame, distinct_value_dict: dict) -> dict:
    rows_per_distinct_value = {}
    for column, distinct_values in distinct_value_dict.items():
        value_counts = table[column].value_counts(dropna=True).to_dict()
        rows_per_distinct_value[column] = value_counts
    return rows_per_distinct_value

def build_query_string(dimension_value_tuples: list[tuple]):
    """
    tuple is (dimension, value)
    """
    query = ""
    for item in dimension_value_tuples:
        if query != "":
            query += " & "
        substring = f"{item[0]}=={item[1]} "
        query += substring
    return query

def get_count_with_combination(table: DataFrame, dimension_value_tuples: list[tuple]) -> dict:
    build_query_string(dimension_value_tuples)
    print(build_query_string(dimension_value_tuples))
    return dict()


def get_value_type(value: Any) -> tuple:
    if isinstance(value, int):
        return "int", value
    if isinstance(value, float):
        return "float", value
    return "str", value



def make_single_query_filter(dimension_value_tuple: tuple) -> str:
    value = dimension_value_tuple[1]
    value_type, value = get_value_type(value)
    if value_type == "str":
        query = f"`{dimension_value_tuple[0]}` == \'{value}\'"
    else:
        query = f"`{dimension_value_tuple[0]}` == {value}"
    return query

def make_many_query_filter(dimension_value_tuples: list[tuple]) -> str:
    query = ""
    for item in dimension_value_tuples:
        if query != "":
            query += " & "
        query += make_single_query_filter(item)
    return query


def add_mortality_rate(table: DataFrame) -> DataFrame:
    numerator = table[KeyDimension.SONS_WHO_HAVE_DIED.value] + table[KeyDimension.DAUGHTERS_WHO_HAVE_DIED.value]
    denominator = table[KeyDimension.TOTAL_CHILDREN_EVER_BORN.value]

    mortality_rate = numerator / denominator
    table = table.copy()
    table["Mortality Rate"] = mortality_rate
    return table


def get_dimension_combinations(dim_dict: dict, depth: int) -> list:
    dimensions = list(dim_dict.keys())
    dim_combinations = combinations(dimensions, depth)

    all_paired_combinations = []
    for dim_combo in dim_combinations:
        # Get the list of values for each dimension in the combination
        values_lists = [dim_dict[dim] for dim in dim_combo]

        # Generate the Cartesian product of the values
        for values in product(*values_lists):
            # Pair each dimension with its corresponding value
            paired = tuple(zip(dim_combo, values))
            all_paired_combinations.append(paired)

    return all_paired_combinations

TEST_DIMS = [
    [1,2,3,4,5],
    ['a','b','c','d','e'],
    [6,7,8,9,10],
    ['x','y','z']
    ]

def testit(dim_matrix=TEST_DIMS, level:int=1):
    a = dim_matrix[0]
    b = dim_matrix[1]
    c = dim_matrix[2]
    d = dim_matrix[3]

def validate_with_table(table: DataFrame, sublist: list, indices: list) -> bool:
    return True

SAMPLE_DF = DataFrame()

def check_valid(sublist: list, is_test: bool=True, table: DataFrame=SAMPLE_DF) -> bool:
    # For demonstration, let's say a combination is invalid if it contains both 1 and 3
    if is_test:
        if 1 in sublist and 3 in sublist:
            return False
        return True
    else:
        validate_with_table()



def generate_combinations_with_validation(lists):
    all_combinations = []
    n = len(lists)

    # Iterate over all possible subset sizes (1 to n)
    for size in range(1, n + 1):
        # Generate all combinations of indices for the current subset size
        for subset_indices in combinations(range(n), size):
            # Extract the lists corresponding to the current subset
            selected_lists = [lists[i] for i in subset_indices]
            # Compute the Cartesian product of the selected lists
            for combo in product(*selected_lists):
                # Check if the combination is valid
                if check_valid(combo):
                    all_combinations.append(combo)
                else:
                    # If invalid, skip adding and potentially skip supersets containing this combination
                    # Note: Implementing the skipping of supersets requires additional logic
                    pass  # Placeholder for any additional handling if needed

    return all_combinations


def generate_combinations_and_indices(lists: list, table: DataFrame=SAMPLE_DF) -> tuple[list]:
    all_combinations = []
    all_indices = []
    invalid_subsets = set()
    max_depth = len(lists)

    # Iterate over all possible subset sizes (1 to n)
    for size in range(1, max_depth + 1):
        # Generate all combinations of indices for the current subset size
        for subset_indices in combinations(range(max_depth), size):
            # Extract the lists corresponding to the current subset
            selected_lists = [lists[i] for i in subset_indices]
            # Compute the Cartesian product of the selected lists
            for combo in product(*selected_lists):
                # Check if this combination contains any invalid subset
                contains_invalid = False
                for invalid in invalid_subsets:
                    if set(invalid).issubset(set(combo)):
                        contains_invalid = True
                        break
                if contains_invalid:
                    continue  # Skip this combination as it contains an invalid subset

                # Check if the combination itself is valid
                if check_valid(combo):
                    all_combinations.append(combo)
                    all_indices.append(subset_indices)
                else:
                    # Add this combination as an invalid subset to prune future supersets
                    invalid_subsets.add(combo)

    return (all_combinations, all_indices)

