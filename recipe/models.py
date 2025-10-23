from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', 
                                        blank=True, 
                                        null=True)
    bio = models.CharField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user}'

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='recipes')
    category = models.PositiveIntegerField(choices=CategoryTypes.CHOICES, 
                                           default=CategoryTypes.VEG)
    cuisine = models.CharField(max_length=50)
    difficulty = models.PositiveIntegerField(choices=DifficultyLevels.CHOICES, 
                                             default=DifficultyLevels.EASY)
    servings = models.PositiveIntegerField(default=1,
                                            help_text="Number of people the recipe serves")
    prep_time = models.PositiveIntegerField(help_text="Time required to prepare ingredients in minutes")
    total_time = models.PositiveIntegerField(help_text="Preparation time + Cooking Time in minutes",
                                             validators=[MaxValueValidator(300),
                                                         MinValueValidator(5)])
    calories = models.PositiveIntegerField(help_text="Estimated calories per serving")
    instructions = models.TextField()
    featured = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at", "title")
        unique_together = ('title', 'author')
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return f'{self.title}'
    
    def clean(self):

        if self.total_time < self.prep_time:
            raise ValidationError({
                'total_time': "Total time cannot be less than preparation time."
            })

class Ingredient(TimeStampedModel):

    class UnitTypes:
        GRAM = 0
        KILOGRAM = 1
        TEASPOON = 2
        TABLESPOON = 3
        CUP = 4
        PIECE = 5

        CHOICES = (
            (GRAM, "grams"),
            (KILOGRAM, "kilogram"),
            (TEASPOON, "teaspoon"),
            (TABLESPOON, "tablespoon"),
            (CUP, "cup"),
            (PIECE, "piece"),
        )

    recipe = models.ForeignKey(Recipe, 
                               on_delete=models.CASCADE, 
                               related_name='ingredients')
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, 
                                   decimal_places=2)
    unit = models.IntegerField(choices=UnitTypes.CHOICES,
                                default=UnitTypes.GRAM)
    optional = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class Collection(TimeStampedModel):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, 
                              on_delete=models.CASCADE, 
                              related_name='collections')
    recipes = models.ManyToManyField(Recipe, 
                                     blank=True)
    class Meta:
        ordering = ('-created_at', 'title')
        unique_together = ('title', 'owner')

    def __str__(self):
        return f"{self.title}"

def recipe_image_upload_to(instance, filename):
    return f'recipe_images/{instance.recipe.id}/{filename}'

class RecipeImage(TimeStampedModel):
    recipe = models.ForeignKey(Recipe,
                                on_delete=models.CASCADE, 
                                related_name='images')
    image = models.ImageField(upload_to=recipe_image_upload_to,
                               blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"Image for recipe: {self.recipe.title}"
