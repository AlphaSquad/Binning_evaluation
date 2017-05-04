# Binning_evaluation

###ncbi_taxonomy.py
Script for reading the NCBI taxonomy and creating a dump of the needed tax IDs and their lineage in the following format:

TaxID	lineage

where lineage consists of tab-separated triplets of the form

rank	taxID	scientific_name

Input:
* Output file path
* list of input file paths in CAMI binning format

Output:
* NCBI taxdump including all the taxids appearing at least once in any of the input binning files
