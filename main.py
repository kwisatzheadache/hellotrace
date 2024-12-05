import pandas as pd
import reader

SAMPLE_MIN = 3

if __name__ == "__main__":
    print("hello")

women = pd.read_csv(reader.women_csv)
household = pd.read_csv(reader.household_csv)
joined = reader.join_tables(women, household)
# Add mortality rate
joined = reader.add_mortality_rate(joined)

# Get all the distinct values for each dimension
distinct = reader.make_distinct_value_dict(joined)

# Remove the dimensions we don't care about.
dimensions = list(distinct.keys())
for dimension in dimensions:
    if dimension not in [x.value for x in reader.Dimension]:
        distinct.pop(dimension)

# Get the counts of all the distinct values for each dimension
distinct_rows = reader.make_rows_per_distinct_value_dict(joined, distinct)

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


# Example usage:
A = [1, 2]
B = [3, 4]
C = [5, 6]
D = [7, 8]
input_lists = [A, B, C, D]

combinations_output = reader.generate_combinations_with_validation(input_lists)
combos, indices = reader.generate_combinations_and_indices(input_lists)
for combo in combinations_output:
    print(combo)
