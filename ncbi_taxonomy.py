#!/usr/bin/python

from ete2 import NCBITaxa

def read_binners(filenames, taxonomy):
	tax_dict = {}
	for filename in filenames:
		with open(filename, 'r') as binner:
			for line in binner:
				if not line.strip() or line.startswith('#') or line.startswith('@'):
					continue # header
				linesplit = line.strip().split('\t')
				sequenceid, taxid = linesplit[:2]
				if taxid not in tax_dict:
					tax_dict[taxid] = taxonomy.get_lineage(taxid)
	return tax_dict

def write_taxonomy(tax_dict, out_file, taxonomy):
	with open(out_file, 'wb') as out:
		for taxid in tax_dict:
			toWrite = taxid
			lineage = tax_dict[taxid]
			for rank_id in lineage:
				rank = taxonomy.get_rank([rank_id])[rank_id]
				if rank != "no rank":
					toWrite += "\t%s\t%s\t%s" % (rank, rank_id, taxonomy.get_taxid_translator([rank_id])[rank_id])
			toWrite += "\n"
			out.write(toWrite)

def main(out_file, filenames):
	taxonomy = NCBITaxa()
	tax_dict = read_binners(filenames, taxonomy)
	write_taxonomy(tax_dict, out_file, taxonomy)
