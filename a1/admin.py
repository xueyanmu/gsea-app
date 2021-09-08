from django.contrib import admin
from django.shortcuts import render

from .models import Gene, Geneset, Organism, CrossRefDB, CrossRef
# Register your models here.
admin.site.register(Gene)
admin.site.register(Geneset)
admin.site.register(Organism)
admin.site.register(CrossRefDB)
admin.site.register(CrossRef)
