from django.conf.urls import url
from django.urls import path, include

import v1
from . import views

app_name = 'v1'

urlpatterns = [
    path('', views.base, name='base'),
    path('<int:gene_id>/', views.detail, name='gene_detail'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
    url(r'^', views.upload_file, name='upload_file'),
    url(r'^saved/$', views.upload_file, name='saved'),

]
