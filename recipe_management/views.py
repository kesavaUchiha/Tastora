from django.shortcuts import render, redirect
from django.contrib import messages
from recipe.models import Recipe, Nutrition, Ingredient, RecipeImage
from .forms import RecipeForm, NutritionForm, RecipeImageForm
from itertools import zip_longest
from decimal import Decimal

def create_recipe(request):
    recipe_form = RecipeForm(request.POST or None, request.FILES or None)
    nutrition_form = NutritionForm(request.POST or None)
    image_form = RecipeImageForm(request.POST, request.FILES or None)

    if request.method == "POST":
        if recipe_form.is_valid() and nutrition_form.is_valid() and image_form.is_valid():
            # Check ingredients
            ingredient_names = request.POST.getlist('ingredient_name[]')
            if not any(name.strip() for name in ingredient_names):
                messages.error(request, "⚠️ Please add at least one ingredient for the recipe.")
                return render(
                    request,
                    'recipe_management/add_recipe.html',
                    {
                        'recipeform': recipe_form,
                        'nutritionform': nutrition_form,
                        'recipe_image': image_form,
                    }
                )

            # Save Recipe
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # Save Nutrition
            nutrition = nutrition_form.save(commit=False)
            nutrition.recipe = recipe
            nutrition.save()

            # Save Recipe Image
            recipe_image = image_form.save(commit=False)
            recipe_image.recipe = recipe
            recipe_image.save()

            # Save Ingredients
            ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
            ingredient_units = request.POST.getlist('ingredient_unit[]')
            ingredient_optionals = request.POST.getlist('ingredient_optional[]')

            for name, quantity, unit, optional in zip_longest(
                ingredient_names, ingredient_quantities, ingredient_units, ingredient_optionals, fillvalue=''
            ):
                clean_name = (name or '').strip()
                if not clean_name:
                    continue

                Ingredient.objects.create(
                    recipe=recipe,
                    name=clean_name.lower(),
                    quantity=Decimal(quantity or "0"),
                    unit=int(unit or 0),
                    optional=(optional == "True")
                )

            messages.success(request, "🎉 Recipe created successfully!")
            return redirect('recipe_management:create_recipe')
        else:
            messages.error(request, "⚠️ Please correct the errors in the form below.")

    return render(
        request,
        'recipe_management/add_recipe.html',
        {
            'recipeform': recipe_form,
            'nutritionform': nutrition_form,
            'recipe_image': image_form,
        }
    )
# ✅ HTMX ingredient partial
def add_ingredient_form(request):
    return render(request, "recipe_management/forms/_ingredient_form.html")
