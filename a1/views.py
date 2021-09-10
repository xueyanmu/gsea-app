from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import DocumentForm
from .models import Document, Gene, Geneset, Organism, CrossRefDB, CrossRef


def index(request):
    gene_list = Gene.objects.all()
    template = loader.get_template('a1/index.html')
    context = {
        'gene_list': gene_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, gene_id):
    return HttpResponse("You're looking at gene %s." % gene_id)


# upload form
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the document list after POST
            #return HttpResponse(redirect('index'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return HttpResponse(render(
        request,
        'a1/list.html',
        {'documents': documents, 'form': form}
    ))
