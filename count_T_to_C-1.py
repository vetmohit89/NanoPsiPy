#!/usr/bin/env python3
import glob
import os

def process_file(input_file, prefix):
    output_file = f"{prefix}T_C_with_percent.STATS"
    # Get column indices from header
    with open(input_file, 'r') as f:
        header = f.readline().strip().split()
        chr_idx = header.index("chr")
        pos_idx = header.index("pos")
        ref_idx = header.index("ref_nuc")
        cov_idx = header.index("coverage")
        t_idx = header.index("T")
        c_idx = header.index("C")

    # Write filtered results with C%
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Write new header with prefix
        outfile.write("\t".join([
            "chr", "pos", "ref_nuc",
            f"{prefix}coverage",
            f"{prefix}T",
            f"{prefix}C",
            f"{prefix}C%"
        ]) + "\n")
        
        for line in infile:
            if line.startswith("chr"):  # Skip original header
                continue
            parts = line.strip().split()
            try:
                ref_nuc = parts[ref_idx]
                coverage = int(parts[cov_idx])
                t_count = parts[t_idx]
                c_count = parts[c_idx]
                c = int(c_count)
                if ref_nuc == 'T' and coverage > 20:
                    c_percent = (c / coverage) * 100
                    new_line = "\t".join([
                        parts[chr_idx],
                        parts[pos_idx],
                        ref_nuc,
                        parts[cov_idx],
                        t_count,
                        c_count,
                        f"{c_percent:.2f}"
                    ])
                    outfile.write(new_line + "\n")
            except (ValueError, IndexError):
                continue
    print(f"Filtered data with C percentages written to {output_file}")

def main():
    stats_files = sorted(glob.glob("*.STATS"))
    for stats_file in stats_files:
        # Use everything before .STATS as the prefix, plus an underscore
        prefix = os.path.splitext(stats_file)[0] + "_"
        process_file(stats_file, prefix)

if __name__ == "__main__":
    main()
