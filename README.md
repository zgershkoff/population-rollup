## Introduction
This takes population change data as provided by the census and rolls it up. It aggregates data from each Core Based Statistical Area (CBSA) and produces a CSV file listing the CBSA ID number along with the following:

* total number of census tracts,
* total population in 2000,
* total population in 2010 and
* average population percent change for census tracts in this Core Based Statistical Area

If a tract is empty in 2000 or 2010, I've made the choice to count it in the total number of tracts, and to treat the percent change as 0 for the purpose of averaging.

## Instructions
Python 3.8 is used for this application.

A file named `censustract-00-10.csv` should be placed in the `input` folder. Then the run script is called in bash with the command `./run.sh`. This creates `results.csv` in the `output` folder.
