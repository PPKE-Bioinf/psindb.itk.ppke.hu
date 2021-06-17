from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='routes'),
    path('entry/<str:uniprot_id>', views.entry, name='entry'),
    path('network/<str:accession>', views.network, name='network'),
    path('interactions', views.interactions, name='interactions'),
    path('manual', TemplateView.as_view(template_name="manual.html")),
]
