import statsmodels
from statsmodels.stats.multitest import multipletests
from scipy.stats import hypergeom
from a1 import GMT
import csv
import json
import math

def hg(ref_set, user_set, ref_genesets):
    """
    computes hypergeometric value between 2 sets.
    :param ref_set_name: set of genes
    :param user_set: set of genes
    :param ref_genesets: default dict of all genesets in ref file
    :return: pval: the two-tailed p value between the 2 sets of genes
            ref_set_name, user_set
    """
    m = len(ref_set)
    k = len(user_set)
    x = len(user_set.intersection(ref_set))
    M = 0
    for val_set in ref_genesets.values():
        M += len(val_set)
    pval = hypergeom.sf(x - 1, M, k, m)

    #use negative log here to indicate logarithmic significance
    return -(math.log(pval))
    #return pval


def hg_loop(ref_genesets, user_set, mht_flag):
    """
    This function finds the P-value of a given user set over each set in a reference file

    :param: ref_genesets: default dict of all GO terms, where one item looks like:
        GO:0086027	AV node cell to bundle of His cell signaling (6)	775	6330	6336	783	6331	54795
    :param: user_set: one SET of genes in a gene type, like so: {'123', '456'}
    :param: bool flag for multi hypo correction or not
    :return: if mht_flg == False: p_list: list of p values from every set in ref file, including the name of the user and ref sets
             if mht_flag == True: return multi hypo corrected p val list, including the name of the user and ref sets

    """
    p_list = []
    mht_list = []
    for ref_set in ref_genesets.values():
        pval = hg(ref_set, user_set, ref_genesets)
        p_list.append(pval)
    if mht_flag == True:
        p_val_list = p_list #for having multiple attributes use [x[0] for x in p_list]
        mht = statsmodels.stats.multitest.multipletests(p_val_list, alpha=0.05, method='fdr_bh', is_sorted=False,
                                                        returnsorted=False)
        p_corrected = mht[1]
        for pcorr in p_corrected:
            mht_list.append(pcorr)
        #TODO: mht function makes p_corrected return 1 and -0.0 only
        #return mht_list
    return p_list

"""
TESTING
input the user geneset and the reference genesets,
print the results
"""
#
# #reference genesets
ref_filename = 'hsa_EXP_BP_propagated.gmt'  #REPLACE W hsa_EXP_BP_propagated.gmt, a longer file
ref_parser = GMT(open(ref_filename, 'r')).genesets

# #grab one user geneset (currently hardcoded)
user_filename = 'drugtargets.gmt'
user_parser = GMT(open(user_filename, 'r')).genesets
user_GMT = GMT(open(user_filename, 'r'))

def gene_group(gene_list, ref_filename, user_filename, mht_flag):
    """
    generates a json data file of the genes--> significant GO terms

    :param gene_list: list of gene names in string form, i.e.:"DRB003918"
    :param ref_filename: reference geneset filename
    :param user_filename: user geneset filename
    :param mht_flag: bool for whether to apply mult. hypo. test
    :return:
    """
    # reference genesets
    ref_parser = GMT(open(ref_filename, 'r')).genesets
    #todo: get the GO descriptions, not numbers
    ref_setnames = ref_parser.keys()

    # grab one user geneset (currently hardcoded)
    user_GMT = GMT(open(user_filename, 'r'))
    user_setnames = GMT(open(user_filename, 'r')).setnames

    #get pval of all genes and their terms [geneName: pval, goTerm]
    #{"D34555": [(),(),()], }
    raw_pval_dict = dict()
    for gene_str in gene_list:
        #todo
        user_set_str = user_GMT.get_genes_str(gene_str)
        # print(user_set_str)
        ref_set_str = ref_parser.keys()
        # print(ref_set_str)
        user_set = set(user_set_str.split())
        p_corrected = hg_loop(ref_parser, user_set, mht_flag)
        p_to_name = zip(p_corrected, ref_setnames)
        #due to log change in first func
        p_to_name = sorted(p_to_name, reverse=True)
        #(-0.0, 'GO:0000432'),(-0.0, 'GO:0001432'),

        #find all sig terms-- this code leaves pvals of 1 to be blank for other gene sets without the sig pval!
        #print(p_to_name)
        p_to_name_clean = []
        for tup in p_to_name:
            if tup[0] > 0 :
                p_to_name_clean.append(tup)

        key = gene_str
        val = p_to_name_clean
        raw_pval_dict[key] = val
    # print(raw_pval_dict)
        print(p_to_name_clean)
    #find all significant terms
    sig_terms = dict()
    for key, lst in raw_pval_dict.items():
        for tup in lst:
            # if tup[0] != 1.0:
            if tup[0] >0:
                sig_terms[tup[1]] = tup[0]
    print(sig_terms)

    # check if term is significant, and then label them, and aggregate to array todo: this is actually useless because of the
    #todo: sig checker above^!
    clean = dict()
    for key, val in raw_pval_dict.items():
        newval = []
        for tup in val:
            newvalDict = {}
            if tup[1] in sig_terms.keys():
                newvalDict['pval'] = tup[0]
                newvalDict['GOterm'] = tup[1]
            #dont add empty dicts
            if newvalDict.items():
                newval.append(newvalDict)
        clean[key] = newval

    #make each geneName have its own dict--> geneName :{pval, GO}
    allDict = []
    for key, val in clean.items():
        singleDict = {}
        singleDict['gene name'] = key
        singleDict['values'] = val
        if singleDict:
            allDict.append(singleDict)
    with open('data1.json', 'w') as outfile:
        json.dump(allDict, outfile)

#test func
input_genelist = ["DRB003918","DRB003917", "DRB003901", "DRB003919",
              "DRB003929", "DRB003941", "DRB004025", "DRB004035",
              "DRB004025", "DRB004017"]
result = gene_group(input_genelist, ref_filename, user_filename, True)
print(result)



