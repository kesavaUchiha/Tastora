from django import forms
from recipe.models import Recipe, Nutrition, RecipeImage

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title", "category", "cuisine", "difficulty",
            "servings", "prep_time", "total_time", "instructions", "featured"
        ]

class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition
        fields = ["calories", "protein", "fat", "sugar", "fiber", "carbohydrates"]

class RecipeImageForm(forms.ModelForm):
    class Meta:
        model = RecipeImage
        fields = ["image"]
