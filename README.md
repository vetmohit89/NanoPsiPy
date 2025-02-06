
# NanoPsiPy: Introducing a Tool for Estimating Pseudouridine Levels Through U-to-C Base-Calling Error Analysis in Direct RNA Nanopore Sequencing Data.

# Description
NanoPsiPy method identify and semi-quantify transcriptome-wide pseudouridine (Ψ) modification using U-to-C basecalling "error" signature as a distinctive feature of Ψ in Direct RNA sequencing data.

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

Now you've installed the package. You could use it at any place of your account. If you are not clear about any command, you could find help by the command

````NanoPsiPy_estimation -h````

and

````NanoPsiPy_comparison -h````


# Protocol
## Base call
It is advisable to basecall after completing the sequencing. If the data is not base called, use the following command to do the base call.
```bash
guppy_basecaller rna002_70bps_hac@v3/ *.pod5 > *.bam
```
"*pod5" is the input raw data. "rna002_70bps_hac@v3" is the base-calling model. ".bam" is output bam file.

```bash
bedtools bamtofastq -i <BAM> -fq <FASTQ>
```

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

 
## B. PSI comparison between two samples: To compare between two conditions, execute the following command to estimate the significant Ψ at each U site in specific kmers:
```bash
NanoPsiPy_comparison -c ./control_file.csv -t ./treatment_file.csv -o output_folder -d reference_data_type (genome or transcriptome) -k kmers.txt
```
1. The first argument is the control sample file generated after running **NanoPsiPy_estimation**
2. The second argument is treatment sample file generated after running **NanoPsiPy_estimation**
3. The third argument is the output folder directory.
4. The fourth argument specifies the type of reference file used for running **NanoPsiPy_estimation** (Either genome or transcriptome).
5. The fifth argument specifies the input kmers for filtering the data


## Acknowledgements:
NanoPsiPy tool workflow was built around Nanopore_psu tool available at (https://github.com/sihaohuanguc/Nanopore_psU/)
