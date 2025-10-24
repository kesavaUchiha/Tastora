from django.shortcuts import render
from django.views.generic import ListView
from recipe.models import Recipe

class AddRecipe(ListView):
    template_name='add_recipe.html'
    model = Recipe
