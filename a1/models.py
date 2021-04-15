from django.db import models
from django.core.exceptions import FieldError
from genes.models import Gene, CrossRef, CrossRefDB
from organisms.models import Organism

#TODO: do we need to ensure Organism is loaded first
class Geneset(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    size = models.IntegerField(default=0)
    grouping = models.CharField(max_length=64)
    organisms = models.OneToOneField(Organism, on_delete=models.CASCADE)
    function_database = models.CharField(max_length=200)
    genes = models.ManyToManyField(Gene)

#todo: use Organism in the manytomany with geneset?


    class Meta:
        ordering = ['id']


    def __str__(self):
        return str(self.id)


#gs = Geneset(id="lung gene set", size=10, grouping="GO term", organism="homo sapiens", function_database="crossRef")