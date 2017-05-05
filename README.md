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
#tax_id	tp	fp	tn	fn
200666	1	0	52	0

If the -rank argument is added to the command, the program will read in the taxonomy
and summarize the results for each level of taxonomy.

Format of output file by rank
Name = result_rank.tsa
Format = tab separated text
Example:
#	tp	fp	tn	fn
species	6	2	466	3
#	tp	fp	tn	fn
total	196	30	2536	47

tp = true positive -- the participant reports a taxid for a sequence which matches the ground truth at that level of taxonomy.
fp = false positive -- the participant reports a taxid for a sequence which does not match the ground truth at that level of taxonomy 
AND the ground truth DOES report a result for that level of taxonomy.
For example if participant reports Escherichia coli and the ground truth for the sequence is Escherichia, participant gets tp for genus and no result for species.
tn = true negative -- participant does not report a particular taxid for a sequence and neither does ground truth.
fn = false negative -- participant does not report a particular taxid for a sequence but the ground truth does.
