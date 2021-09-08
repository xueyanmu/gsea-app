from django.http import HttpResponse
from django.http import HttpResponse
from django.template import loader

from .models import Gene, Geneset, Organism, CrossRefDB, CrossRef

def index(request):
    gene_list = Gene.objects.all()
    template = loader.get_template('a1/index.html')
    context = {
        'gene_list': gene_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, gene_id):
    return HttpResponse("You're looking at gene %s." % gene_id)
