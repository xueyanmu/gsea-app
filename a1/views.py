from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.db.models import Q
from .forms import DocumentForm
from .models import Document, Gene, Geneset, Organism, CrossRefDB, CrossRef, Geneset_membership
import statsmodels
from statsmodels.stats.multitest import multipletests
from scipy.stats import hypergeom
from a1 import GMT
import csv
import json
import math
from a1.models import Geneset


def base(request):
    # todo: decide whether to keep this feature
    search_post = request.GET.get('search')
    # search by the entrezID
    if search_post:
        genes = Gene.objects.filter(Q(entrezid__icontains=search_post) | Q(description__icontains=search_post))
    else:
        # Query all posts
        genes = Gene.objects.all()
    return render(request, 'a1/base.html', {'genes': genes})


def saved(request):
    return render(request, 'a1/saved.html')


def detail(request, gene_id):
    return HttpResponse("You're looking at gene %s." % gene_id)


# # upload form
def upload_file(request):
    saved = False
    missing_genes = []
    valid_genes = []
    geneset = None
    # Handle file upload

    if request.method == 'POST':
        img_file = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(img_file.name, img_file)
        uploaded_file_path = fs.path(filename)
        # print('absolute file path', uploaded_file_path)
        saved = True
        missing_genes.append(check_input(uploaded_file_path)[0])

        valid_genes.append(check_input(uploaded_file_path)[1])
        valid_genes = valid_genes[0]

        # calculate the P value
        # todo: do we still use random selected gene list like below?
        input_genelist = ["DRB003918", "DRB003917", "DRB003901", "DRB003919",
                          "DRB003929", "DRB003941", "DRB004025", "DRB004035",
                          "DRB004025", "DRB004017"]
        pval = get_p(input_genelist, valid_genes)
        print("PVAL HERE")
        print(pval)
        geneset = check_input(uploaded_file_path)[2]
    return render(request, 'a1/saved.html', locals())


def check_input(filename):
    """
    input:filename
    output:valid genes set, missing genes set,
    Reads space OR tab delimited genes, and marks unavailable ones,
    and adds the available ones.
    """
    missing = set()
    valid = []
    with open(filename, 'r') as f:
        f.readline()  # discard header
        for line in f:
            # Tab delimited- todo: how to add space AND tab functionality?
            tokens = line.split('\t')
            geneset_type = tokens[0]
            entrez = tokens[1]
            symbol = tokens[2]
            if entrez != '':
                try:
                    gene = Gene.objects.get(entrezid=entrez)
                    valid.append(gene)
                except:
                    missing.add(entrez)

        ref_set = {}
        user_set = {}
    return missing, valid, geneset_type


def get_p(gene_list, user_set):
    result = gene_group(gene_list, user_set, True)
    print("RESULT")
    print(result)
    return result


"""
=======================================

"""


def hg(ref_set, user_set, ref_genesets):
    """
    computes hypergeometric value between 2 sets.
    :param ref_set_name: set of genes
    :param user_set: set of genes
    :param ref_genesets: list of set of all genes in database
    :return: pval: the two-tailed p value between the 2 sets of genes
            ref_set_name, user_set
    """
    m = len(ref_set)
    k = len(user_set)
    x = len(user_set.intersection(ref_set))
    M = 0
    #
    for val_set in ref_genesets:
        M += len(val_set)
    pval = hypergeom.sf(x - 1, M, k, m)

    # use negative log here to indicate logarithmic significance
    return -(math.log(pval))


def hg_loop(ref_sets, user_set, mht_flag):
    """
    This function finds the P-value of a given user set over each set in a reference file

    :param: ref_sets:
        collection of all sets of genes, like so: [{'123', '456'}, , {'123', '4567'}]
    :param: user_set: one SET of genes in a gene type, like so: {'123', '456'}
    :param: bool flag for multi hypo correction or not
    :return: if mht_flg == False: p_list: list of p values from every set in ref file, including the name of the user and ref sets
             if mht_flag == True: return multi hypo corrected p val list, including the name of the user and ref sets

    """
    p_list = []
    mht_list = []
    for ref_set in ref_sets:
        ref_set = set(ref_set)
        user_set = set(user_set)
        pval = hg(ref_set, user_set, ref_sets)

        if pval > 0:
            print("pval in hg loop")
            print(pval)

        p_list.append(pval)

    if mht_flag == True:
        p_val_list = p_list  # for having multiple attributes use [x[0] for x in p_list]
        mht = statsmodels.stats.multitest.multipletests(p_val_list, alpha=0.05, method='fdr_bh', is_sorted=False,
                                                        returnsorted=False)
        p_corrected = mht[1]
        for pcorr in p_corrected:
            mht_list.append(pcorr)
        # TODO: mht function makes p_corrected return 1 and -0.0 only
        # return mht_list
    return p_list


"""
#ref_sets is a list of sets of genes
ref_sets = []
for ref in Geneset.objects.all():
    #get the genes in entrez form for each geneset- 
    ref_set = ref.Genes.all().values_list('entrezid', flat=True) # -- queryset of genes
    ref_sets.append(set(ref_set))
    
    

"""


def gene_group(gene_list, pre_user_set, mht_flag):
    # process user set into set of entrezID nums
    user_set = []
    for genes in pre_user_set:
        id = genes.entrezid
        user_set.append(id)

    print("user set")
    print(user_set)

    # ref_sets is a dict of
    ref_sets_entrez = []
    ref_sets_names = []
    for ref in Geneset.objects.all():
        # get the genes in entrez form for each geneset-

        """
        committee_relations = CommitteeRole.objects.filter(user=request.user).values_list('committee__pk', flat=True)
        item_list = Item.objects.filter(committees__in=committee_relations)
        """
        setname = ref.id
        geneset_relations = Geneset_membership.objects.filter(geneset=setname).values_list('geneset__pk', flat=True)
        # print("geneset_relations")
        # print(geneset_relations)

        ref_genes_list = Gene.objects.filter(geneset_name__in=geneset_relations).values_list('entrezid', flat=True)
        # print("ref_genes_list")
        # print(ref_genes_list)
        #

        ref_sets_entrez.append(ref_genes_list)
        ref_sets_names.append(setname)
        # print("ref set entrez")
        # print(ref_sets_entrez)

        # get pval of all genes and their terms [geneName: pval, goTerm]
        # {"D34555": [(),(),()], }

    raw_pval_dict = dict()

    """
    1. make sure this is what gene_str in gene)list for looop is doing
    
    2. replace gene_list iwth user set and obtain user set names 
    """


    p_corrected = hg_loop(ref_sets_entrez, user_set, mht_flag)

    print('P CORRECTED')
    print(p_corrected)
    print('ref set names')
    print(ref_sets_names)


    p_to_name = zip(p_corrected, ref_sets_names)
    # due to log change in first func
    p_to_name = sorted(p_to_name, reverse=True)
    # (-0.0, 'GO:0000432'),(-0.0, 'GO:0001432'),

    # find all sig terms-- this code leaves pvals of 1 to be blank for other gene sets without the sig pval!
    # print(p_to_name)
    p_to_name_clean = []
    for tup in p_to_name:
        if tup[0] > 0:
            p_to_name_clean.append(tup)

    print("p to name clean")
    print(p_to_name_clean)

    key = gene_list[0]
    val = p_to_name_clean
    raw_pval_dict[key] = val
    # print(raw_pval_dict)


    # print(p_to_name_clean)
    # find all significant terms
    sig_terms = dict()
    for key, lst in raw_pval_dict.items():
        for tup in lst:
            # if tup[0] != 1.0:
            if tup[0] > 0:
                sig_terms[tup[1]] = tup[0]

    print("sig terms!")
    print(sig_terms)

    # check if term is significant, and then label them, and aggregate to array
    # todo: this is actually useless because of the
    # todo: sig checker above^!
    clean = dict()
    for key, val in raw_pval_dict.items():
        newval = []
        for tup in val:
            newvalDict = {}
            if tup[1] in sig_terms.keys():
                newvalDict['pval'] = tup[0]
                newvalDict['GOterm'] = tup[1]
            # dont add empty dicts
            if newvalDict.items():
                newval.append(newvalDict)
        clean[key] = newval

    # make each geneName have its own dict--> geneName :{pval, GO}
    allDict = []
    for key, val in clean.items():
        singleDict = {}
        singleDict['geneset name'] = key
        singleDict['values'] = val
        if singleDict:
            allDict.append(singleDict)
    with open('data1.json', 'w') as outfile:
        json.dump(allDict, outfile)

    return allDict

# test func
input_genelist = ["DRB003918", "DRB003917", "DRB003901", "DRB003919",
                  "DRB003929", "DRB003941", "DRB004025", "DRB004035",
                  "DRB004025", "DRB004017"]

input_genelist = ["DRB003918"]
