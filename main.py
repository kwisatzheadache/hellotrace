import csv

import pandas as pd
from pandas import DataFrame
import utils
from enum import Enum

"""
1. Read the files
2. Join the files on Cluster Number and HouseHold Number
3. Load it into a dataframe
4. Make table of distinct values for each dimension
5. Make table with number of rows per dimension
6. Make algorithm to generate all combinations of dimensions:

"""
SAMPLE_MIN = 2000

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

HOUSEHOLD_CSV = "./data/household.csv"
WOMEN_CSV = "./data/women.csv"


def join_tables(household: DataFrame, women: DataFrame)->DataFrame:
    """ Join on cluster_number and household_number"""
    join_columns = [
        KeyDimension.CLUSTER_NUMBER.value,
        KeyDimension.HOUSEHOLD_NUMBER.value
    ]

    joined_df = pd.merge(
        household,
        women,
        how='left',
        left_on=join_columns,
        right_on=join_columns,
    )

    return joined_df

def add_mortality_rate(table: DataFrame) -> DataFrame:
    numerator = table[KeyDimension.SONS_WHO_HAVE_DIED.value] + table[KeyDimension.DAUGHTERS_WHO_HAVE_DIED.value]
    denominator = table[KeyDimension.TOTAL_CHILDREN_EVER_BORN.value]

    mortality_rate = numerator / denominator
    table = table.copy()
    table["Mortality Rate"] = mortality_rate
    return table

def validate_against_table(subset_list: list, indices: list):
    query = utils.build_query_from_subset_list_and_indices(subset_list, indices, DIMENSION_INDEX_MAP)
    result = JOINED.query(query)
    size = result.shape[0]
    if size >= SAMPLE_MIN:
        mortality_rate = float(round(result["Mortality Rate"].mean(),2))
        RESULTS.append((query, size, mortality_rate))
        return True
    else: return False

def validate_always_true(subset_list: list, indices: list):
    return True


if __name__ == "__main__":
    print("Reading Files")

    # Read the tables and join them
    women = pd.read_csv(WOMEN_CSV)
    household = pd.read_csv(HOUSEHOLD_CSV)
    JOINED = join_tables(women, household)
    # Add mortality rate
    JOINED = add_mortality_rate(JOINED)

    # Get all the distinct values for each dimension
    distinct = utils.make_distinct_value_dict(JOINED)

    # Remove the dimensions we don't care about.
    dimensions = list(distinct.keys())
    for dimension in dimensions:
        if dimension not in [x.value for x in Dimension]:
            distinct.pop(dimension)

    # Get the counts of all the distinct values for each dimension
    distinct_rows = utils.make_rows_per_distinct_value_dict(JOINED, distinct)

    # Trim dimensions that don't have enough rows per distinct value
    dimensions = list(distinct_rows.keys())
    trimmed_distinct = {}
    for dimension in dimensions:
        trimmed_distinct[dimension] = []
        values = list(distinct_rows[dimension].keys())
        for value in values:
            if distinct_rows[dimension][value] < SAMPLE_MIN:
                distinct_rows[dimension].pop(value)
            else:
                trimmed_distinct[dimension].append(value)

    # Now that we've trimmed down our starting set, let's use the algorithm.
    # If we didn't want to trim it down beforehand, we could just use the initial distinct_rows dictionary
    DIMENSION_INDEX_MAP = {}
    dimension_distinct_value_lists = []
    for ind, item in enumerate(trimmed_distinct.keys()):
        DIMENSION_INDEX_MAP[ind] = item
        dimension_distinct_value_lists.append(trimmed_distinct[item])

    # PROBLEM 1
    # Compute all combinations for problem 1. Note, we've already trimmed out set to exclude small sample sizes. For full results - use SAMPLE_MIN = 1
    all_combos, all_indices = utils.generate_combinations_and_indices(dimension_distinct_value_lists, validate_function=validate_always_true)
    ALL_RESULTS = []
    for i in range(len(all_combos)):
        query = utils.build_query_from_subset_list_and_indices(all_combos[i], all_indices[i], DIMENSION_INDEX_MAP)
        ALL_RESULTS.append(query)
    output = utils.format_all_combos_with_tabulate(ALL_RESULTS)
    print(output)
    outfile = f"./output/all_combos_bases_on_sample_min_{SAMPLE_MIN}.txt"
    with open(outfile, 'w', newline='') as outfile:
        outfile.write(output)


    # PROBLEM 2
    # Compute only combinations that yield rows > SAMPLE_MIN
    RESULTS = []
    combos, indices = utils.generate_combinations_and_indices(dimension_distinct_value_lists, validate_function=validate_against_table)
    headers = [f"Conditions with sample size over {SAMPLE_MIN}", "Sample Size", "Mortality Rate"]
    output = utils.format_valid_combos_with_tabulate(RESULTS, headers=headers)
    print(output)
    # Write to output file
    outfile = f"./output/valid_combinations_sample_min{SAMPLE_MIN}.txt"
    with open(outfile, 'w', newline='') as outfile:
        outfile.write(output)
