from django.urls import path
from . import views

app_name = "recipe_management"  # ✅ Required for namespacing

urlpatterns = [
    path("recipes/create/", views.create_recipe, name="create_recipe"),
    path("recipes/add-ingredient-form/", views.add_ingredient_form, name="add_ingredient_form"),  # ✅ Add this line
]
