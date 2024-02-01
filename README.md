
# NanoPsiPy:
![github MALAT1](https://github.com/vetmohit89/NanoPsiPy/assets/110649675/8e7459df-fee9-48f7-a951-b5dca02bba84)

# Description
NanoPsiPy method identify and quantify transcriptome-wide pseudouridine (Î¨) modification using U-to-C basecalling "error" signature as a distinctive feature of Î¨ in Direct RNA sequencing data.

# Package versions
The version of softwares and packages for testing codes:

Python 3.11.0

guppy_basecaller: 6.4.2 ((C) Oxford Nanopore Technologies, Limited) (So far this software is only available when you are a customer of Oxford Nanopore Technologies)

minimap2: 2.18-r1015

samtools: 1.12 (Copyright (C) 2020 Genome Research Ltd.)

Python packages:

pickle: 4.0 (python3)

numpy: 1.24.0

re: 2.2.1

pandas: 2.1.0

# Download
You could download the package to your cluster by the following command.
```bash
git clone https://github.com/vetmohit89/NanoPsiPy
```
Then go to the folder with the ``setup.py`` file. And run

````pip install .````

Now you've installed the package. You could use it at any place of your account. If you are not clear about auy command, you could find help by the command

````NanoPsiPy_estimation -h````

and

````NanoPsiPy_comparison -h````


# Protocol
## Base call
It is advisable to basecall after completing the sequencing. If the data is not base called, use the following command to do the base call.
```bash
guppy_basecaller --input_path fast5 \
                 --recursive \
                 --save_path fastq \
                 --records_per_fastq 0 \
                 --flowcell FLO-MIN106 \
                 --kit SQK-RNA002 \
                 --qscore_filtering \
                 --min_qscore 7 \
                 --cpu_threads_per_caller 3 \
                 --num_callers 5
```
"Input_path" is the path of your raw data. "Save_path" is your output folder. "Flowcell" is the type of nanopore flowcell you use. "Kit" is the version of nanopore direct RNA sequencing kit you use. Customize "cpu_threads_per_caller" and "num_caller" according to the state of your own cluster. This step is computation intensive.


## A: Estimate U to C base calling "error" at each U site whole transcriptome wide in individual samples:

## A : NanoPsiPy_estimation

To use NanoPsiPy_estimation, run the following command: 

```bash
NanoPsiPy_estimation -i fastq_files_directory/ -r reference_file -o output_file_name.csv -s Specify the sample type (control or treatment)
```

1. The first argument is the input fastq path. The fastq files must be directly in this folder. 
2. The second argument is the genome or transcriptome reference file.
3. The third argument is the name of the output file
4. The fourth argument specifies the type of sample (Either control or treatment).

#

**Here is the explanation of each individual script function:**

## A (i) Alignment and pile up

The output after align.py, is a folder `alignment` with two subfolders `plus_strand` and `minus_strand`. The two subfolders contains data of reads aligned to forward and reverse strands respectively. 

If you would like to test the package on your device. Please copy the `example` folder, which contains MALAT1 IVT oligo RNA treated with mutant PUS7 and human PUS7 enzyme and its reference sequence locally. Then use the above code to have positional data of each Uridine base pair. 

Here is the output directory after align.py:

```bash
$ ls alignment/plus_strand/
collect.bam    collect_pile.txt  collect.sorted.bam  collect.filtered.sorted.bam reference.fa.fai
collect.fastq  collect.sam       reference.fa
```
If you align your transcriptome sample to the genome reference, then you'll likely to have both `plus_strand` and `minus_strand` folder.

## A (ii) Process the mpileup data

The process scirpt will procees collect.filtered.sorted.bam. Due to the design of samtools, in the mpileup files, the spliced reads will be filled a ">" or "<" in the jumped regions and the coverage and the quality score are affected. The data points with ">" or "<" are not real bases. Run the following script to remove the gap sections in the mpileup file. This step is computation intensive.

```bash
In your `plus_strand` and `minus_strand` folders you'll find a new file named `collect_pile_no_intron.txt`.
```

## A (iii) Feature extraction at each U site
Then extract features of all U sites. In order to remove poor quality reads accouting for U to C basecalling error, there is a threshold for a U site which is â‰¥9 reads. Only U sites with â‰¥9 reads will be processed for following analysis. This step is computation intensive.

The output file is `features.csv` in the `alignment` folder. This file contains information from reads aligned to both forward and reverse strands.


## A (iv) PSI estimation
To estimate the psU level of all the U sites from `features.csv`, The extraction process involves reading the input feature.CSV file, parsing specific columns such as "ID," "position," "base_type," "coverage," and "misC". Subsequently, the script calculates values for "C_reads" and "U_reads" based on the extracted "coverage" and "misC" columns.

**```Note: Run the same above code for treatment (knockdown or knockout) sample in a separate folder.```**
 
## B. PSI comparison between two samples: To compare between two conditions, execute the following command to estimate the significant Î¨ at each U site:
```bash
NanoPsiPy_comparison -c ./control_file.csv -t ./treatment_file.csv -o output_folder -d reference_data_type (genome or transcriptome)
```
1. The first argument is the control sample file generated after running **NanoPsiPy_estimation**
2. The second argument is treatment sample file generated after running **NanoPsiPy_estimation**
3. The third argument is the output folder directory.
4. The fourth argument specifies the type of reference file used for running **NanoPsiPy_estimation** (Either genome or transcriptome).

#

**Here is the explanation of each individual script function:**

## B (i) Merge the both control and treatment file using:

```bash
merge_script.py: 
```
This script create a merge dataset for each Uridine found common between control and treatment sample. The updated dataset is saved to a new CSV file ('control_vs_treatment.csv').

## B (ii). Estimating significant PSI sites at each position:

```bash
chi_sqare.py
```
This Python script conducts a statistical analysis by performing a chi-square test to compare the ratios of U-to-C reads between two conditions. The script calculates p-values for each row using a chi-square test on a contingency table. The updated dataset is saved to a new CSV file ('control_vs_treatment_result.csv').

#

## Acknowledgements:
NanoPsiPy tool workflow was built around Nanopore_psu tool available at (https://github.com/sihaohuanguc/Nanopore_psU/)
