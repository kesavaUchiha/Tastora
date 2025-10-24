from django.shortcuts import render, redirect
from django.contrib import messages
from recipe.models import Recipe, Nutrition, Ingredient, RecipeImage
from .forms import RecipeForm, NutritionForm, RecipeImageForm
from itertools import zip_longest
from decimal import Decimal

def create_recipe(request):
    recipe_form = RecipeForm(request.POST or None, request.FILES or None)
    nutrition_form = NutritionForm(request.POST or None)
    image_form = RecipeImageForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if recipe_form.is_valid() and nutrition_form.is_valid() and image_form.is_valid():
            # ✅ 1. Save Recipe
            recipe = recipe_form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            # ✅ 2. Save Nutrition
            nutrition = nutrition_form.save(commit=False)
            nutrition.recipe = recipe
            nutrition.save()

            # ✅ 3. Save Recipe Image
            recipe_image = image_form.save(commit=False)
            recipe_image.recipe = recipe
            recipe_image.save()

            # ✅ 4. Handle Ingredients
            ingredient_names = request.POST.getlist('ingredient_name[]')
            ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
            ingredient_units = request.POST.getlist('ingredient_unit[]')
            ingredient_optionals = request.POST.getlist('ingredient_optional[]')

            for name, quantity, unit, optional in zip_longest(
                ingredient_names, ingredient_quantities, ingredient_units, ingredient_optionals, fillvalue=''
            ):
                clean_name = (name or '').strip().lower()
                if not clean_name:
                    continue

                quantity = Decimal(quantity or "0")
                unit = int(unit or 0)
                is_optional = (optional == 'True')

                existing = Ingredient.objects.filter(recipe=recipe, name=clean_name).first()

                if existing:
                    existing.quantity = existing.quantity + quantity  # Decimal-safe addition
                    existing.unit = unit
                    existing.optional = is_optional
                    existing.save()
                else:
                    Ingredient.objects.create(
                        recipe=recipe,
                        name=clean_name,
                        quantity=quantity,
                        unit=unit,
                        optional=is_optional
                    )

            messages.success(request, "🎉 Recipe created successfully!")
            return redirect('recipe_management:create_recipe')
        else:
            messages.error(request, "⚠️ Please correct the form errors before submitting.")

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
