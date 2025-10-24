from django.urls import path
from . import views

app_name = "recipe_management"

urlpatterns = [
    path("recipes/create/", views.create_recipe, name="create_recipe"),
]
