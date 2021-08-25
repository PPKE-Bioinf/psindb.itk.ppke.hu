from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='routes'),
    path('browse', TemplateView.as_view(template_name="browse.html")),
    path('entry/<str:uniprot_id>', views.entry, name='entry'),
    path('network/<str:accession>', views.network, name='network'),
    path('interactions', views.interactions, name='interactions'),
    path('manual', TemplateView.as_view(template_name="manual.html")),
    path('downloads', TemplateView.as_view(template_name="downloads.html")),
    path('faq', TemplateView.as_view(template_name="faq.html")),
    path('log', TemplateView.as_view(template_name="log.html")),
    path('related-pages', TemplateView.as_view(template_name="related-pages.html")),
    path('privacy-policy', TemplateView.as_view(template_name="privacy-policy.html")),
]
