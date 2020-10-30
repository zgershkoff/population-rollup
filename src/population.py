#!/usr/bin/python

import sys
from bisect import bisect_left
from csv import reader, DictWriter
from collections import defaultdict

def calculate_moving_average(old_avg, num, new_item):
    """
    Returns the updated average, based on how many values were in the old one

    INPUT:
      - old_avg - a number
      - num - positive integer saying how many numbers contributed to the old
        average
      - new_item - a number

    OUTPUT:
      A float
    """
    return (old_avg * num + new_item) / (num + 1)

def parse_data(inFile):
    """
    Takes an input file and returns data structures more useful for the report

    INPUT:
      - inFile - a string specifying the file path

    OUTPUT:
      A sorted list of area codes, and a dictionary of data. The keys of the
      dictionary are the area codes, and the items are dictionaries with fields
      ['CBSA', 'name', 'tracts', 'pop00', 'pop10', 'change'].
    """
    with open(inFile, 'r') as f:
        csv_file = reader(f)
        next(csv_file) # discard the headers
        CBSAs, data = _parse_data(csv_file)

    return CBSAs, data

def _parse_data(csv_file):
    """
    Helper method for parse_data()

    INPUT:
      - csv_file - an iterator with the interface that each item contains a list
      corresponding to the 20 entries in each row of the census files

    OUTPUT:
      A sorted list of area codes, and a dictionary of data. The keys of the
      dictionary are the area codes, and the items are dictionaries with fields
      ['CBSA', 'name', 'tracts', 'pop00', 'pop10', 'change'].
    """
    # maintain a sorted list of CBSAs with bisect
    CBSAs = []
    # use dictionaries to track attributes of CBSAs
    data = {}

    for line in csv_file:
        # important indices:
        # 7: CBSA ID number
        # 8: CBSA name
        # 12: pop_2000
        # 14: pop_2010
        # 17: percentage change

        # skip the tract if it's not in a CBSA
        if not line[7]:
            continue
        CBSA = int(line[7])
        name = line[8]
        pop00 = int(line[12].replace(',', ''))
        pop10 = int(line[14].replace(',', ''))

        # I would get better precision calculating this change myself,
        # but reading it from the input file is faster.
        # If there is no population, let's count the tract but treat
        # the change as 0
        if pop00 and pop10:
            percent_change = float(line[17].replace(',', ''))
        else:
            percent_change = 0

        idx = bisect_left(CBSAs, CBSA)
        # if the CBSA hasn't been seen already:
        if idx >= len(CBSAs) or CBSAs[idx] != CBSA:
            CBSAs.insert(idx, CBSA)
            # initialize a dict for the CBSA in data
            data[CBSA] = {"tracts": 0, "pop00": 0, "pop10": 0}
            data[CBSA]["name"] = name
            data[CBSA]["change"] = percent_change
        else:
            # this should be rounded, but we'll save rounding for the end
            data[CBSA]["change"] = calculate_moving_average(
                data[CBSA]["change"], data[CBSA]["tracts"], percent_change)

        data[CBSA]["tracts"] += 1
        data[CBSA]["pop00"] += pop00
        data[CBSA]["pop10"] += pop10

    return CBSAs, data

def generate_report(outFile, CBSAs, data):
    """
    Creates a .csv file with the required statistics

    INPUT:
      - outFile - a string indicating the file path
      - CBSAs - a sorted list of CBSA area codes
      - data - a dictionary of dictionaries as generated in parse_data()

    OUTPUT:
      None. (Writes to a .csv file)
    """
    with open(outFile, 'w', newline='') as f:
        fieldnames = ['CBSA', 'name', 'tracts', 'pop00', 'pop10', 'change']
        CBSAwriter = DictWriter(f, fieldnames=fieldnames)
        for item in CBSAs:
            CBSA_data = data[item]
            CBSA_data["CBSA"] = item
            CBSA_data["change"] = round(CBSA_data["change"], 2)
            CBSAwriter.writerow(CBSA_data)


if __name__ == "__main__":
    _, inFile, outFile = sys.argv
    CBSAs, data = parse_data(inFile)
    generate_report(outFile, CBSAs, data)
