#!/usr/bin/env python
from sys import argv, stdout, stderr, stdin, exit

#program to read in ground truth file and participant file
#report confusion matrix as tsv
#TODO sort output, report per taxonomy rank

input_file1 = "gsa.tsv"
input_file2 = "participant.tsv"
output_file = "result.tsv"

tax_set = set()
seq_set = set()
#ground truth assignments
gsa_dict = dict()
length_dict = dict()
#participant assignments
partic_dict = dict()

#open ground truth file
#assign tax_id to seq_id in gsa_dict
with open(input_file1, "r") as f:
    for line in f:
        if len(line) > 1:
            if line[0] == '#':
                j = 0 #for later use?
            elif line[0] == '@':
                j = 0 #for later use?
            else:
                rows = line.strip().split("\t")
                if len(rows) > 1:
                    seq_id, tax_id = rows[:2]
                    #try to read a length column, if not present assigne length to 1
                    if len(rows) > 2:
                        try:
                            length = int(rows[2])
                        except ValueError:
                            length = 1
                    else:
                        length = 1
                    gsa_dict[seq_id] = tax_id
                    length_dict[seq_id] = length
                    seq_set.add(seq_id)
                    tax_set.add(tax_id)
f.close()

#open participant file
#assign tax_id to seq_id in partic_dict
with open(input_file2, "r") as f:
    for line in f:
        if len(line) > 1:
            if line[0] == '#':
                j = 0 #for later use?
            elif line[0] == '@':
                j = 0 #for later use?
            else:
                rows = line.strip().split("\t")
                if len(rows) > 1:
                    seq_id, tax_id = rows[:2]
                    partic_dict[seq_id] = tax_id
f.close()

#check for any Seq id not identified by participant
#assign the id to -1
num_not_assigned = 0
for seq_id in seq_set:
    if seq_id not in partic_dict:
        num_not_assigned += 1
        partic_dict[seq_id] = -1
        
print num_not_assigned, "not assigned by participant"

#totals
false_pos = 0
false_neg = 0
true_pos = 0
true_neg = 0

#per tax_id:  tp, fp, tn, fn 
stats = dict()

for tax_id in tax_set:
    stats[tax_id] = [0,0,0,0]

    #check if participant's assigned to this taxid is correct
    for seq_id in seq_set:
        if partic_dict[seq_id] == tax_id:
            if gsa_dict[seq_id] == tax_id:
                stats[tax_id][0] += length_dict[seq_id]
                true_pos += length_dict[seq_id]
            else:
                stats[tax_id][1] += length_dict[seq_id]
                false_pos += length_dict[seq_id]
        else:
            if gsa_dict[seq_id] == tax_id:
                stats[tax_id][3] += length_dict[seq_id]
                false_neg += length_dict[seq_id]
            else:
                stats[tax_id][2] += length_dict[seq_id]
                true_neg += length_dict[seq_id]

#output results
result_file = open(output_file, 'w')
line = str(num_not_assigned) + "not assigned by participant"
result_file.write(line)
line = "total true positive " + str(true_pos) + '\n'
result_file.write(line)
line = "total false positive " + str(false_pos) + '\n'
result_file.write(line)
line = "true negative " + str(true_neg) + '\n'
result_file.write(line)
line = "false negative " + str(false_neg) + '\n'
result_file.write(line)

line = "tax_id\ttp\tfp\ttn\tfn\n"
result_file.write(line)

for tax_id in tax_set:
    line = tax_id + "\t" + "\t".join(stats[taxid]) + "\n"
    result_file.write(line)
    
result_file.close()