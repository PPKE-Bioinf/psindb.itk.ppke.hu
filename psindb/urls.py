from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='routes'),
    path('entry/<str:uniprot_id>', views.entry, name='entry'),
    path('network/<str:accession>', views.network, name='network'),
    path('interactions', views.interactions, name='interactions'),
]
