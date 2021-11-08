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
from .models import Document, Gene, Geneset, Organism, CrossRefDB, CrossRef


def base(request):
    #todo: decide whether to keep this feature
    search_post = request.GET.get('search')
    #search by the entrezID
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
        #print('absolute file path', uploaded_file_path)
        saved = True
        missing_genes.append(check_input(uploaded_file_path)[0])

        valid_genes.append(check_input(uploaded_file_path)[1])
        valid_genes=valid_genes[0]
        # for g in valid_genes:
        # #print(g)
        # #print(valid_genes)
        geneset = check_input(uploaded_file_path)[2]
    return render(request, 'a1/saved.html', locals())


def check_input(filename):
    """
    Reads space OR tab delimited genes, and marks unavailable ones,
    and adds the available ones.
    """
    missing = set()
    valid = []
    matching_genesets = None
    with open(filename, 'r') as f:
        f.readline()  # discard header
        for line in f:
            #Tab delimited- todo: how to add space AND tab functionality?
            tokens = line.split('\t')
            #tokens = [x.strip() for x in tokens]
            entrez = tokens[1]
            symbol = tokens[2]
            if entrez != '':
                all_genes = Gene.objects.all()
                for gene in all_genes:

                    if Gene.objects.filter(entrezid__icontains=entrez):
                        if gene not in valid:
                            valid.append(gene)
                in_database = Gene.objects.filter(entrezid__icontains=entrez).distinct()

                #TODO: fix this workaround to properly get the geneset type
                #Todo: rename this variable
                matching_genesets = Geneset.objects.all()[0]
                if not in_database:
                    missing.add(entrez)
    return missing, valid, matching_genesets


class HomePageView(TemplateView):
    template_name = 'a1/base.html'


class SearchResultsView(ListView):
    model = Gene
    template_name = 'a1/search_results.html'

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        object_list = Gene.objects.filter(
            Q(entrezid__icontains=query) | Q(systemic_name__icontains=query | Q(standard_name__icontains=query))
        )
        return object_list
