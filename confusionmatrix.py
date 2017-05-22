#!/usr/bin/env python
import argparse


# program to read in ground truth file and participant file
# will read in taxonomy tree if -rank in command
# report confusion matrix as tsv
# TODO read length file


# open ground truth file
# assign tax_id to seq_id in gsa_dict
def read_ground_truth_file(ground_truth_file):
    tax_set = set()
    seq_set = set()
    # ground truth assignments
    gsa_dict = dict()
    length_dict = dict()
    with open(ground_truth_file, "r") as f:
        for line in f:
            if len(line) > 1:
                if line[0] == '#':
                    j = 0  # for later use?
                elif line[0] == '@':
                    j = 0  # for later use?
                else:
                    rows = line.strip().split("\t")
                    if len(rows) > 1:
                        seq_id, tax_id = rows[:2]
                        # try to read a length column, if not present assigne length to 1
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
    return gsa_dict, length_dict, seq_set, tax_set


# open participant file
# assign tax_id to seq_id in partic_dict
def read_participant_file(participant_file, tax_set):
    # participant assignments
    partic_dict = dict()
    with open(participant_file, "r") as f:
        for line in f:
            if len(line) > 1:
                if line[0] == '#':
                    j = 0  # for later use?
                elif line[0] == '@':
                    j = 0  # for later use?
                else:
                    rows = line.strip().split("\t")
                    if len(rows) > 1:
                        seq_id, tax_id = rows[:2]
                        partic_dict[seq_id] = tax_id
                        tax_set.add(tax_id)
    f.close()
    return partic_dict, tax_set


# open taxonomy file
def read_taxonomy_file(taxonomy_file):
    rank_set = dict()  # dictionary of sets of all taxonomy numbers associated with a tax_id
    rank_cat = dict()  # rank that this tax_id belongs to
    rank_idx = dict()  # index of rank in list
    rank_list = []  # ranks seen
    tax_set2 = set()  # including all levels of taxonomy
    rank_cat["none"] = 0
    rank_set["none"] = set()
    with open(taxonomy_file, "r") as f:
        for line in f:
            if len(line) > 1:
                if line[0] == '#':
                    j = 0  # for later use?
                elif line[0] == '@':
                    j = 0  # for later use?
                else:
                    rows = line.strip().split("\t")
                    if len(rows) > 1:
                        tax_id = rows[0]
                        rank_set[tax_id] = set()
                        for j in range(1, len(rows) - 2, 3):
                            rank = rows[j]
                            rank_id = rows[j + 1]
                            rank_name = rows[j + 2]  # not saved
                            if rank not in rank_idx:
                                rank_idx[rank] = len(rank_list)
                                rank_list.append(rank)
                            rank_cat[rank_id] = rank_idx[rank]
                            rank_set[tax_id].add(rank_id)
                            tax_set2.add(rank_id)
    f.close()
    return rank_set, rank_cat, rank_idx, rank_list, tax_set2


# check for any Seq id not identified by participant
# assign the id to -1
def check_participant_seq_ids(seq_set, partic_dict):
    num_not_assigned = 0
    for seq_id in seq_set:
        if seq_id not in partic_dict:
            num_not_assigned += 1
            partic_dict[seq_id] = "none"
    return partic_dict, num_not_assigned


def compute_matrix(result_file_all, tax_set, seq_set, length_dict, gsa_dict, partic_dict, num_not_assigned):
    result_file1 = open(result_file_all, 'w')
    line = "# " + str(num_not_assigned) + " not assigned by participant\n"
    result_file1.write(line)

    # total stats
    total_stats = [0, 0, 0, 0]
    # per tax_id:  tp, fp, tn, fn
    tax_stats = dict()

    for tax_id in tax_set:
        tax_stats[tax_id] = [0, 0, 0, 0]
        # check if participant's assignment to this taxid is correct
        for seq_id in seq_set:
            if partic_dict[seq_id] == tax_id:  # tp
                if gsa_dict[seq_id] == tax_id:
                    tax_stats[tax_id][0] += length_dict[seq_id]
                    total_stats[0] += length_dict[seq_id]
                else:  # fp
                    tax_stats[tax_id][1] += length_dict[seq_id]
                    total_stats[1] += length_dict[seq_id]
            else:
                if gsa_dict[seq_id] == tax_id:  # fn
                    tax_stats[tax_id][3] += length_dict[seq_id]
                    total_stats[3] += length_dict[seq_id]
                else:  # tn
                    tax_stats[tax_id][2] += length_dict[seq_id]
                    total_stats[2] += length_dict[seq_id]

    # output results
    line = "#tax_id\ttp\tfp\ttn\tfn\n"
    result_file1.write(line)
    for tax_id in tax_set:
        line = tax_id + "\t" + "\t".join(map(str, tax_stats[tax_id])) + "\n"
        result_file1.write(line)

    line = "total\t" + "\t".join(map(str, total_stats)) + "\n"
    result_file1.write(line)
    result_file1.close()


def compute_matrix_using_rankings(result_file_rank, tax_set, tax_set2, rank_list, rank_cat, rank_set, length_dict,
                                  seq_set, partic_dict, gsa_dict, num_not_assigned):
    tax_set = tax_set.union(tax_set2)
    result_file2 = open(result_file_rank, 'w')
    line = "# " + str(num_not_assigned) + " not assigned by participant\n"
    result_file2.write(line)
    line = "#\ttp\tfp\ttn\tfn\ttp\tfp\ttn\tfn\n"
    result_file2.write(line)

    # total stats
    total_rstats = [0, 0, 0, 0]
    total_tstats = [0, 0, 0, 0]
    # per tax_id:  tp, fp, tn, fn

    for rank_num in range(len(rank_list)):
        rank_stats = [0, 0, 0, 0]
        tax_stats = [0, 0, 0, 0]
        for tax_id in tax_set:
            if rank_cat[tax_id] == rank_num:
                # check if participant's assignment to this taxid is correct
                for seq_id in seq_set:
                    call_on_level = (rank_cat[partic_dict[seq_id]] == rank_num)
                    if tax_id in rank_set[partic_dict[seq_id]]:
                        if tax_id in rank_set[gsa_dict[seq_id]]:
                            rank_stats[0] += length_dict[seq_id]
                            total_rstats[0] += length_dict[seq_id]
                            if call_on_level:
                                tax_stats[0] += length_dict[seq_id]
                                total_tstats[0] += length_dict[seq_id]
                        else:  # fp
                            # determine if any call made in ground truth file
                            called = False
                            for tid in rank_set[gsa_dict[seq_id]]:
                                if rank_cat[tid] == rank_num:
                                    called = True
                            if called:
                                rank_stats[1] += length_dict[seq_id]
                                total_rstats[1] += length_dict[seq_id]
                                if call_on_level:
                                    tax_stats[1] += length_dict[seq_id]
                                    total_tstats[1] += length_dict[seq_id]
                    else:
                        if tax_id in rank_set[gsa_dict[seq_id]]:  # fn
                            rank_stats[3] += length_dict[seq_id]
                            total_rstats[3] += length_dict[seq_id]
                            if call_on_level:
                                tax_stats[3] += length_dict[seq_id]
                                total_tstats[3] += length_dict[seq_id]
                        else:  # tn
                            rank_stats[2] += length_dict[seq_id]
                            total_rstats[2] += length_dict[seq_id]
                            if call_on_level:
                                tax_stats[2] += length_dict[seq_id]
                                total_tstats[2] += length_dict[seq_id]
                                # output results
        line = rank_list[rank_num] + "\t" + "\t".join(map(str, rank_stats)) + "\t" + "\t".join(
            map(str, tax_stats)) + "\n"
        result_file2.write(line)

    line = "total\t" + "\t".join(map(str, total_rstats)) + "\t" + "\t".join(map(str, total_tstats)) + "\n"
    result_file2.write(line)
    result_file2.close()


def main(gold_standard_file,
         participant_file,
         taxdump_file,
         out_file,
         out_rank_file):
    gsa_dict, length_dict, seq_set, tax_set = read_ground_truth_file(gold_standard_file)
    partic_dict, tax_set = read_participant_file(participant_file, tax_set)

    if taxdump_file:
        rank_set, rank_cat, rank_idx, rank_list, tax_set2 = read_taxonomy_file(taxdump_file)

    partic_dict, num_not_assigned = check_participant_seq_ids(seq_set, partic_dict)
    compute_matrix(out_file, tax_set, seq_set, length_dict, gsa_dict, partic_dict, num_not_assigned)

    if out_rank_file:
        compute_matrix_using_rankings(out_rank_file, tax_set, tax_set2, rank_list, rank_cat, rank_set, length_dict,
                                      seq_set, partic_dict, gsa_dict, num_not_assigned)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gold_standard_file", help="gold standard - ground truth - file")
    parser.add_argument("-p", "--participant_file", help="participant file")
    parser.add_argument("-t", "--taxdump_file", help="NCBI taxdump file (optional)")
    parser.add_argument("-o", "--out_file", help="output confusion matrix file")
    parser.add_argument("-r", "--out_rank_file",
                        help="output confusion matrix file of taxonomic rankings (requires option -t)")
    args = parser.parse_args()
    if not args.gold_standard_file or not args.out_file or (args.out_rank_file and not args.taxdump_file):
        parser.print_help()
        parser.exit(1)

    main(args.gold_standard_file,
         args.participant_file,
         args.taxdump_file,
         args.out_file,
         args.out_rank_file)

    # example
    # main("Tests/minimal_gs.tsv",
    #      "Tests/minimal_participant.tsv",
    #      "Tests/minimal_taxonomy.tsv",
    #      "Tests/minimal_result_all.tsv",
    #      "Tests/minimal_result_rank.tsv")
