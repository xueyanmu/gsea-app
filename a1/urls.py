from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:gene_id>/', views.detail, name='gene_detail'),
]