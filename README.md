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


###confusionmatrix.py
Script for reading the ground truth for each sequence id and the participant assignment for each seqid

Format of ground truth file
Name = gsa.tsa
Format = tab separated text
Example:
#SequenceID	#TaxID	#Length
Contig_1	2	1000
The third column (length) is optional. If absent, each length will be set to 1.

Format of participant file
Name = participant.tsa
Format = tab separated text
Example:
#SequenceID	#TaxID
Contig_1	2

Format of output file
Name = result_all.tsa
Format = tab separated text
Example:
# 4 not assigned by participant
#tax_id	tp	fp	tn	fn
200666	1	0	52	0

If the -rank argument is added to the command, the program will read in the taxonomy
and summarize the results for each level of taxonomy.

Format of output file by rank
Name = result_rank.tsa
Format = tab separated text
Example:
# 4 not assigned by participant
#	tp	fp	tn	fn	tp	fp	tn	fn
species	6	2	466	3	6	2	62	2
total	196	30	2536	47	41	8	374	12

4 sequences were not assigned any tax id.
tp = true positive -- the participant reports a taxid for a sequence which matches the ground truth at that level of taxonomy.
fp = false positive -- the participant reports a taxid for a sequence which does not match the ground truth at that level of taxonomy 
AND the ground truth DOES report a result for that level of taxonomy.
For example if participant reports Escherichia coli and the ground truth for the sequence is Escherichia, participant gets tp for genus and no result for species.
tn = true negative -- participant does not report a particular taxid for a sequence and neither does ground truth.
fn = false negative -- participant does not report a particular taxid for a sequence but the ground truth does.

The first set of tp/fp/tn/fn are from using all levels of taxonomy, the second set is from evaluation only at the level of taxonomy indicated by the taxid.
If the participant reports E. coli correctly that will give a tp at all levels of taxonomy in the first set, but will only be recorded at species level in the second set.
