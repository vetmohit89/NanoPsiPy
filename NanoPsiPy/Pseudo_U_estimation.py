#!/usr/bin/env python
import os
import csv
import re
import numpy
from collections import Counter

def process_strand_file(input_file, outcsv):
    for line in input_file:
        site = line.strip("\n").split("\t")
        if site[2] == "T" and int(site[3]) > 8:
            out_line = site[:4]
            pattern = re.compile("\\^.")
            alignment = re.sub(pattern, "", site[4])

            pattern2 = re.compile("\\+[0-9]+[ATCGNatcgn]+")
            result2 = pattern2.findall(alignment)
            num_of_insertion = 0
            len_of_insertion = 0
            for item in result2:
                num_of_insertion += 1
                num_pattern = re.compile("[0-9]+")
                num_result = num_pattern.findall(item)[0]
                len_of_insertion += int(num_result)
                char_pattern = re.compile("[ATCGNatcgn]+")
                char_result = char_pattern.findall(item)[0]
                substr = "+" + num_result + char_result[0: int(num_result)]
                alignment = alignment.replace(substr, "", 1)
            out_line.append(float(num_of_insertion) / int(site[3]))
            out_line.append(float(len_of_insertion) / int(site[3]))

            pattern3 = re.compile("\\-[0-9]+[ATCGNatcgn]+")
            result3 = pattern3.findall(alignment)
            num_of_deletion = 0
            len_of_deletion = 0
            for item in result3:
                num_of_deletion += 1
                num_pattern = re.compile("[0-9]+")
                num_result = num_pattern.findall(item)[0]
                len_of_deletion += int(num_result)
                char_pattern = re.compile("[ATCGNatcgn]+")
                char_result = char_pattern.findall(item)[0]
                substr = "-" + num_result + char_result[0: int(num_result)]
                alignment = alignment.replace(substr, "", 1)
            out_line.append(float(num_of_deletion) / int(site[3]))
            out_line.append(float(len_of_deletion) / int(site[3]))

            pattern4 = re.compile("\\*")
            result4 = pattern4.findall(alignment)
            out_line.append(float(len(result4)) / int(site[3]))

            pattern5 = re.compile("[ATCGatcg]")
            result5 = pattern5.findall(alignment)
            out_line.append(float(len(result5)) / int(site[3]))
            find_T = re.compile("[Tt]").findall(alignment)
            out_line.append(float(len(find_T)) / int(site[3]))
            find_A = re.compile("[Aa]").findall(alignment)
            out_line.append(float(len(find_A)) / int(site[3]))
            find_C = re.compile("[Cc]").findall(alignment)
            out_line.append(float(len(find_C)) / int(site[3]))
            find_G = re.compile("[Gg]").findall(alignment)
            out_line.append(float(len(find_G)) / int(site[3]))

            all_qual = []
            for item in site[5]:
                all_qual.append(ord(item) - 33)
            out_line.append(numpy.mean(all_qual))
            out_line.append(numpy.std(all_qual))
            out_line.append(float(Counter(all_qual)[0]) / int(site[3]))

            outcsv.writerow(out_line)

def ex_fe():
    working_path = os.getcwd()
    in_folder = os.path.join(working_path, "alignment")
    plus_folder = os.path.join(in_folder, "plus_strand")
    minus_folder = os.path.join(in_folder, "minus_strand")
    out_file = os.path.join(in_folder, "features.csv")

    with open(out_file, "w+", newline="") as output:
        outcsv = csv.writer(output)

        columns = [
            "ID",
            "position",
            "base_type",
            "coverage",
            "ins",
            "ins_len",
            "del",
            "del_len",
            "fuzzy",
            "mis",
            "misT",
            "misA",
            "misC",
            "misG",
            "base_qual_mean",
            "base_qual_STD",
            "base_qual_count_0",
        ]
        outcsv.writerow(columns)

        plus_file = os.path.join(plus_folder, "collect_pile_no_intron.txt")
        with open(plus_file, "r") as input_file:
            process_strand_file(input_file, outcsv)

        # Continue processing for minus_strand folder
        if os.path.exists(minus_folder):
            minus_file = os.path.join(minus_folder, "collect_pile_no_intron.txt")
            with open(minus_file, "r") as input_file:
                process_strand_file(input_file, outcsv)



