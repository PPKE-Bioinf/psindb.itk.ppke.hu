from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    # path('home/<str:search>', views.index, name='home'),
    # path('protein/<str:protein_id>', views.protein, name='protein')
]