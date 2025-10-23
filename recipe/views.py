from django.shortcuts import render
from django.views.generic import ListView
from .models import Recipe

class HomePage(ListView):
    model = Recipe
    template_name='home.html'
