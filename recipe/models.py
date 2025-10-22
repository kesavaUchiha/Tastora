from email.mime import image
from django.db import models
from django.conf import settings

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
    

class Profile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/',blank=True,null=True)
    bio = models.CharField(max_length=1000,blank=True)
    location = models.CharField(max_length=100,blank=True)
    

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='recipes')
    category = models.IntegerField(choices=CategoryTypes.CHOICES,default=CategoryTypes.VEG)
    cuisine =  models.CharField(max_length=50)
    difficulty = models.IntegerField(choices=DifficultyLevels.CHOICES,default=DifficultyLevels.EASY)
    servings = models.IntegerField(default=1,help_text="Number of people the recipe serves")
    prep_time = models.IntegerField(help_text="Time required to prepare ingredients")
    total_time = models.IntegerField(help_text="Preparation time + Cooking Time")
    calories = models.IntegerField()
    instructions = models.TextField()
    featured = models.BooleanField(default=False)
    

    class Meta:
        ordering = ("-created_at","title")
        unique_together = ('title', 'author')

    def __str__(self):
        return f'{self.title}'

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


    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='ingredients')
    name=models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.IntegerField(choices=UnitTypes.CHOICES,default=UnitTypes.GRAMS)
    optional = models.BooleanField(default=False)

class Collection(TimeStampedModel):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='collections')
    

    class Meta:
        ordering=('-created_at','title')
        unique_together = ('title', 'owner')

    def __str__(self):
        return f'{self.title}'
    
class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='recipe_img')
    created_at = models.DateTimeField(auto_now_add=True)
