# Trace Exercise

Suppose we have a dataset with N rows and the following columns:

- `subject_id` - every row has a unique value
- `dimension001`, `dimension002`, ..., `dimensionX` - each dimensional column has between 1 to V unique values, where V << N
- `measure1` and `measure2` - columns that'll be used to calculate the ratio metric

Define the ratio metric as:

$$
\frac{\text{sum}(\text{measure1})}{\text{sum}(\text{measure2})}

$$

Our goal is to calculate the ratio metric for different combinations of dimensional values. Your program should be written to work generically on any dataset with a certain input structure. To help make the problem more concrete, the program should work on the specific problem and dataset in the "Real-world application" written below.

## Problem 1

Compute the ratio metric for **every possible combination** of values in the first K dimensions: `dimension001` ,`dimension002` … `dimensionK` . "Every possible combination" means all combinations *up to* the total number of dimensions (in this case, K). So, that would mean 1, 2, 3… K dimensional cuts of the metric. 

## Problem 2

As more dimensions are added, say we have a 50 dimensional data set, exhaustive computation of the ratio metric for every combination of dimensional values can become prohibitive - 50-dim, 49-dim, 48-dim, 47-dim combos... etc. Develop an algorithm that only computes the ratio metric for a narrower subset of combinations that *each* meet a minimum threshold of rows.

## Real-world application: under-5 mortality

In 2015, the United Nations set the Sustainable Development Goals to be the "blueprint to achieve a better and more sustainable future for all by 2030". One goal is to "ensure healthy lives and promote well-being for all at all ages" and under-5 mortality is a key metric to track progress towards this goal. Developing countries often do not have the means and funds to track every birth and death in a registry, so they rely on surveys of women to get a proxy metric for under-5 mortality: $\text{CD}/\text{CEB} = (\text{total children died})/(\text{total children ever born})$. This metric is further split by cohorts of women's age, where the younger cohort provides a more recent estimate of under-5 mortality. Our goal is to estimate under-5 mortality and understand how different drivers affect the metric over time.

You’ll find 2 datasets [here](https://drive.google.com/drive/u/3/folders/1P7muXfDYPBOSKlaNUUjmoriec6ticE2H):  

- [`women.csv`](https://drive.google.com/file/d/11A1IkhLd4GB3Xgr6R5p3KefTYFUjRGYY/view?usp=sharing) contains information about women.
- [`household.csv`](https://drive.google.com/file/d/1uujlH3AAdLU_Z0o1ufMmpYWKCMDacoiE/view?usp=sharing) contains information about the households that the women come from.

A woman's household can be found using the `Cluster number` and `Household number` columns.

Compute $\text{CD}/\text{CEB}$, defined as: 

$$
\frac{\text{sum}(\text{Sons who have died + Daughters who have died)}}{\text{sum}(\text{Total children ever born})}

$$

for the following combination of dimensions:

- `Age in 5-year groups` (woman's age cohort)
- `Type of place of residence`
- `Number of household members`
- `Source of drinking water`
- `Time to get to water source (minutes)`
- `Type of toilet facility`
- `Has electricity`
- `Has radio`
- `Age of head of household`

## Notes

- We'll be reviewing this exercise based on your engineering abilities, *not* your data science or script writing abilities. To that end, consider how your code would generalize to any arbitrary dataset in the specified format.
- We expect this to take 3-6 hours but there is no explicit time limit. If at any point, this is taking more time than you can afford, please write or present the pseudo-code for the parts you couldn't finish.