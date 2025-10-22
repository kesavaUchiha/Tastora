from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.CharField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.user)

class Recipe(TimeStampedModel):

    class CategoryTypes:
        VEG = 0
        VEGAN = 1
        NON_VEG = 2
        CHOICES = (
            (VEG, "Veg"),
            (VEGAN, "Vegan"),
            (NON_VEG, "Non-Veg"),
        )

    class DifficultyLevels:
        EASY = 0
        MEDIUM = 1
        HARD = 2
        CHOICES = (
            (EASY, "Easy"),
            (MEDIUM, "Medium"),
            (HARD, "Hard"),
        )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    category = models.IntegerField(validators=[MinValueValidator(0)],choices=CategoryTypes.CHOICES, default=CategoryTypes.VEG)
    cuisine = models.CharField(max_length=50)
    difficulty = models.IntegerField(validators=[MinValueValidator(0)],choices=DifficultyLevels.CHOICES, default=DifficultyLevels.EASY)
    servings = models.IntegerField(default=1, help_text="Number of people the recipe serves",validators=[MinValueValidator(1)])
    prep_time = models.IntegerField(help_text="Time required to prepare ingredients in minutes")
    total_time = models.IntegerField(help_text="Preparation time + Cooking Time in minutes",validators=[MaxValueValidator(300),MinValueValidator(5)])
    calories = models.IntegerField()
    instructions = models.TextField()
    featured = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at", "title")
        unique_together = ('title', 'author')
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.title

class Ingredient(TimeStampedModel):

    class UnitTypes:
        GRAMS = 0
        KILOGRAMS = 1
        TEASPOON = 2
        TABLESPOON = 3
        CUP = 4
        PIECES = 5
        CHOICES = (
            (GRAMS, "grams"),
            (KILOGRAMS, "kilograms"),
            (TEASPOON, "teaspoon"),
            (TABLESPOON, "tablespoon"),
            (CUP, "cup"),
            (PIECES, "pieces"),
        )

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.IntegerField(validators=[MinValueValidator(0)],choices=UnitTypes.CHOICES, default=UnitTypes.GRAMS)
    optional = models.BooleanField(default=False)

class Collection(TimeStampedModel):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='collections')

    class Meta:
        ordering = ('-created_at', 'title')
        unique_together = ('title', 'owner')

    def __str__(self):
        return self.title

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='recipe_img',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =('-created_at',)
