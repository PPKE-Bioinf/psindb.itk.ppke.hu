from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('entry/<str:uniprot_id>', views.entry, name='entry'),

    path('network/<str:accession>', views.network, name='network')
    # path('protein/<str:protein_id>', views.protein, name='protein')
]