from django.shortcuts import render, redirect
from django.contrib import messages
from recipe.models import Recipe, Nutrition, Ingredient, RecipeImage
from django.conf import settings
from itertools import zip_longest

def create_recipe(request):
    if request.method == "POST":
        # 1️⃣ Recipe fields
        title = request.POST.get('title')
        category = request.POST.get('category')
        cuisine = request.POST.get('cuisine')
        difficulty = request.POST.get('difficulty')
        servings = request.POST.get('servings')
        prep_time = request.POST.get('prep_time')
        total_time = request.POST.get('total_time')
        instructions = request.POST.get('instructions')
        featured = bool(request.POST.get('featured'))

        recipe = Recipe.objects.create(
            title=title,
            author=request.user,
            category=int(category),
            cuisine=cuisine,
            difficulty=int(difficulty),
            servings=int(servings),
            prep_time=int(prep_time),
            total_time=int(total_time),
            instructions=instructions,
            featured=featured
        )

        # 2️⃣ Nutrition
        calories = request.POST.get('calories')
        protein = request.POST.get('protein')
        fat = request.POST.get('fat')
        sugar = request.POST.get('sugar')
        fiber = request.POST.get('fiber')
        carbohydrates = request.POST.get('carbohydrates')

        Nutrition.objects.create(
            recipe=recipe,
            calories=int(calories or 0),
            protein=int(protein or 0),
            fat=int(fat or 0),
            sugar=int(sugar or 0),
            fiber=int(fiber or 0),
            carbohydrates=int(carbohydrates or 0)
        )

        # 3️⃣ Recipe Images
        images = request.FILES.getlist('recipe_images')
        for img in images:
            RecipeImage.objects.create(recipe=recipe, image=img)

        # 4️⃣ Ingredients
        ingredient_names = request.POST.getlist('ingredient_name[]')
        ingredient_quantities = request.POST.getlist('ingredient_quantity[]')
        ingredient_units = request.POST.getlist('ingredient_unit[]')
        ingredient_optionals = request.POST.getlist('ingredient_optional[]')

        for name, quantity, unit, optional in zip_longest(
            ingredient_names, ingredient_quantities, ingredient_units, ingredient_optionals, fillvalue=''
        ):
            name = (name or '').strip()
            if not name:
                continue
            Ingredient.objects.create(
                recipe=recipe,
                name=name,
                quantity=float(quantity or 0),
                unit=int(unit or 0),
                optional=optional == 'True'
            )

        messages.success(request, "Recipe created successfully!")
        return redirect('recipe:home')

    return render(request, 'recipe_management/add_recipe.html')
